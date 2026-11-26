from pathlib import Path
from plone_client import PloneClient
from plone_client import blocks
from plone_client import file_data
from prettyconf import config
from sketches.utils.data import Sketch

import os


BASE_REPO_URL = "https://github.com/ericof/sketch-a-day/tree"

API_PREFIX = "++api++"

TIMEOUT: int = int(os.environ.get("SITE_TIMEOUT", 20))


def site_settings() -> dict:
    return {
        "user": config("SITE_USER"),
        "password": config("SITE_PASSWORD"),
        "base_url": config("SITE_BASE_URL"),
    }


def _site_root(base_url: str) -> str:
    """Root URL of the site, for a folder URL that may carry ``++api++``.

    :param base_url: URL of the folder sketches are added to, such as
        ``https://ericof.com/++api++/en/sketches``.
    :returns: The URL before ``/++api++``, or ``base_url`` itself when it has
        no API prefix.
    """
    return base_url.split(f"/{API_PREFIX}", 1)[0]


def _code_block(
    code: str, language: str = "python", line_numbers: bool = True, wrap: bool = True
) -> dict:
    """Code block."""
    return blocks.block(
        "codeBlock",
        code=code,
        language=language,
        lineNbr=1,
        showLineNumbers=line_numbers,
        wrapLongLines=wrap,
        style="dark",
    )


def _construct_repo_url(path: Path, commit_hash: str = "") -> str:
    """Construct the URL for the sketch."""
    return f"{BASE_REPO_URL}/{commit_hash}/{path}"


def post_to_site(sketch: Sketch, commit_hash: str = "") -> str:
    """Create the sketch's page on the site.

    :param sketch: The sketch to publish.
    :param commit_hash: Commit of the sketch; not used yet.
    :returns: URL of the new page.
    :raises plone_client.PloneClientError: If the site cannot be reached or
        refuses the page.
    """
    settings = site_settings()
    base_url = settings["base_url"]
    info = sketch.info
    image = file_data(
        info.filepath,
        filename=f"{info.day}",
        content_type="image/gif" if info.format == ".gif" else "image/png",
    )
    payload = {
        "id": f"{info.day}",
        "title": info.title,
        "description": info.description,
        "created": f"{sketch.commit_date}",
        "effective": f"{sketch.commit_date}",
        "modified": f"{sketch.commit_date}",
        "preview_caption": info.alt,
        "preview_image": image,
        "subjects": info.tags,
        **blocks.build(
            blocks.title(),
            blocks.block("slate"),
            _code_block(sketch.code()),
        ),
    }
    with PloneClient(
        _site_root(base_url),
        username=settings["user"],
        password=settings["password"],
        timeout=TIMEOUT,
    ) as site:
        item = site.content.create(base_url, "Sketch", payload)
    return item["@id"]
