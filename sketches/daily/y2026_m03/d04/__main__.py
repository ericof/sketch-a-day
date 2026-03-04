"""2026-03-04
Divisões 01
Inspirado em sketch de Alexandre Villares
ericof.com|https://abav.lugaralgum.com/sketch-a-day/#sketch_2026_02_16
png
Sketch,py5,CreativeCoding
"""

from collections import deque
from shapely import Polygon
from sketches.utils.draw import canvas
from sketches.utils.draw.cores.paletas import gera_paleta
from sketches.utils.helpers import sketches as helpers

import numpy as np
import py5


sketch = helpers.info_for_sketch(__file__, __doc__)

cor_fundo = py5.color(0)
paleta: deque[int] = gera_paleta("mandarin-redux", como_deque=True)

divisoes: int = 4

vs = []
shapes = []
areas = []


def start(largura: int, altura: int):
    global group
    vs[:] = (
        np.array(pt) for pt in ((0, 0), (largura, 0), (largura, altura), (0, altura))
    )
    shapes.clear()
    shapes.append((0, 1, 2, 3))
    group = py5.create_shape(py5.GROUP)


def split_shapes():
    global max_area
    new_shapes = []
    while shapes:
        shp = shapes.pop()
        if len(shp) == 4:
            a, b, c, d = shp
            ac = py5.dist(*vs[a], *vs[c])
            bd = py5.dist(*vs[b], *vs[d])
            if ac < bd:
                new_shapes.append((a, b, c))
                new_shapes.append((a, c, d))
            else:
                new_shapes.append((a, b, d))
                new_shapes.append((b, c, d))
            continue
        a, b, c = shp
        ab = py5.dist(*vs[a], *vs[b])
        bc = py5.dist(*vs[b], *vs[c])
        if ab != bc:
            abi = len(vs)
            vs.append((vs[a] + vs[b]) / 2)
            bci = len(vs)
            vs.append((vs[b] + vs[c]) / 2)
            aci = len(vs)
            vs.append((vs[a] + vs[c]) / 2)
            new_shapes.append((a, abi, aci))
            new_shapes.append((abi, b, bci, aci))
            new_shapes.append((bci, c, aci))
        else:
            i = len(vs)
            if ab > bc:
                vs.append((vs[a] + vs[b]) / 2)
                new_shapes.append((a, i, c))
                new_shapes.append((i, b, c))
            if bc > ab:
                vs.append((vs[b] + vs[c]) / 2)
                new_shapes.append((b, i, a))
                new_shapes.append((i, c, a))
            else:
                vs.append((vs[a] + vs[c]) / 2)
                new_shapes.append((a, i, b))
                new_shapes.append((i, c, b))
    shapes[:] = new_shapes
    areas[:] = (shape_area(shp) for shp in shapes)
    max_area = max(areas)
    group_shape()


def distort(intensity=0.0008, f=1.1):
    global scaling_factors, va
    va = np.array(vs)
    va -= np.array((py5.width / 2, py5.height / 2))
    distances = np.linalg.norm(va, axis=1)
    scaling_factors = 1 + (intensity * (distances**f))
    va = 1.5 * va / scaling_factors[:, np.newaxis]
    meio = helpers.DIMENSOES.internal[0] / 2, helpers.DIMENSOES.internal[1] / 2
    va += np.array(meio)
    vs[:] = va
    group_shape()


def group_shape():
    global group
    group = py5.create_shape(py5.GROUP)
    for shp, _ in zip(shapes, areas, strict=False):
        poly = py5.create_shape()
        pts = np.array(vs)[np.array(shp)]
        with poly.begin_closed_shape():
            poly.vertices(pts)
        cor = paleta[0]
        paleta.rotate()
        poly.set_fill(cor)
        group.add_child(poly)


def shape_area(shp):
    return Polygon(np.array(vs)[np.array(shp)]).area


def setup():
    py5.size(*helpers.DIMENSOES.external, py5.P3D)
    py5.color_mode(py5.CMAP, "viridis", 255)
    start(*helpers.DIMENSOES.internal)
    for _ in range(divisoes):
        split_shapes()


def draw():
    py5.background(cor_fundo)
    with py5.push():
        py5.shape_mode(py5.CENTER)
        py5.translate(*helpers.DIMENSOES.centro)
        py5.shape(group)
    fps = py5.get_frame_rate()
    py5.window_title(f"Divisões: {divisoes} - Frame Rate: {fps:.2f}")
    # Credits and go
    canvas.sketch_frame(
        sketch,
        cor_fundo,
        "large_transparent_white",
        "transparent_white",
        version=2,
    )


def key_pressed():
    global divisoes
    key = py5.key
    if key == " ":
        save_and_close()
    elif key == "r":
        start(*helpers.DIMENSOES.internal)
    elif key == "p":
        split_shapes()
        divisoes += 1
    elif key == "d":
        distort()


def save_and_close():
    py5.no_loop()
    canvas.save_sketch_image(sketch)
    py5.exit_sketch()


if __name__ == "__main__":
    py5.run_sketch()
