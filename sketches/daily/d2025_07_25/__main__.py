"""2025-07-25
Circularis strepitus I
Criação de círculos com pontos baseados em ruído.
ericof.com|Inspirado em https://ericof.com/en/sketches/2023-05-25
png
Sketch,py5,CreativeCoding
"""

from sketches.utils.draw import canvas
from sketches.utils.helpers import sketches as helpers

import numpy as np
import opensimplex
import py5


sketch = helpers.info_for_sketch(__file__, __doc__)


def calcula_circulo_com_ruido(
    diametro: float, z: int
) -> list[tuple[int, int, int, float]]:
    """Calcula um círculo com pontos baseados em ruído."""
    raio = diametro / 2
    n = int(raio)
    pontos = []
    for ponto in range(0, n + 1):
        x = np.cos(2 * py5.PI / n * ponto) * raio
        y = np.sin(2 * py5.PI / n * ponto) * raio
        noise = opensimplex.noise2(x=x, y=y)
        pontos.append((int(x), int(y), int(z), noise))
    return pontos


def popula_pontos():
    pontos: list[list[tuple[int, int, int, float]]] = []
    step = 20
    diametro = 5
    z = 100
    while diametro < 720:
        pontos.append(calcula_circulo_com_ruido(diametro=diametro, z=z))
        if diametro % 180 == 0:
            step += 20
        diametro += step
        z -= 10
    return pontos


def desenha_circulo(circulo: list[tuple[int, int, int, float]], idx: int, hb: int = 80):
    with py5.begin_shape():
        x0 = None
        y0 = None
        for x, y, z, noise in circulo:
            h = hb - (idx * 3)
            s = 100
            b = 100 * abs(noise)
            cor = py5.color(h, s, b)
            py5.fill(cor)
            cor = py5.color(h, s, b * 0.90)
            py5.stroke(cor)
            py5.vertex(x, y, z)
            if x0 and y0:
                py5.quadratic_vertex(x0, y0, z, x, y, z)
            x_noise = x + (noise * x / 20)
            y_noise = y + (noise * y / 20)
            py5.quadratic_vertex(x, y, z, x_noise, y_noise, z)
            x_noise_1 = x_noise + (noise * x / 8)
            y_noise_1 = y_noise + (noise * y / 8)
            py5.quadratic_vertex(x_noise, y_noise, z, x_noise_1, y_noise_1, z)
            x0 = x
            y0 = y


PONTOS = popula_pontos()


def setup():
    py5.size(*helpers.DIMENSOES.external, py5.P3D)
    cor_fundo = py5.color(0)
    py5.background(cor_fundo)
    py5.color_mode(py5.HSB, 360, 100, 100)
    py5.frame_rate(5)


def draw():
    cor_fundo = py5.color(0)
    py5.background(cor_fundo)
    centro = (py5.width / 2, py5.height / 2)
    with py5.push():
        py5.translate(*centro, 250)
        for idx, circulo in enumerate(PONTOS[::-1]):
            angulo = float(py5.radians(py5.random_int(0, 360)))
            py5.rotate(angulo)
            hb = 120
            desenha_circulo(circulo, idx, hb)
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
    py5.run_sketch()
