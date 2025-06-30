from base64 import b64encode
from dataclasses import dataclass
from datetime import date
from datetime import datetime
from pathlib import Path


@dataclass
class SketchSize:
    """Dimensions of the sketch."""

    external: tuple[int, int]
    internal: tuple[int, int]

    @property
    def pos_interno(self) -> tuple[int, int]:
        """Posição interna do sketch."""
        x, y = self.internal
        x = (self.external[0] - x) // 2
        y = (self.external[1] - y) // 2
        return x, y


@dataclass
class SketchInfo:
    """Basic information about a sketch."""

    path: Path
    title: str
    description: str
    other_credits: str
    alt: str
    format: str
    tags: list[str]
    size: SketchSize

    @property
    def day(self) -> date:
        """Dia do Sketch."""
        parts = [int(i) for i in (self.path.name[1:]).split("_")]
        return date(*parts)

    @property
    def filename(self) -> str:
        """Nome do arquivo de imagem / vídeo."""
        return f"{self.day}.{self.format}"

    @property
    def filepath(self) -> Path:
        """Path para o arquivo."""
        path = self.path
        filename = self.filename
        return path / filename

    @property
    def exists(self) -> bool:
        """Confirma se arquivo existe."""
        return self.filepath.exists()


@dataclass
class Sketch:
    """Sketch data."""

    info: SketchInfo
    commit_hash: str | None = None
    commit_date: datetime | None = None
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
