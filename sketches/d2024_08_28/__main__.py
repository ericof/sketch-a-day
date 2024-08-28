"""2024-08-28
Colisões 2
Exercício utilizando pymunk e colisões entre partículas e os limites do sketch
png
Sketch,py5,CreativeCoding
"""

from collections import deque

import py5
import pymunk

from utils import helpers

space = pymunk.Space()
space.gravity = (0, 9)


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
]

PARTICULAS = None
MAX_LEN = 350
LIMITES = []
PONTOS = []

sketch = helpers.info_for_sketch(__file__, __doc__)


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


def adiciona_rastro(space, pos, raio, posicoes):
    limite = pymunk.Segment(space.static_body, pos, pos, raio)
    limite.elasticity = 0.0
    limite.friction = 0.95
    space.add(limite)
    if len(posicoes) == MAX_LEN:
        space.remove(posicoes[0][1])
    posicoes.append((pos, limite))


def cria_limites(space):
    for inicio, final in POSICAO_MURO:
        limite = pymunk.Segment(space.static_body, inicio, final, 20)
        limite.elasticity = 0.0
        limite.friction = 0.95
        space.add(limite)
        LIMITES.append((inicio, final))


def setup():
    global PARTICULAS
    py5.size(helpers.LARGURA, helpers.ALTURA, py5.P3D)
    py5.color_mode(py5.HSB, 360, 100, 100)
    PARTICULAS = {}
    cria_limites(space)
    s = 80
    b = 80
    i = 0
    meio = py5.width // 2
    x0 = meio + 10
    x1 = meio - 10
    pontos = [
        (
            (x0 if idx % 2 else x1) + ((1 if idx % 2 else -1) * diff),
            py5.height - MARGEM_INTERNA,
            (1 if idx % 2 else -1) * py5.random_int(800, 1200),
            py5.random_int(-2000, -800),
        )
        for idx, diff in enumerate(range(0, 250, 5))
    ]
    for idx, (x0, y0, impulso_x, impulso_y) in enumerate(pontos):
        key = f"particula_{i:02d}"
        raio = 5
        massa = raio * py5.random_int(3, 5)
        h = py5.random_int(0, 30) + (idx % 2 * 180)
        cor = (h, s, b)
        particula = cria_particula(space, x0, y0, raio=raio, massa=massa, cor=cor)
        particula.body.apply_impulse_at_local_point((impulso_x, impulso_y))
        PARTICULAS[key] = {"particula": particula, "posicoes": deque(maxlen=MAX_LEN)}
        i += 1


def draw():
    py5.background(0)
    with py5.push_style():
        for (x0, y0), (xf, yf) in LIMITES:
            py5.stroke(200, 0, 100)
            py5.stroke_weight(4)
            py5.line(x0, y0, xf, yf)
    for particula in PARTICULAS.values():
        p = particula["particula"]
        pos = (p.body.position.x, p.body.position.y)
        posicoes = particula["posicoes"]
        adiciona_rastro(space, pos, p.radius, posicoes)
        h, s, b = p._color
        cor = py5.color(h, s, b)
        py5.stroke(cor)
        py5.stroke_weight(p.radius * 0.1)
        total = len(posicoes)
        for idx, rastro in enumerate(posicoes):
            mult = idx / total
            py5.stroke_weight(p.radius * mult)
            (x, y), _ = rastro
            if idx == total - 1:
                py5.circle(x, y, p.radius)
            elif not idx:
                py5.point(x, y)
            else:
                cor = py5.color(h, s, b)
                py5.stroke(cor)
                x0, y0 = particula["posicoes"][idx - 1][0]
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
