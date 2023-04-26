"""2023-04-25"""
from helpers import HEIGHT
from helpers import save_image
from helpers import WIDTH
from helpers import write_legend
from pathlib import Path

import py5


IMG_NAME = Path(__file__).name.replace(".py", "")


def settings():
    py5.size(WIDTH, HEIGHT)


def setup():
    background()
    py5.color_mode(py5.HSB, 300)
    circles()
    write_legend(["#FFFFFF"], IMG_NAME)
    save_image(IMG_NAME, "png")


def background():
    py5.background(0)


def circles():
    py5.no_fill()
    rotacoes = 3
    diametro = 600
    raio = diametro / 2
    diff_raio = 22
    raio_1 = raio - diff_raio
    mr_1 = raio_1 / 2
    with py5.push_matrix():
        py5.translate(py5.width / 2, py5.height / 2)
        py5.stroke(200, 200, 100)
        py5.fill(200, 200, 100, 100)
        py5.circle(0, 0, diametro)
        for _ in range(0, rotacoes):
            angulo = 360 // rotacoes
            py5.rotate(py5.radians(angulo))
            py5.stroke(100, 100, 100)
            # Draw arc
            py5.ellipse_mode(py5.CENTER)
            py5.fill(100, 100, 100, 100)
            py5.arc(
                0,
                -raio,
                diametro,
                diametro,
                py5.radians(30),
                py5.radians(150),
            )
            # Draw ellipse
            py5.ellipse_mode(py5.CORNERS)
            py5.stroke(200, 100, 100)
            py5.fill(200, 100, 100, 100)
            py5.ellipse(-mr_1, -raio, mr_1, -diff_raio)
            # Draw circles
            py5.stroke(300, 100, 100)
            py5.fill(300, 100, 100, 100)
            py5.ellipse(
                -raio / 3 / 2,
                -diff_raio - raio / 3,
                raio / 3 / 2,
                -diff_raio - 2 * raio / 3,
            )
            py5.ellipse(-raio / 3 / 2, -diff_raio, raio / 3 / 2, -diff_raio - raio / 3)
            py5.ellipse(-mr_1 / 2, -raio, mr_1 / 2, -diff_raio - 1.5 * raio / 3)
            # Draw line
            py5.stroke(200, 100, 100)
            py5.line(0, -raio - 100, 0, raio + 100)


py5.run_sketch()
