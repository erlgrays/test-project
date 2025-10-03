import os
import sys
import requests
from dotenv import load_dotenv

"""
Downloads a PNG from a Figma file/node using FIGMA_TOKEN, FIGMA_FILE_KEY, FIGMA_NODE_ID.
Saves to FIGMA_BASELINE_PATH (default: .playwright/figma_baseline.png)
Usage: python scripts/figma_fetch.py
"""


def main() -> int:
    load_dotenv()
    token = os.getenv("FIGMA_TOKEN")
    file_key = os.getenv("FIGMA_FILE_KEY")
    node_id = os.getenv("FIGMA_NODE_ID")
    scale = os.getenv("FIGMA_SCALE", "1")
    out_path = os.getenv("FIGMA_BASELINE_PATH", ".playwright/figma_baseline.png")

    if not token or not file_key or not node_id:
        print("FIGMA_TOKEN, FIGMA_FILE_KEY, FIGMA_NODE_ID env vars are required", file=sys.stderr)
        return 2

    headers = {"X-Figma-Token": token}
    images_url = f"https://api.figma.com/v1/images/{file_key}?ids={node_id}&format=png&scale={scale}"
    r = requests.get(images_url, headers=headers, timeout=30)
    r.raise_for_status()
    data = r.json()
    image_url = data.get("images", {}).get(node_id)
    if not image_url:
        print("Failed to obtain image URL from Figma API", file=sys.stderr)
        return 3

    img_resp = requests.get(image_url, timeout=60)
    img_resp.raise_for_status()

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "wb") as f:
        f.write(img_resp.content)

    print(f"Saved Figma baseline to {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
