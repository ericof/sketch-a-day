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

    @property
    def centro(self) -> tuple[int, int]:
        """Ponto central do sketch."""
        x, y = self.external
        x //= 2
        y //= 2
        return x, y

    @property
    def vertices_interno(
        self,
    ) -> tuple[
        tuple[int, int],
        tuple[int, int],
        tuple[int, int],
        tuple[int, int],
    ]:
        """Vértices da área interna."""
        x, y = self.internal
        x = (self.external[0] - x) // 2
        y = (self.external[1] - y) // 2
        vertices = (
            (x, y),
            (x + self.internal[0], y),
            (x + self.internal[0], y + self.internal[1]),
            (x, y + self.internal[1]),
        )
        return vertices


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
        parts = self.path.parent.name.split("_")
        parts.append(self.path.name)
        parts = [int("".join([char for char in i if char.isdigit()])) for i in parts]
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
