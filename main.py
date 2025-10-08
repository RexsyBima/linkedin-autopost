import os
from youtube_transcript_api import YouTubeTranscriptApi, FetchedTranscript
from pprint import pprint as print
from typing import Any
import re
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from markdown import markdown

load_dotenv()
ytt_api = YouTubeTranscriptApi()


def _get_youtube_id(url: str) -> str | None:
    """
    Extracts the video ID from a YouTube URL.

    Args:
        url (str): The YouTube video URL.

    Returns:
        str | None: The video ID if found, otherwise None.
    """
    pattern = r"(?:v=|\/)([0-9A-Za-z_-]{11}).*"
    match = re.search(pattern, url)
    return match.group(1) if match else None


def _get_youtube_full_text(transcript: FetchedTranscript) -> str:
    output = ""
    for t in transcript:
        output += t.text
    return output


def _get_userinfo(secret: str) -> tuple[dict[str, Any], str]:
    url = "https://api.linkedin.com/v2/userinfo"
    headers = {"Authorization": f"Bearer {secret}"}
    response_json = requests.get(url, headers=headers).json()
    return response_json, response_json["sub"]


def _register_media(profile_id: str, access_token: str):
    headers = {
        "Content-Type": "application/json",
        "X-Restli-Protocol-Version": "2.0.0",
        "Authorization": "Bearer " + access_token,
    }

    post_data = {
        "registerUploadRequest": {
            "recipes": ["urn:li:digitalmediaRecipe:feedshare-image"],
            "owner": "urn:li:person:" + profile_id,
            "serviceRelationships": [
                {
                    "relationshipType": "OWNER",
                    "identifier": "urn:li:userGeneratedContent",
                }
            ],
        }
    }
    url = "https://api.linkedin.com/v2/assets?action=registerUpload"
    response = requests.post(url, headers=headers, json=post_data)
    return response


def post_content_no_image(content: str, profile_id: str, access_token: str):
    url = "https://api.linkedin.com/v2/ugcPosts"

    headers = {
        "Content-Type": "application/json",
        "X-Restli-Protocol-Version": "2.0.0",
        "Authorization": "Bearer " + access_token,
    }
    post_data = {
        "author": "urn:li:person:" + profile_id,
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {"text": content},
                "shareMediaCategory": "NONE",
            }
        },
        "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"},
    }

    response = requests.post(url, headers=headers, json=post_data)
    return response


def _post_content_image(
    content: str, profile_id: str, access_token: str, media_asset: str
):
    url = "https://api.linkedin.com/v2/ugcPosts"
    headers = {
        "Content-Type": "application/json",
        "X-Restli-Protocol-Version": "2.0.0",
        "Authorization": "Bearer " + access_token,
    }
    post_data = {
        "author": f"urn:li:person:{profile_id}",
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {"text": content},
                "shareMediaCategory": "IMAGE",
                "media": [
                    {
                        "status": "READY",
                        "description": {"text": "Center stage!"},
                        "media": media_asset,
                        "title": {"text": "LinkedIn Talent Connect 2021"},
                    }
                ],
            }
        },
        "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"},
    }
    response = requests.post(url, headers=headers, json=post_data)
    return response


def post_personal_branding_with_image(
    image_path: str | None = None, content: str | None = None
):
    user_secret = os.getenv("USER_SECRET")
    if image_path is None or content is None or user_secret is None:
        raise Exception(
            "parameter of image_path and content must be filled bruh, also .env of USER_SECRET must be filled"
        )
    _, profile_id = _get_userinfo(user_secret)
    response = _register_media(profile_id, user_secret)
    asset = response.json()["value"]["asset"]
    url = response.json()["value"]["uploadMechanism"][
        "com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest"
    ]["uploadUrl"]

    headers = {"Authorization": f"Bearer {os.getenv('USER_SECRET')}"}
    with open(image_path, "rb") as f:
        response = requests.post(url, headers=headers, data=f)
    response = _post_content_image(
        content=content,
        profile_id=profile_id,
        access_token=user_secret,
        media_asset=asset,
    )

    print(response)
    print(response.status_code)
    print(response.json())


def html_to_text_with_lists(soup: BeautifulSoup):
    lines = []

    def walk(node, indent=0, ol_level=0):
        if node.name == "ul":
            for li in node.find_all("li", recursive=False):
                lines.append("  " * indent + "* " + walk(li, indent + 1))
        elif node.name == "ol":
            i = 1
            for li in node.find_all("li", recursive=False):
                lines.append("  " * indent + f"{i}. " + walk(li, indent + 1))
                i += 1
        elif node.name == "li":
            # If li has nested ul/ol, handle separately
            text = node.get_text(" ", strip=True)
            sublists = node.find_all(["ul", "ol"], recursive=False)
            return text if not sublists else text
        else:
            # For headings, paragraphs, etc.
            if node.string:
                return node.string.strip()
            else:
                return " ".join(
                    child.get_text(" ", strip=True) for child in node.children if child
                )

    for child in soup.children:
        txt = walk(child)
        if txt:
            if isinstance(txt, str):
                lines.append(txt)

    return "\n".join(lines)


def get_youtube_text(url: str) -> str:
    video_id = _get_youtube_id(url)
    assert video_id is not None, "Video ID incorrect"
    transcript = _get_youtube_full_text(ytt_api.fetch(video_id))
    return transcript


if __name__ == "__main__":
    url = "https://www.youtube.com/watch?v=rxSVfhUXRDU&t=113s"
    video_id = _get_youtube_id(url)
    print(video_id)  # Output: rxSVfhUXRDU
    assert video_id is not None, "Video ID incorrect"
    transcript = _get_youtube_full_text(ytt_api.fetch(video_id))
    print(transcript)
    exit()
    output = ""
    with open("./input.md", "r") as f:
        soup = BeautifulSoup(markdown(f.read()), "html.parser")
        text_content = html_to_text_with_lists(soup)
        # text_content = soup.get_text()
        # print(text_content)
    with open("./output.txt", "w") as f:
        f.writelines(text_content)
    # post_personal_branding_with_image("./tes.png", content=output)
    #
    #
    #
