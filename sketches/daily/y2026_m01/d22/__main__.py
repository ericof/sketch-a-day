"""2026-01-22
Tiles 07
Desenho de uma grade de formas que se transformam ciclicamente.
ericof.com|https://openprocessing.org/sketch/1995082
png
Sketch,py5,CreativeCoding
"""

from random import shuffle
from sketches.utils.draw import canvas
from sketches.utils.draw.cores.paletas import gera_paleta
from sketches.utils.draw.cores.paletas import lista_paletas
from sketches.utils.draw.grade import cria_grade
from sketches.utils.helpers import sketches as helpers

import py5
import py5_tools


sketch = helpers.info_for_sketch(__file__, __doc__)

COLUNAS = 20
LINHAS = COLUNAS
D_RANDOM = (0.4, 0.95)
T1 = 30
OFF_FACTOR = 0.1
CRR_FACTOR = 0.75
cor_fundo = py5.color(0)


def ease_in_out_expo(x: float) -> float:
    if x < 0.5:
        return (2 ** (20 * x - 10)) / 2
    return (2 - (2 ** (-20 * x + 10))) / 2


def seleciona_cores(paleta: list[int], total: int = 4) -> list[int]:
    """Gera lista com seleção de cores."""
    tmp = paleta[:]
    shuffle(tmp)
    return [py5.color(t) for t in tmp[:total]]


class Objeto:
    x: float
    y: float
    w: float
    cols: list[int]
    cx: float
    cy: float

    def __init__(self, x: float, y: float, w: float, paleta: list[int]):
        self.x = x
        self.y = y
        self.w = w

        self.cx = x
        self.cy = y

        self.cols = seleciona_cores(paleta, 4)

        self.t1 = T1
        self.pdrc = None

        self.inicializa()

    def inicializa(self):
        drc = py5.random_int(0, 4)
        while self.pdrc is not None and drc == self.pdrc:
            drc = py5.random_int(0, 4)
        self.drc = drc
        self.pdrc = drc

        self.d = self.w * py5.random(*D_RANDOM)

        # choose target corner or center
        if self.drc == 0:
            self.cx1 = self.x + ((self.w / 2) - (self.d / 2))
            self.cy1 = self.y + ((self.w / 2) - (self.d / 2))
        elif self.drc == 1:
            self.cx1 = self.x - ((self.w / 2) - (self.d / 2))
            self.cy1 = self.y + ((self.w / 2) - (self.d / 2))
        elif self.drc == 2:
            self.cx1 = self.x + ((self.w / 2) - (self.d / 2))
            self.cy1 = self.y - ((self.w / 2) - (self.d / 2))
        elif self.drc == 3:
            self.cx1 = self.x - ((self.w / 2) - (self.d / 2))
            self.cy1 = self.y - ((self.w / 2) - (self.d / 2))
        else:  # 4
            self.cx1 = self.x
            self.cy1 = self.y

        self.cx0 = self.cx
        self.cy0 = self.cy
        self.t = 0

    def show(self):
        py5.no_stroke()
        xx = self.x - (self.w / 2)
        yy = self.y - (self.w / 2)

        ww = self.cx - xx
        hh = self.cy - yy

        off = self.w * OFF_FACTOR
        crr = self.w * CRR_FACTOR

        # top-left
        py5.fill(self.cols[0])
        py5.rect(xx + (off / 2), yy + (off / 2), ww - off, hh - off, crr)

        # top-right
        py5.fill(self.cols[1])
        py5.rect(xx + ww + (off / 2), yy + (off / 2), self.w - ww - off, hh - off, crr)

        # bottom-right
        py5.fill(self.cols[2])
        py5.rect(
            self.cx + (off / 2),
            self.cy + (off / 2),
            self.w - ww - off,
            self.w - hh - off,
            crr,
        )

        # bottom-left
        py5.fill(self.cols[3])
        py5.rect(xx + (off / 2), yy + hh + (off / 2), ww - off, self.w - hh - off, crr)

    def move(self):
        if 0 < self.t < self.t1:
            n = py5.norm(self.t, 0, self.t1)
            e = ease_in_out_expo(n)
            self.cx = float(py5.lerp(self.cx0, self.cx1, e))
            self.cy = float(py5.lerp(self.cy0, self.cy1, e))

        if self.t > self.t1:
            self.inicializa()
        self.t += 1

    def run(self):
        self.show()
        self.move()


objetos: list[Objeto] = []


def setup():
    py5.size(*helpers.DIMENSOES.external, py5.P3D)
    largura, altura = helpers.DIMENSOES.external
    celula_x = largura // COLUNAS
    celula_y = altura // LINHAS
    grade = cria_grade(largura, altura, 0, 0, celula_x, celula_y, False)
    diff_x, diff_y = (
        helpers.DIMENSOES.external[0] / 2,
        helpers.DIMENSOES.external[1] / 2,
    )
    m_x = celula_x / 2
    m_y = celula_y / 2
    todas_paletas = lista_paletas()
    shuffle(todas_paletas)
    nomes: list[str] = [py5.random_choice(todas_paletas) for _ in range(COLUNAS)]
    paletas: list[list[int | str]] = [gera_paleta(nome, False) for nome in nomes]
    for xb, yb in grade:
        x, y = xb + m_x - diff_x, yb + m_y - diff_y
        paleta = py5.random_choice(paletas)
        while len(paleta) <= 4:
            paleta = py5.random_choice(paletas)
        objetos.append(Objeto(x, y, celula_x, paleta))


def draw():
    frame = py5.frame_count
    z = -200 + (frame // 2)
    py5.background(cor_fundo)
    with py5.push():
        py5.translate(*helpers.DIMENSOES.centro, z)
        py5.rotate(py5.radians(-45))
        for objeto in objetos:
            objeto.run()
    # Credits and go
    canvas.sketch_frame(
        sketch, cor_fundo, "large_transparent_white", "transparent_white"
    )


def key_pressed():
    key = py5.key
    if key == " ":
        save_and_close()


def save_and_close():
    py5.no_loop()
    canvas.save_sketch_image(sketch)
    py5.exit_sketch()


if __name__ == "__main__":
    img_path = sketch.path / f"{sketch.day}.gif"
    py5_tools.animated_gif(str(img_path), count=60, period=0.1, duration=0.1)
    py5.run_sketch()
