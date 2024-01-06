"""2024-01-06
Genuary 06 - Screensaver.
Inspirado no screensaver de DVDs, temos um círculo que rebate nas limites do sketch.
gif
Sketch,py5,CreativeCoding,genuary,genuary6
"""
from collections import deque

import py5
import py5_tools
import pymunk

from utils import helpers

sketch = helpers.info_for_sketch(__file__, __doc__)


space = pymunk.Space()
space.gravity = (0, 0)


POSICAO_MURO = [
    ((0, 0), (helpers.LARGURA, 0)),
    (
        (helpers.LARGURA, 0),
        (helpers.LARGURA, helpers.ALTURA),
    ),
    (
        (helpers.LARGURA, helpers.ALTURA),
        (0, helpers.ALTURA),
    ),
    ((0, helpers.ALTURA), (0, 0)),
]

HISTORICO = deque(maxlen=100)

LIMITES = []
ELEMENTO = None


def cria_limites(space):
    for inicio, final in POSICAO_MURO:
        limite = pymunk.Segment(space.static_body, inicio, final, 20)
        limite.elasticity = 0.95
        limite.friction = 0.7
        space.add(limite)
        LIMITES.append(limite)


def cria_elemento(space, x0, y0, raio, massa, cor) -> pymunk.Circle:
    inercia = pymunk.moment_for_circle(massa, 0, raio, (0, 0))
    body = pymunk.Body(massa, inercia)
    body.position = x0, y0
    shape = pymunk.Circle(body, raio, (0, 0))
    shape._color = cor
    shape.elasticity = 0.7
    shape.friction = 0.95
    space.add(body, shape)
    return shape


def setup():
    global ELEMENTO
    py5.size(helpers.LARGURA, helpers.ALTURA, py5.P3D)
    py5.background(0)
    py5.color_mode(py5.HSB, 360, 100, 100)
    cria_limites(space)
    cor = py5.color(180, 80, 80)
    ELEMENTO = cria_elemento(
        space, helpers.LARGURA // 2, helpers.ALTURA // 2, raio=70, massa=20, cor=cor
    )


def draw():
    global HISTORICO
    frame = py5.frame_count
    if frame % 300 == 1:
        vx = py5.random_int(3000, 5000) * py5.random_int(-1, 1)
        vy = py5.random_int(3000, 5000) * py5.random_int(-1, 1)
        vector = py5.Py5Vector(vx, vy)
        wx = py5.random_int(0, helpers.LARGURA)
        wy = py5.random_int(0, helpers.ALTURA)
        ELEMENTO.body.apply_impulse_at_world_point((vector.x, vector.y), (wx, wy))
    py5.background(0)

    py5.no_fill()
    HISTORICO.append((ELEMENTO.body.position.x, ELEMENTO.body.position.y))
    total = len(HISTORICO)
    for idx, (x, y) in enumerate(HISTORICO):
        cor = py5.color(idx * 3.6, idx, 80)
        py5.stroke(cor)
        if idx + 1 >= total:
            py5.fill(cor)
            raio = ELEMENTO.radius
        else:
            mult = (idx % 10) / 10
            raio = ELEMENTO.radius * mult
        py5.circle(x, y, raio)

    # Avança a simulação
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
        count=50,
        period=0.5,
        duration=0.00,
        block=False,
    )
    py5.run_sketch()
