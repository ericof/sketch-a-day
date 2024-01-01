from base64 import b64encode
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import List


@dataclass
class SketchInfo:
    """Basic information about a sketch."""

    path: Path
    title: str
    description: str
    alt: str
    format: str
    tags: List[str]

    @property
    def day(self) -> date:
        """Dia do Sketch."""
        parts = [int(i) for i in (self.path.name[1:]).split("_")]
        return date(*parts)

    @property
    def filename(self) -> str:
        """Nome do arquivo de imagem / vídeo."""
        return f"{self.day}.{self.format}"


@dataclass
class Sketch:
    """Sketch data."""

    info: SketchInfo
    commit_date: datetime = None
    url: str = ""

    def blob(self):
        """Blob data."""
        info = self.info
        blob = info.path / info.filename
        return b64encode(blob.read_bytes())

    def code(self):
        """Sketch code data."""
        info = self.info
        code_file = info.path / "__main__.py"
        return code_file.read_text()
