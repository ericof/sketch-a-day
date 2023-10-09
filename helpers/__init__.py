from collections import UserList
from dataclasses import dataclass
from PIL import Image
from pathlib import Path
from random import choice
from typing import Any
from typing import List

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
    img = py5.get_pixels(0, 0, WIDTH, HEIGHT)
    img.save(img_path)


def tmp_path() -> Path:
    return Path(tempfile.mkdtemp())


def save_frame(tmp_path, img_name, frame) -> Path:
    path = tmp_path / f"{img_name}_{frame:03d}.tga"
    py5.save_frame(path)
    return path


def save_gif(img_name, frames, duration: float = 200, loop=0):
    folder = Path(__file__).parent.parent.resolve()
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


class BaseCelula:
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


class Celula(BaseCelula):
    def desenha(self):
        with py5.push_matrix():
            py5.translate(self.x, self.y)
            if self.espelhada:
                py5.scale(-1, 1)
            py5.rotate(py5.radians(self.rot))
            funcao_desenho = self.funcs[self.func_ativa]
            funcao_desenho(0, 0, self.largura, self.cor)


class CelulaV2(BaseCelula):
    def __init__(self, x, y, largura, formas, cores):
        self.x, self.y = x, y
        self.largura = largura
        self.largura_interna = largura * 0.9
        self.formas = formas
        self.forma_ativa = choice(formas)
        self.rot = choice(range(0, 360, 90))
        self.espelhada = False
        self.cores = cores
        self.cor = choice(self.cores)

    def desenha(self):
        largura = self.largura_interna
        py5.shape_mode = py5.CENTER
        forma = self.forma_ativa
        forma.set_fill(self.cor)
        forma.set_stroke(self.cor)
        forma.rotate(py5.radians(self.rot))
        if self.espelhada:
            forma.scale(-1, 1)
        py5.shape(forma, self.x, self.y, largura, largura)


class CelulaV3(CelulaV2):
    def __init__(self, x, y, largura, formas, cores, border: bool = False):
        super().__init__(x, y, largura, formas, cores)
        self.espelhada = choice([True, False])
        self.rot = 0
        self.border = border

    def desenha(self):
        with py5.push_matrix():
            py5.translate(self.x, self.y)
            largura = self.largura_interna
            if self.border:
                py5.no_fill()
                py5.stroke(self.cor)
                py5.square(0, 0, self.largura)
            buffer = (self.largura - self.largura_interna) / 2
            forma = self.forma_ativa
            forma.set_fill(self.cor)
            forma.set_stroke(self.cor)
            forma.rotate(py5.radians(self.rot))
            py5.shape_mode = py5.CORNER
            if self.espelhada:
                py5.shape(forma, buffer + largura, buffer, -largura, largura)
            else:
                py5.shape(forma, buffer, buffer, largura, largura)


class CelulaV4(CelulaV3):
    fill: bool = True
    stroke: bool = True

    def __init__(self, x, y, largura, formas, cores, border: bool = False):
        super().__init__(x, y, largura, formas, cores)
        self.largura_interna = self.largura * 0.95
        self.espelhada = False
        self.espelhada_vertical = False
        self.rot = 0
        self.border = border

    def desenha(self):
        with py5.push_matrix():
            py5.translate(self.x, self.y)
            largura = self.largura_interna
            if self.border:
                py5.no_fill()
                py5.stroke(self.cor)
                py5.square(0, 0, self.largura)
            buffer = (self.largura - self.largura_interna) / 2
            forma = self.forma_ativa
            cor = self.cor
            forma.set_fill(cor if self.fill else False)
            forma.set_stroke(cor if self.stroke else False)
            forma.rotate(py5.radians(self.rot))
            py5.shape_mode = py5.CORNER
            x, y, l_x, l_y = buffer, buffer, largura, largura
            if self.espelhada:
                x = buffer + largura
                l_x = -largura

            if self.espelhada_vertical:
                y = buffer + largura
                l_y = -largura
            py5.shape(forma, x, y, l_x, l_y)


@dataclass
class CelulaInfo:
    x: float
    y: float
    celulas: List[BaseCelula] = None


class Grade(UserList):
    data: List[CelulaInfo]

    def __init__(self, x, y, width, height, colunas, linhas, margem_x, margem_y):
        celulas = []
        largura = width - (margem_x * 2)
        altura = height - (margem_y * 2)
        x0 = x + margem_x
        y0 = y + margem_y
        passo_x = largura // colunas
        passo_y = altura // linhas
        for linha in range(linhas):
            cy = y0 + (linha * passo_y)
            for coluna in range(colunas):
                cx = x0 + (coluna * passo_x)
                celulas.append(CelulaInfo(cx, cy, []))
        self.data = celulas

    def desenha(self):
        for item in self.data:
            celulas = item.celulas
            for celula in celulas:
                celula.desenha()
