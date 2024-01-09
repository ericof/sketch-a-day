"""2024-01-09
Genuary 09 - ASCII
Imagem do Monte Fuji e um Santuário formada por caracteres ASCII.
png
Sketch,py5,CreativeCoding,genuary,genuary9
"""
from pathlib import Path

import numpy as np
import py5
import pymunk

from utils import helpers

sketch = helpers.info_for_sketch(__file__, __doc__)

space = pymunk.Space()
space.gravity = (0, 20)


CHARS = (
    "  `.-':_,^=;><+!rc*/z?sLTv)J7(|Fi{C}fI31tlu[neoZ"
    "5Yxjya]2ESwqkP6h9d4VpOGbUAKXHm8RD#$Bg0MNWQ%&@"
)

BORDAS = None
LINHAS = []
RAIO = 4


def asciilate(img_array) -> list:
    pixel_chunk = RAIO
    pesos_rgb = [0.2989, 0.5870, 0.1140]
    img_array_cinza = np.dot(img_array[..., :3], pesos_rgb)
    py5.text_size(20)
    LINHAS = []
    py5.text_align(py5.CENTER)
    for y in range(0, helpers.ALTURA, pixel_chunk):
        line = []
        if y + pixel_chunk > helpers.ALTURA:
            pixel_chunk = helpers.ALTURA - y
        for x in range(0, helpers.LARGURA, pixel_chunk):
            block = img_array[y : y + pixel_chunk, x : x + pixel_chunk]
            avg_color = np.median(block, axis=(0, 1))
            cor = py5.color(avg_color[0], avg_color[1], avg_color[2], 100)
            block = img_array_cinza[y : y + pixel_chunk, x : x + pixel_chunk]
            avg_color = np.median(block, axis=(0, 1))
            char = int(py5.remap(avg_color, 0, 255, 0, len(CHARS)))
            line.append((x, y, CHARS[char], cor))
        LINHAS.append(line)
    return LINHAS


def cria_linha(space, raio, massa, linha, idy) -> pymunk.Poly:
    _linha = []
    for x, y, char, cor in linha:
        yf = y
        # Começar fora da tela
        y -= py5.height
        _linha.append((x, char, cor))
    largura = py5.width
    massa = massa * 1 / (idy * 2 + 1)
    inercia = pymunk.moment_for_box(massa, (largura, raio))
    body = pymunk.Body(massa, inercia)
    body.position = 0, y
    shape = pymunk.Poly.create_box(body, (largura, raio * 4))
    shape._linha = _linha
    shape._y = yf
    shape.elasticity = 0.0
    shape.friction = 1.0
    space.add(body, shape)
    return shape


def bordas(space, x: int, y: int):
    bordas = []
    # bordas
    x0 = -400
    xf = x + 400
    y0 = -2000
    yf = y + 100
    for inicio, final in (
        ((x0, yf), (xf, yf)),  # Chao
        ((x0, y0), (x0, yf)),  # esquerda
        ((xf, y0), (xf, yf)),  # direita
    ):
        limite = pymunk.Segment(space.static_body, inicio, final, 100)
        limite.elasticity = 0.0
        limite.friction = 1.0
        space.add(limite)
        bordas.append(limite)
    return bordas


def setup():
    global BORDAS
    global LINHAS
    py5.size(helpers.LARGURA, helpers.ALTURA, py5.P3D)
    py5.background(0)
    BORDAS = bordas(space, py5.width, py5.height)
    path = Path(__file__).parent / "fuji.jpg"
    img_array = helpers.image_as_array(path)
    linhas = asciilate(img_array)
    for idy, linha in enumerate(linhas[::-1]):
        LINHAS.append(cria_linha(space, RAIO, 10, linha, idy))
    helpers.write_legend(sketch=sketch)


def draw():
    py5.background(0)
    py5.text_size(20)
    py5.text_align(py5.CENTER)
    rate = py5.get_frame_rate()
    for idy, linha in enumerate(LINHAS):
        y = linha.body.position.y
        yf = linha._y
        if np.isnan(y) or int(y) >= yf:
            y = yf
            linha.body.moment = 0.0
        for x, char, cor in linha._linha:
            py5.fill(cor)
            py5.text(char, x, y)

    space.step(1 / rate)
    helpers.write_legend(sketch=sketch)


def key_pressed():
    key = py5.key
    if key == " ":
        save_and_close()


def save_and_close():
    py5.no_loop()
    helpers.save_sketch_image(sketch)
    py5.exit_sketch()


if __name__ == "__main__":
    py5.run_sketch()
