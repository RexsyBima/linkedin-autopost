from typing import Any
from pprint import pprint as print
import requests
from dotenv import load_dotenv
import os

load_dotenv()


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
    if image_path is None or content is None:
        raise Exception("parameter of image_path and content must be filled bruh")
    user_secret = os.getenv("USER_SECRET")
    assert user_secret is not None, "user secret must be filled"
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


if __name__ == "__main__":
    post_personal_branding_with_image()
