import os
from pathlib import Path

import requests


def download_service(
    platform: str,
    owner: str,
    repo: str,
    destination: str,
    token: str | None = None,
):
    headers = {
        "Accept": "application/vnd.github+json",
    }

    if token:
        headers["Authorization"] = f"Bearer {token}"

    api_url = f"https://api.github.com/repos/{owner}/{repo}/releases"
    response = requests.get(api_url, headers=headers, timeout=30)
    response.raise_for_status()

    releases = response.json()

    # Find the first release containing an .exe asset.
    allowed_extensions = (".exe", ".msi", ".zip")

    for release in releases:
        for asset in release.get("assets", []):
            asset_name = asset["name"]

            if not asset_name.lower().endswith(allowed_extensions):
                continue
            if not platform in asset_name.lower():
                continue

            asset_response = requests.get(
                asset["browser_download_url"],
                headers=headers,
                stream=True,
                timeout=120,
            )
            asset_response.raise_for_status()

            output_path = Path(destination) / asset_name
            output_path.parent.mkdir(parents=True, exist_ok=True)

            with output_path.open("wb") as output_file:
                for chunk in asset_response.iter_content(
                    chunk_size=1024 * 1024
                ):
                    if chunk:
                        output_file.write(chunk)

            return output_path

    raise FileNotFoundError(
        "No .exe, .msi, or .zip asset was found in the GitHub releases."
    )

