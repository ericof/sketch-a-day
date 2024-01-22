"""2024-01-22
Genuary 22 - Point - line - plane.
Animação da transformação de um ponto em uma linha, em um plano.
gif
Sketch,py5,CreativeCoding,genuary,genuary22
"""
import numpy as np
import py5
import py5_tools

from utils import helpers

sketch = helpers.info_for_sketch(__file__, __doc__)

POSICOES = []
QUADRADO = None


def setup():
    global QUADRADO
    py5.size(helpers.LARGURA, helpers.ALTURA, py5.P3D)
    py5.color_mode(py5.HSB, 360, 100, 100)
    lado = 200
    meio_lado = lado / 2
    xb = helpers.LARGURA / 4
    x0 = xb - meio_lado
    x1 = xb + meio_lado
    yb = (helpers.ALTURA / 4) * 3
    y0 = yb - meio_lado
    y1 = yb + meio_lado
    POSICOES.extend([(x1, y) for y in np.linspace(y1, y0, num=lado, endpoint=True)])
    POSICOES.extend([(x, y0) for x in np.linspace(x1, x0, num=lado, endpoint=True)])
    POSICOES.extend([(x0, y) for y in np.linspace(y0, y1, num=lado, endpoint=True)])
    POSICOES.extend(
        [(x0, y, x1, y) for y in np.linspace(y0, y1, num=lado, endpoint=True)]
    )
    QUADRADO = (x0, y0, x1, y1)


def draw():
    py5.background(0)
    frame = py5.frame_count
    total = len(POSICOES)
    idx = total - 1
    angulo = 45
    incompleto = frame <= total
    if incompleto:
        idx = (frame % total) - 1
        angulo = py5.remap(idx, 0, total, 0, angulo)
    py5.stroke_weight(5)
    with py5.push_matrix():
        py5.rotate_x(py5.radians(angulo))
        py5.rotate_z(py5.radians(-(angulo / 2)))
        for i in range(0, idx):
            pos = POSICOES[i]
            s, h = pos[:2]
            h = py5.remap(h, 200, 600, 120, 240)
            s = py5.remap(h, 200, 600, 80, 100)
            py5.stroke(py5.color(h, s, 100))
            func = py5.line if len(pos) == 4 else py5.point
            func(*pos)
    helpers.write_legend(sketch=sketch)


def key_pressed():
    key = py5.key
    if key == " ":
        save_and_close()


def save_and_close():
    py5.no_loop()
    py5.exit_sketch()


if __name__ == "__main__":
    py5_tools.animated_gif(
        f"{sketch.path}/{sketch.day}.gif",
        count=140,
        period=0.1,
        duration=0.01,
        block=False,
    )
    py5.run_sketch()
