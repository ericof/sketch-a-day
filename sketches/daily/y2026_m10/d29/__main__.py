"""2026-10-29
Esfera 03
Execício de criação de esfera
ericof.com
png
Sketch,py5,CreativeCoding
"""

from sketches.utils.draw import canvas
from sketches.utils.draw.esfera import pontos_esfera
from sketches.utils.helpers import sketches as helpers

import py5


sketch = helpers.info_for_sketch(__file__, __doc__)

cor_fundo = py5.color(0)

RAIO = 300
PONTOS = 900
BAGUNCA_MAX = 1.9
BAGUNCA_MIN = 1.2
CURVA = 40
TRACO_MAX = 4
TRACO_MIN = 2
SEGMENTOS = 16
DIST_MIN = RAIO / BAGUNCA_MAX
DIST_MAX = RAIO


def ponto_controle(p, p0, t):
    """Ponto entre ``p`` e ``p0`` na fração ``t``, deslocado ao acaso."""
    return tuple(
        py5.lerp(a, b, t) + py5.random(-CURVA, CURVA)
        for a, b in zip(p, p0, strict=True)
    )


def cor_distancia(x, y, z):
    """Cor quente perto do centro, clara longe dele."""
    distancia = py5.dist(0, 0, 0, x, y, z)
    t = py5.constrain(py5.norm(distancia, DIST_MIN, DIST_MAX), 0, 1)
    h = int(py5.lerp(90, 180, t))
    s = int(py5.lerp(100, 15, t))
    b = int(py5.lerp(90, 100, t))
    return py5.color(h, s, b)


def vertices_curva(curva):
    """Pontos da Bézier, cada um com a cor da sua distância ao centro."""
    xs, ys, zs = curva[0::3], curva[1::3], curva[2::3]
    vertices = []
    for i in range(SEGMENTOS + 1):
        t = i / SEGMENTOS
        ponto = tuple(py5.bezier_point(a, b, c, d, t) for a, b, c, d in (xs, ys, zs))
        vertices.append((ponto, cor_distancia(*ponto)))
    return vertices


def inicializa():
    global esfera
    esfera = []
    for x, y, z in pontos_esfera(RAIO, PONTOS):
        traco = py5.random_int(TRACO_MIN, TRACO_MAX)
        bagunca_x, bagunca_y, bagunca_z = (
            py5.random(BAGUNCA_MIN, BAGUNCA_MAX),
            py5.random(BAGUNCA_MIN, BAGUNCA_MAX),
            py5.random(BAGUNCA_MIN, BAGUNCA_MAX),
        )
        p = (x, y, z)
        p0 = (x / bagunca_x, y / bagunca_y, z / bagunca_z)
        c1 = ponto_controle(p, p0, 1 / 3)
        c2 = ponto_controle(p, p0, 2 / 3)
        curva = (*p, *c1, *c2, *p0)
        esfera.append((vertices_curva(curva), traco))


def setup():
    py5.size(*helpers.DIMENSOES.external, py5.P3D)
    py5.color_mode(py5.HSB, 360, 100, 100)
    inicializa()


def draw():
    py5.background(cor_fundo)
    frame = py5.frame_count
    radianos = float(py5.radians(frame))
    with py5.push():
        py5.translate(*helpers.DIMENSOES.centro, 0)
        py5.rotate_y(radianos)
        py5.rotate_z(radianos)
        py5.stroke_weight(3)
        py5.no_fill()
        for vertices, traco in esfera:
            py5.stroke_weight(traco)
            with py5.begin_shape():
                for ponto, cor in vertices:
                    py5.stroke(cor)
                    py5.vertex(*ponto)
    # Credits and go
    canvas.sketch_frame(
        sketch,
        cor_fundo,
        "large_transparent_white",
        "transparent_white",
        version=2,
    )


def key_pressed():
    key = py5.key
    if key == " ":
        save_and_close()
    elif key == "r":
        inicializa()


def save_and_close():
    py5.no_loop()
    canvas.save_sketch_image(sketch)
    py5.exit_sketch()


if __name__ == "__main__":
    py5.run_sketch()
