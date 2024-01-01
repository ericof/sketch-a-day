"""2024-01-01
Genuary 01 - Particulas em uma caixa.
Imagem de particulas de diversas cores em uma caixa.
png
Sketch,py5,CreativeCoding,genuary,genuary1
"""
from itertools import product
from random import choice

import py5
import pymunk

from utils import helpers

space = pymunk.Space()
space.gravity = (0, 10)


MARGEM = 100
MARGEM_INTERNA = int(MARGEM * 1.1)

POSICAO_MURO = [
    ((MARGEM, MARGEM), (helpers.LARGURA - MARGEM, MARGEM)),
    (
        (helpers.LARGURA - MARGEM, MARGEM),
        (helpers.LARGURA - MARGEM, helpers.ALTURA - MARGEM),
    ),
    (
        (helpers.LARGURA - MARGEM, helpers.ALTURA - MARGEM),
        (MARGEM, helpers.ALTURA - MARGEM),
    ),
    ((MARGEM, helpers.ALTURA - MARGEM), (MARGEM, MARGEM)),
]

PARTICULAS = None

LIMITES = []

ESPECIAL = None

sketch = helpers.info_for_sketch(__file__, __doc__)


def cria_limites(space):
    for inicio, final in POSICAO_MURO:
        limite = pymunk.Segment(space.static_body, inicio, final, 20)
        limite.elasticity = 0.95
        limite.friction = 0.7
        space.add(limite)
        LIMITES.append(limite)


def cria_particula(space, x0, y0, raio, massa, cor) -> pymunk.Circle:
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
    global ESPECIAL, PARTICULAS
    py5.size(helpers.LARGURA, helpers.ALTURA, py5.P3D)
    py5.color_mode(py5.HSB, 360, 100, 100)
    PARTICULAS = {}
    cria_limites(space)
    s = 80
    b = 80
    i = 0
    passo = 30
    x0_range = range(MARGEM_INTERNA, helpers.LARGURA - MARGEM_INTERNA, passo)
    y0_range = range(MARGEM_INTERNA, helpers.LARGURA - MARGEM_INTERNA, passo)
    pontos = list(product(x0_range, y0_range))
    especial = choice(range(0, len(pontos)))
    for x0, y0 in pontos:
        key = f"particula_{i:02d}"
        raio = py5.random_int(1, 8)
        massa = raio * py5.random_int(3, 5)
        h = y0 % 180 + 10
        if i == especial:
            raio = 15
            massa = 40
            h = 0
            ESPECIAL = key
        cor = py5.color(h, s, b)
        particula = cria_particula(space, x0, y0, raio=raio, massa=massa, cor=cor)
        PARTICULAS[key] = particula
        i += 1


def draw():
    py5.background(0)
    # Rendering visual representations of our new bodies
    py5.stroke(py5.color(180, 100, 100))
    py5.stroke_weight(20)
    for muro in LIMITES:
        py5.line(muro.a.x, muro.a.y, muro.b.x, muro.b.y)

    py5.no_stroke()
    for particula in PARTICULAS.values():
        py5.fill(particula._color)
        py5.circle(
            particula.body.position.x, particula.body.position.y, particula.radius * 2
        )

    # Avança a simulação
    space.step(1 / py5.get_frame_rate())
    helpers.write_legend(sketch=sketch)


def mouse_pressed():
    incremento = 50000
    particula = PARTICULAS[ESPECIAL]
    particula_f = py5.Py5Vector(0, 0)
    if py5.mouse_x > particula.body.position.x:
        # If the mouse is to the right of the ball, let's push it left
        particula_f.x = -incremento
    if py5.mouse_x < particula.body.position.x:
        # Otherwise, let's push it right
        particula_f.x = incremento

    if py5.mouse_y > particula.body.position.y:
        # If the mouse is below the ball, let's push it up
        particula_f.y = -incremento
    if py5.mouse_y < particula.body.position.y:
        # Otherwise, let's push it down
        particula_f.y = incremento

    particula.body.apply_impulse_at_world_point(
        (particula_f.x, particula_f.y), (py5.mouse_x, py5.mouse_y)
    )


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
