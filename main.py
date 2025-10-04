from typing import Any
import requests
from dotenv import load_dotenv
import os

load_dotenv()


def get_userinfo(secret: str) -> tuple[dict[str, Any], str]:
    url = "https://api.linkedin.com/v2/userinfo"
    headers = {"Authorization": f"Bearer {secret}"}
    response_json = requests.get(url, headers=headers).json()
    return response_json, response_json["sub"]


def post_content(content: str, profile_id: str, access_token: str):
    headers = {
        "Content-Type": "application/json",
        "X-Restli-Protocol-Version": "2.0.0",
        "Authorization": "Bearer " + access_token,
    }
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


def main():
    user_secret = os.getenv("USER_SECRET")
    assert user_secret is not None, "USER_SECRET env is empty, fill it up"
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    user_info, profile_id = get_userinfo(user_secret)
    response = post_content(
        "Hellow world from linkedin API because why not", profile_id, user_secret
    )
    print(response)
    print(user_info, profile_id, sep="\n\n")


if __name__ == "__main__":
    main()
