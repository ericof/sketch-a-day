"""2026-10-27
Esfera 01
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
PONTOS = 800
BAGUNCA_MAX = 1.5
BAGUNCA_MIN = 1.2


def inicializa():
    global esfera
    esfera = []
    for x, y, z in pontos_esfera(RAIO, PONTOS):
        h = int(py5.remap(x, -RAIO, RAIO, 0, 360))
        s = int(py5.remap(x, -RAIO, RAIO, 50, 100))
        b = int(py5.remap(x, -RAIO, RAIO, 50, 100))
        traco = py5.random_int(1, 4)
        cor = py5.color(h, s, b)
        bagunca_x, bagunca_y, bagunca_z = (
            py5.random(BAGUNCA_MIN, BAGUNCA_MAX),
            py5.random(BAGUNCA_MIN, BAGUNCA_MAX),
            py5.random(BAGUNCA_MIN, BAGUNCA_MAX),
        )
        x0, y0, z0 = x / bagunca_x, y / bagunca_y, z / bagunca_z
        esfera.append(((x, y, z), (x0, y0, z0), traco, cor))


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
        for (x, y, z), (x0, y0, z0), traco, cor in esfera:
            py5.stroke(cor)
            py5.stroke_weight(traco)
            py5.line(x, y, z, x0, y0, z0)
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
