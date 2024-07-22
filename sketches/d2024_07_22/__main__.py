"""2024-07-22
Colisões 2
Exercício utilizando pymunk e colisões com muros invisíveis
png
Sketch,py5,CreativeCoding
"""

from collections import deque

import py5
import pymunk

from utils import helpers

space = pymunk.Space()
space.gravity = (0, 0)


MARGEM = 100
MARGEM_INTERNA = int(MARGEM * 1.01)

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
    (
        (
            py5.random_int(MARGEM, helpers.LARGURA - MARGEM),
            py5.random_int(MARGEM, helpers.ALTURA - MARGEM),
        ),
        (
            py5.random_int(MARGEM, helpers.LARGURA - MARGEM),
            py5.random_int(MARGEM, helpers.ALTURA - MARGEM),
        ),
    ),
    (
        (
            py5.random_int(MARGEM, helpers.LARGURA - MARGEM),
            py5.random_int(MARGEM, helpers.ALTURA - MARGEM),
        ),
        (
            py5.random_int(MARGEM, helpers.LARGURA - MARGEM),
            py5.random_int(MARGEM, helpers.ALTURA - MARGEM),
        ),
    ),
]

PARTICULAS = None

LIMITES = []

sketch = helpers.info_for_sketch(__file__, __doc__)


def cria_particula(space, x0, y0, raio, massa, cor) -> pymunk.Circle:
    inercia = pymunk.moment_for_circle(massa, 0, raio, (0, 0))
    body = pymunk.Body(massa, inercia)
    body.position = x0, y0
    shape = pymunk.Circle(body, raio, (0, 0))
    shape._color = cor
    shape.elasticity = 0.6
    shape.friction = 0.95
    space.add(body, shape)
    return shape


def cria_limites(space):
    for inicio, final in POSICAO_MURO:
        limite = pymunk.Segment(space.static_body, inicio, final, 20)
        limite.elasticity = 0.6
        limite.friction = 0.95
        space.add(limite)
        LIMITES.append(limite)


def setup():
    global PARTICULAS
    py5.size(helpers.LARGURA, helpers.ALTURA, py5.P3D)
    py5.color_mode(py5.HSB, 360, 100, 100)
    PARTICULAS = {}
    cria_limites(space)
    s = 80
    b = 80
    i = 0
    pontos = [
        (
            py5.random_int(MARGEM_INTERNA, py5.width - MARGEM_INTERNA),
            py5.random_int(MARGEM_INTERNA, py5.height - MARGEM_INTERNA),
        )
        for _ in range(8)
    ]
    for x0, y0 in pontos:
        key = f"particula_{i:02d}"
        raio = py5.random_int(1, 8)
        massa = raio * py5.random_int(3, 5)
        h = y0 % 180 + 10
        cor = py5.color(h, s, b)
        particula = cria_particula(space, x0, y0, raio=raio, massa=massa, cor=cor)
        particula.body.apply_impulse_at_world_point(
            (particula.body.position.x, particula.body.position.y),
            (
                py5.random_int(-4000, 4000),
                py5.random_int(-4000, 4000),
            ),
        )
        PARTICULAS[key] = {"particula": particula, "posicoes": deque(maxlen=5000)}
        i += 1


def draw():
    py5.background(0)
    for particula in PARTICULAS.values():
        p = particula["particula"]
        particula["posicoes"].append((p.body.position.x, p.body.position.y))
        py5.stroke(p._color)
        py5.stroke_weight(p.radius)
        for idx, (x, y) in enumerate(particula["posicoes"]):
            if not idx:
                py5.point(x, y)
            else:
                x0, y0 = particula["posicoes"][idx - 1]
                py5.line(x0, y0, x, y)

    # Avança a simulação
    space.step(1 / py5.get_frame_rate())
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
