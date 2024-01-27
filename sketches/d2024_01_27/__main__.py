"""2024-01-27
Genuary 27 - Code for one hour. At the one hour mark, you are done.
Círculos concêntricos com 'espinhos' criados com py5.noise.
png
Sketch,py5,CreativeCoding,genuary,genuary27
"""
import numpy as np
import py5

from utils import helpers

sketch = helpers.info_for_sketch(__file__, __doc__)


def calcula_circulo(diametro):
    raio = diametro / 2
    n = int(raio)
    pontos = []
    for ponto in range(0, n + 1):
        passo = 2 * py5.PI / n * ponto
        x = np.cos(passo) * raio
        y = np.sin(passo) * raio
        noise = py5.noise(x, y)
        pontos.append((int(x), int(y), noise))
    return pontos


def popula_pontos():
    pontos = []
    step = 30
    diametro = 15
    while diametro < 720:
        pontos.append(calcula_circulo(diametro=diametro))
        if diametro % 180 == 0:
            step += 20
        diametro += step
    return pontos


def desenha_circulo(circulo, idx):
    z = -300 + (idx * 10)
    with py5.begin_shape():
        x0 = None
        y0 = None
        for x, y, noise in circulo:
            h = 240 - (idx * 10)
            s = abs(100 - (idx * 20))
            b = 100 * abs(noise)
            py5.fill(py5.color(h, s, b))
            py5.stroke(py5.color(h, s, b - 5))
            py5.vertex(x, y, z)
            if x0:
                py5.quadratic_vertex(x0, y0, z, x, y, z)
            x_noise = x + (noise * x / 4)
            y_noise = y + (noise * y / 3)
            py5.quadratic_vertex(x, y, z, x_noise, y_noise, z)
            x_noise_1 = x_noise + (noise * x / 8)
            y_noise_1 = y_noise + (noise * y / 5)
            py5.quadratic_vertex(x_noise, y_noise, z, x_noise_1, y_noise_1, z)
            x0 = x
            y0 = y


def setup():
    global PONTOS
    py5.size(helpers.LARGURA, helpers.ALTURA, py5.P3D)
    py5.color_mode(py5.HSB, 360, 100, 100)
    py5.frame_rate(1)
    PONTOS = popula_pontos()


def draw():
    py5.background(120, 0, 0)
    helpers.write_legend(sketch=sketch)
    with py5.push_matrix():
        py5.translate(py5.width / 2, py5.height / 2, 0)
        for idx, circulo in enumerate(PONTOS[::-1]):
            py5.translate(0, idx, idx * 1.6)
            py5.rotate_z(py5.radians(idx * 5))
            py5.rotate(py5.radians(py5.random_int(15, 60)))
            desenha_circulo(circulo, idx)


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
