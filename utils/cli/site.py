from uuid import uuid4

import requests
from prettyconf import config

from utils.data import Sketch


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


def post_to_site(sketch: Sketch):
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
    blocks_layout = [k for k in blocks]
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
    response = session.post(settings["base_url"], json=payload)
    if response.status_code != 201:
        raise Exception()
    data = response.json()
    return data["@id"]
