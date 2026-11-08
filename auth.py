import os

import httpx
import msal
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.environ["CLIENT_ID"]
AUTHORITY = "https://login.microsoftonline.com/consumers"
SCOPES = ["Mail.Read"]
CACHE_FILE = "token_cache.json"


def get_token() -> str:
    cache = msal.SerializableTokenCache()
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE) as f:
            contents = f.read()
        cache.deserialize(contents)
    app = msal.PublicClientApplication(
        CLIENT_ID, authority=AUTHORITY, token_cache=cache
    )
    accounts = app.get_accounts()
    result = None
    if accounts:
        result = app.acquire_token_silent(SCOPES, account=accounts[0])
    if not result:
        result = app.acquire_token_interactive(SCOPES)
    if "access_token" not in result:
        raise RuntimeError(f"Login failed {result.get('error_description')}")

    if cache.has_state_changed:
        with open(CACHE_FILE, "w") as f:
            f.write(cache.serialize())

    return result["access_token"]


if __name__ == "__main__":
    token = get_token()
    response = httpx.get(
        "https://graph.microsoft.com/v1.0/me/mailFolders",
        headers={"Authorization": f"Bearer {token}"},
    )
    response.raise_for_status()
    for folder in response.json()["value"]:
        print(f"{folder['displayName']}, {folder['id']}")
