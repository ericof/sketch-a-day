"""2024-05-20
Redemoinho
Torção de uma grade com círculos em cada uma de suas células.
png
Sketch,py5,CreativeCoding,abav
"""

from random import choice

import numpy as np
import py5

from utils import helpers

sketch = helpers.info_for_sketch(__file__, __doc__)

PATH = helpers.tmp_path()

FRAMES = []

LIMITE_FRAMES = 160

GRADE = []
QUADRADO = 80

CORES = [
    (0, 0, 0),
    (127, 143, 110),
    (179, 176, 133),
    (200, 200, 200),
    (212, 198, 170),
    (218, 211, 189),
    (90, 119, 168),
    (187, 137, 30),
    (30, 30, 30),
    (40, 50, 60),
]

POS = [
    (0, 0),
    (0, QUADRADO),
    (QUADRADO / 2, QUADRADO / 2),
    (QUADRADO / 2, 0),
    (0, QUADRADO / 2),
    (QUADRADO / 2, QUADRADO),
    (QUADRADO, QUADRADO / 2),
    (QUADRADO, QUADRADO),
    (QUADRADO, 0),
]


def faixa(img_array: np.array, x0: int, x1: int):
    resultado = img_array[0 : py5.height, x0:x1]
    return resultado


def setup():
    global PG, pixels_por_frame
    py5.size(helpers.LARGURA, helpers.ALTURA, py5.P3D)
    pixels_por_frame = py5.width / LIMITE_FRAMES
    for idy, y in enumerate(range(-300, 300, 100), 1):
        for idx, x in enumerate(range(-300, 300, 100), 1):
            pg = py5.create_graphics(QUADRADO, QUADRADO)
            fundo = (52 + idx, 140 + idx + idy, 89 + idy)
            num_circulos = py5.random_int(3, 5)
            circulos = []
            for _ in range(num_circulos):
                pos = choice(POS)
                tamanho = py5.random_int(2, 80)
                passo = py5.TWO_PI / py5.random_int(2, 40)
                cor = choice(CORES)
                circulos.append((pos, tamanho, cor))
            GRADE.append((pg, (x, y), (idx, idy), fundo, passo, circulos))


def draw():
    py5.background(248, 241, 219)
    f = py5.frame_count
    i = 0
    with py5.push_matrix():
        py5.translate(py5.width / 2, py5.height / 2)
        rotacao = py5.cos(py5.radians(f * 2) + i * 2) + py5.sin(
            py5.radians(f * 2) + i * 2
        )
        py5.rotate(rotacao)
        for pg, (x, y), (idx, idy), fundo, passo, circulos in GRADE:
            pg.begin_draw()
            pg.background(*fundo)
            for circulo in circulos:
                (xc, yc), d, cor = circulo
                s = py5.cos(py5.radians(f * 2) + i * passo)
                d += 80 * s + idx
                pg.fill(*cor)
                pg.circle(xc, yc, d)
            pg.end_draw()
            with py5.push_style():
                py5.fill("#000")
                py5.square(x - 2, y - 2, QUADRADO + 4)
            py5.image(pg, x, y)
        i += 1
    helpers.write_legend(sketch=sketch, frame="#000")
    if f % 2:
        FRAMES.append(helpers.save_frame(PATH, sketch.day, f))
    # Cada frame vai prover py5.width / LIMITE_FRAMES  pixels
    if len(FRAMES) == LIMITE_FRAMES:
        imagens = [helpers.image_as_array(frame) for frame in FRAMES]
        data = []
        for idx, frame_array in enumerate(imagens):
            x0 = int(idx * pixels_por_frame)
            x1 = int(x0 + pixels_por_frame)
            tmp = faixa(frame_array, x0, x1)
            data.append(tmp)
        new_image = np.concatenate(data, axis=1)
        imagem = py5.create_image_from_numpy(new_image, bands="RGB")
        img_path = sketch.path / f"{sketch.day}.{sketch.format}"
        imagem.save(img_path)
        save_and_close()


def key_pressed():
    key = py5.key
    if key == " ":
        save_and_close()


def save_and_close():
    py5.no_loop()
    py5.exit_sketch()


if __name__ == "__main__":
    py5.run_sketch()
