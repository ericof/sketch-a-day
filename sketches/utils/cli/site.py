from pathlib import Path
from prettyconf import config
from sketches.utils.data import Sketch
from uuid import uuid4

import requests


BASE_REPO_URL = "https://github.com/ericof/sketch-a-day/tree"


def site_settings() -> dict:
    return {
        "user": config("SITE_USER"),
        "password": config("SITE_PASSWORD"),
        "base_url": config("SITE_BASE_URL"),
    }


def _code_block(
    code: str, language: str = "python", line_numbers: bool = True, wrap: bool = True
):
    """Code block."""
    return {
        "code": code,
        "language": language,
        "lineNbr": 1,
        "showLineNumbers": line_numbers,
        "wrapLongLines": wrap,
        "style": "dark",
    }


def _construct_repo_url(path: Path, commit_hash: str = "") -> str:
    """Construct the URL for the sketch."""
    return f"{BASE_REPO_URL}/{commit_hash}/{path}"


def post_to_site(sketch: Sketch, commit_hash: str = ""):
    settings = site_settings()
    session = requests.session()
    session.auth = (settings["user"], settings["password"])
    info = sketch.info
    o_id = f"{info.day}"
    title = info.title
    description = info.description
    data = sketch.blob()
    code = sketch.code()
    blocks = {}
    for block_type in ("title", "slate", "codeBlock"):
        blocks[str(uuid4())] = {"@type": block_type}
    blocks_layout = list(blocks.keys())
    # Code block
    code_block = _code_block(code)
    blocks[blocks_layout[-1]].update(code_block)
    payload = {
        "@type": "Sketch",
        "id": o_id,
        "title": title,
        "description": description,
        "created": f"{sketch.commit_date}",
        "effective": f"{sketch.commit_date}",
        "modified": f"{sketch.commit_date}",
        "preview_caption": info.alt,
        "preview_image": {
            "content-type": "image/gif" if info.format == ".gif" else "image/png",
            "encoding": "base64",
            "filename": f"{info.day}",
            "data": data.decode("utf-8"),
        },
        "blocks": blocks,
        "blocks_layout": {"items": blocks_layout},
        "subjects": info.tags,
    }
    response = session.post(settings["base_url"], json=payload, timeout=20)
    if response.status_code != 201:
        msg = f"Error posting to site: {response.status_code} - {response.text}"
        raise Exception(msg)
    data = response.json()
    return data["@id"]
