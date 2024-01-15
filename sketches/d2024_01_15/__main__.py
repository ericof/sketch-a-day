"""2024-01-15
Genuary 15 - Use a physics library.
Dança de duas partículas conectadas como um pêndulo (feito com pymunk).
gif
Sketch,py5,CreativeCoding,genuary,genuary15
"""
from collections import deque

import py5
import py5_tools
import pymunk

from utils import helpers

sketch = helpers.info_for_sketch(__file__, __doc__)


space = pymunk.Space()
space.gravity = (0, 900)

BASE = space.static_body
PENDULO = []

PASSOS = 40
TRACOS = [
    deque(maxlen=PASSOS),
    deque(maxlen=PASSOS),
]


def junta(corpo1, corpo2, p1=(0, 0), p2=(0, 0)):
    junta = pymunk.constraints.PinJoint(corpo1, corpo2, p1, p2)
    space.add(junta)


def cria_circulo(posicao, raio, densidade=0.2) -> pymunk.Circle:
    body = pymunk.Body()
    body.position = posicao
    forma = pymunk.Circle(body, raio)
    forma.density = densidade
    forma.friction = 0.5
    forma.elasticity = 1
    space.add(body, forma)
    return forma


def setup():
    global PENDULO
    py5.size(helpers.LARGURA, helpers.ALTURA, py5.P3D)
    py5.color_mode(py5.HSB, 360, 100, 100)
    py5.stroke(255)
    py5.stroke_weight(2)
    # Cria Pendulo
    p1 = pymunk.Vec2d(400, 100)
    v1 = pymunk.Vec2d(100, 50)
    c1 = cria_circulo(p1 + v1, 30, densidade=4)
    junta(BASE, c1.body, p1)
    p2 = pymunk.Vec2d(200, 200)
    c2 = cria_circulo(p2, 20, densidade=2)
    junta(c1.body, c2.body)
    p3 = pymunk.Vec2d(300, 200)
    c3 = cria_circulo(p3, 20, densidade=0.1)
    junta(c2.body, c3.body)
    PENDULO = [c1, c2, c3]


def desenha_rastro(tracos: deque, hb: int, xf: int, yf: int):
    h = (len(tracos) / PASSOS) * 200 + hb
    s = 80
    x0, y0 = None, None
    for idx, (x, y) in enumerate(tracos):
        h = (idx / PASSOS) * 200 + hb
        b = (idx / PASSOS) * 100
        py5.stroke(py5.color(h, s, b))
        if not x0:
            py5.point(x, y)
        else:
            py5.line(x0, y0, x, y)
        x0, y0 = x, y
    tracos.append((xf, yf))
    b = 100
    py5.fill(py5.color(h, s, b))
    py5.circle(xf, yf, 4)


def draw():
    py5.background(360, 0, 0)
    c2 = PENDULO[-2]
    c3 = PENDULO[-1]
    for indice, c in enumerate((c2, c3)):
        xf, yf = c.body.position.x, c.body.position.y
        tracos = TRACOS[indice]
        hb = indice * 80
        desenha_rastro(tracos, hb, xf, yf)
        TRACOS[indice].append((xf, yf))

    space.step(1 / py5.get_frame_rate())
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
        count=240,
        period=0.1,
        duration=0.00,
        block=False,
    )
    py5.run_sketch()
