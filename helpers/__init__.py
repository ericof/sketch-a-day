from PIL import Image
from pathlib import Path
from random import choice
import tempfile
import py5


WIDTH = 800
HEIGHT = 800


def write_legend(palette=None, img_name=""):
    if palette:
        color = palette[-1]
    else:
        color = "#000"
    py5.fill(color)
    py5.text_size(12)
    py5.text_align(py5.RIGHT)
    py5.text(img_name, WIDTH - 20, HEIGHT - 20)


def save_image(img_name, extension="jpg"):
    folder = Path(__file__).parent.parent.resolve()
    img_folder = folder / "Images"
    img_path = img_folder / f"{img_name}.{extension}"
    img = py5.get(0, 0, WIDTH, HEIGHT)
    img.save(img_path)


def tmp_path() -> Path:
    return Path(tempfile.mkdtemp())


def save_frame(tmp_path, img_name, frame) -> Path:
    path = tmp_path / f"{img_name}_{frame:03d}.tga"
    py5.save_frame(path)
    return path


def save_gif(img_name, frames, duration: int = 200, loop=0):
    folder = Path(__file__).parent.resolve()
    img_folder = folder / "Images"
    img_path = img_folder / f"{img_name}.gif"
    images = [Image.open(frame) for frame in frames]
    kw = {
        "save_all": True,
        "append_images": images[1:],
        "duration": duration,
        "optimize": True,
    }
    if loop is not None:
        kw["loop"] = loop
    images[0].save(img_path, **kw)


class Celula:
    """
    nova = Celula(x, y, largura, [func_desenho0, func_desenho1, ...])
    .desenha()    desenha celula na sua posição
    .gira()       gira 90 graus
    .sob_mouse()  True ou False se o mouse está sobre a célula
    .espelha()    Inverte espelhamento
    .muda_desenho()   Muda função de desenho para a próxima
    .espelhada    Estado atual de espelhamento
    .rot          Rotação atual
    .func_ativa   Índice da função de desenho atual
    """

    def __init__(self, x, y, largura, funcs, cores):
        self.x, self.y = x, y
        self.largura = largura
        self.funcs = funcs
        self.func_ativa = choice(range(0, len(funcs)))
        self.rot = choice(range(0, 360, 90))
        self.espelhada = False
        self.cores = cores
        self.cor = choice(self.cores)

    def desenha(self):
        with py5.push_matrix():
            py5.translate(self.x, self.y)
            if self.espelhada:
                py5.scale(-1, 1)
            py5.rotate(py5.radians(self.rot))
            funcao_desenho = self.funcs[self.func_ativa]
            funcao_desenho(0, 0, self.largura, self.cor)

    def sob_mouse(self, x, y):
        return (
            self.x - self.largura / 2 < x < self.x + self.largura / 2
            and self.y - self.largura / 2 < y < self.y + self.largura / 2
        )

    def gira(self, rot=90):
        self.rot = self.rot + rot if self.rot < 360 else rot

    def muda_cor(self):
        self.cor = choice(self.cores)

    def muda_desenho(self, i=None):
        self.func_ativa = (self.func_ativa + 1) % len(self.funcs) if i is None else i

    def espelha(self):
        self.espelhada = not self.espelhada
