"""2025-04-20
Juventus' is 101
Uma ode ao meu time do coração.
png
Sketch,py5,CreativeCoding
"""

from pathlib import Path
from random import shuffle

import numpy as np
import py5

from utils import helpers
from utils.draw import rgb_to_hsb

sketch = helpers.info_for_sketch(__file__, __doc__)


TAM_PIXEL = 6


def pixelar(img_array: np.array, tam_pixel: int = 24, func=np.median):
    pontos = []
    # py5.no_stroke()
    for idx, x in enumerate(range(0, helpers.LARGURA, tam_pixel)):
        for idy, y in enumerate(range(0, helpers.ALTURA, tam_pixel)):
            bloco = img_array[y : y + tam_pixel, x : x + tam_pixel]
            cor = func(bloco, axis=(0, 1))
            h, s, b = rgb_to_hsb(cor[0], cor[1], cor[2])
            pontos.append((idx, idy, x, y, (h, s, b)))
    return pontos


def calcula_raio(centro: int, idx: int, idy: int) -> float:
    banda = centro * 0.5
    base = 0.2
    mult = 1 / base
    dx = idx - centro
    dy = idy - centro
    distancia = dx**2 + dy**2
    valor = np.exp(-distancia / (mult * banda**2))
    return base + (1 - base) * valor


def desenha_frases(largura: int, altura: int, fonte: int = 32) -> py5.Py5Graphics:
    frases = [
        "1924 - 2025",
        "Ou Juve ou nada",
        "Mooca é Mooca",
        "Moleque travesso",
        "Rumo a Tóquio",
        "Rua Javari",
    ]
    altura_linha = fonte * 1.2
    y = py5.random_gaussian(-20, 5)
    pg = py5.create_graphics(largura, altura, py5.P3D)
    pg.color_mode(py5.RGB)
    pg.text_size(fonte)
    pg.text_mode(py5.SHAPE)
    pg.fill(py5.color(112, 19, 56))
    with pg.begin_draw():
        while y < altura:
            shuffle(frases)
            x = py5.random_gaussian(-20, 5)
            frase = " - ".join(frases)
            frase = f"{frase} - "
            while x < largura:
                largura_texto = py5.text_width(frase)
                py5.text(frase, x, y)
                x += largura_texto
            y += altura_linha
    return pg


def setup():
    py5.size(helpers.LARGURA, helpers.ALTURA, py5.P3D)
    py5.background(0)
    py5.color_mode(py5.HSB, 360, 100, 100)
    largura = 800
    altura = 800
    path = Path(__file__).parent / "juventus.png"
    img_array = helpers.image_as_array(path)
    pontos = pixelar(img_array, TAM_PIXEL, np.average)
    py5.no_stroke()
    centro = (py5.width / TAM_PIXEL) / 2
    with py5.push():
        py5.translate(-py5.width, -py5.height, -altura)
        largura_g = py5.width * 3
        altura_g = py5.height * 3
        imagem = desenha_frases(largura_g, altura_g, 16)
        py5.image(imagem, 0, 0)
    with py5.push():
        py5.translate(py5.width // 2, py5.height // 2, -altura / 3)
        py5.lights()
        py5.light_specular(0, 150, 300)
        py5.specular(100, 100, 100)
        for idx, idy, xb, yb, cor in pontos:
            x = idx * TAM_PIXEL * 2 - largura
            y = idy * TAM_PIXEL * 2 - altura
            raio = calcula_raio(centro, idx, idy)
            z = -((1 - raio) * 1000)
            with py5.push():
                py5.translate(x, y, z)
                py5.fill(*cor)
                py5.sphere(TAM_PIXEL * raio)

    helpers.write_legend(sketch=sketch, frame="#000", cor="#FFF")


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
