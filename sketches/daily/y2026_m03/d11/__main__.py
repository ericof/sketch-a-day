"""2026-03-11
Divisões 08
Inspirado em sketch de Alexandre Villares
ericof.com|https://abav.lugaralgum.com/sketch-a-day/#sketch_2026_02_16
png
Sketch,py5,CreativeCoding
"""

from collections import deque
from dataclasses import dataclass
from dataclasses import field
from shapely import Polygon
from sketches.utils.draw import canvas
from sketches.utils.draw.cores import lerp_color_rgba
from sketches.utils.draw.cores.paletas import gera_paleta
from sketches.utils.helpers import sketches as helpers

import numpy as np
import py5


sketch = helpers.info_for_sketch(__file__, __doc__)

cor_fundo = py5.color(0)
paleta: deque[int] = gera_paleta("DJ1", como_deque=True)

divisoes: int = 4


@dataclass
class InfoGrupo:
    vs: list = field(default_factory=list)
    shapes: list = field(default_factory=list)
    areas: list = field(default_factory=list)
    max_area: float = 0.0
    shape: py5.Py5Shape | None = None


grupos: dict[int, InfoGrupo] = {}

intensidade: float = 0.0008
fator: float = 1.1
distorcao_va = 1.5


def start(idx: int, largura: int, altura: int):
    """Initialize a division group from a rectangle covering the internal canvas."""
    vs = [np.array(pt) for pt in ((0, 0), (largura, 0), (largura, altura), (0, altura))]
    shapes = []
    shapes.append((0, 1, 2, 3))
    areas = [shape_area((0, 1, 2, 3), vs)]
    grupos[idx] = InfoGrupo(
        shape=None, vs=vs, shapes=shapes, areas=areas, max_area=max(areas)
    )
    return grupos


def _divide_quadrado(
    idx: int, shp: tuple[int, ...], vs: list, div: int = 2
) -> list[tuple[int, ...]]:
    """Divide a quadrilateral into triangles based on div."""
    a, b, c, d = shp
    ac = py5.dist(*vs[a], *vs[c])
    bd = py5.dist(*vs[b], *vs[d])
    gi = len(vs)
    vs.append((vs[a] + vs[b] + vs[c] + vs[d]) / gi)
    new_shapes = [(a, b, c), (a, c, d)] if ac < bd else [(a, b, d), (b, c, d)]
    match div:
        case 3:
            s = new_shapes.pop(-1)
            new_shapes.append((s[0], s[1], gi))
            new_shapes.append((gi, s[1], s[2]))
        case 4:
            new_shapes = [(a, b, gi), (b, c, gi), (c, d, gi), (d, a, gi)]
        case _:
            new_shapes = new_shapes
    print(f"{idx} - 4 -> {len(new_shapes)}")
    return new_shapes


def _divide_trinagulo(
    idx: int, shp: tuple[int, ...], vs: list, div: int = 2
) -> list[tuple[int, ...]]:
    """Divide a triangle into smaller triangles based on edge lengths."""
    a, b, c = shp
    ab = py5.dist(*vs[a], *vs[b])
    ab_m = (vs[a] + vs[b]) / div
    bc = py5.dist(*vs[b], *vs[c])
    bc_m = (vs[b] + vs[c]) / div
    ca = py5.dist(*vs[c], *vs[a])
    ca_m = (vs[c] + vs[a]) / div
    new_shapes = []
    if ab == bc == ca:
        bci = len(vs)
        vs.append(bc_m)
        new_shapes.append((a, b, bci))
        new_shapes.append((bci, a, c))
    elif ab == bc:
        cai = len(vs)
        vs.append(ca_m)
        new_shapes.append((a, b, cai))
        new_shapes.append((cai, a, c))
    elif bc == ca:
        abi = len(vs)
        vs.append(ab_m)
        new_shapes.append((a, c, abi))
        new_shapes.append((abi, b, c))
    else:
        new_shapes.append((a, c, b))
        new_shapes.append((b, a, c))
    print(f"{idx} - 3 -> {len(new_shapes)}")
    return new_shapes


SPLIT_SHAPE = {
    3: _divide_trinagulo,
    4: _divide_quadrado,
}


def split_shapes(idx: int):
    """Create the next subdivision level for the given group index."""
    info = grupos.get(idx)
    if info and info.shape:
        # Não é necessário dividir novamente se já temos um grupo
        # para essa quantidade de divisões
        return
    idx_anterior = idx - 1 if idx > 1 else 1
    anterior = grupos[idx_anterior]
    shapes = anterior.shapes
    vs = list(anterior.vs)
    new_shapes = []
    while shapes:
        shp = shapes.pop()
        total = len(shp)
        div = 2 if total == 3 else py5.random_int(2, 5)
        print(total, div)
        split_fn = SPLIT_SHAPE.get(total)
        if split_fn:
            new_shapes.extend(split_fn(idx, shp, vs, div))

    areas = [shape_area(shp, vs) for shp in new_shapes]
    info = InfoGrupo(
        shape=None, vs=vs, shapes=new_shapes, areas=areas, max_area=max(areas)
    )
    grupos[idx] = info
    group_shape(idx)


def distort(idx: int, intensity=intensidade, f=fator):
    """Apply radial distortion to the group's vertices based on center distance."""
    info = grupos[idx]
    vs = info.vs
    meio = helpers.DIMENSOES.internal[0] / 2, helpers.DIMENSOES.internal[1] / 2
    va = np.array(vs)
    va -= np.array((meio[0], meio[1]))
    distances = np.linalg.norm(va, axis=1)
    scaling_factors = 1 + (intensity * (distances**f))
    va = distorcao_va * va / scaling_factors[:, np.newaxis]
    va += np.array(meio)
    info.vs = va
    _group_shape(info)


def _group_shape(info: InfoGrupo):
    """Build and store a py5 group shape from an `InfoGrupo` definition."""
    grupo = py5.create_shape(py5.GROUP)
    shapes = info.shapes
    areas = info.areas
    vs = info.vs
    formas = list(zip(shapes, areas, strict=False))
    for shp, _ in formas:
        poly = py5.create_shape()
        cor = paleta[0]
        cor_proxima = paleta[1]
        pts = np.array(vs)[np.array(shp)]
        total = len(pts)
        with poly.begin_closed_shape():
            poly.vertices(pts)
        cores = []
        for i in range(total):
            cor = lerp_color_rgba(cor, cor_proxima, i, (0, total))
            cores.append(cor)
        poly.set_fills(cores)
        poly.set_stroke_weight(4)
        grupo.add_child(poly)
        paleta.rotate()
    info.shape = grupo


def group_shape(idx: int):
    """Create a renderable group shape for a stored subdivision group."""
    info = grupos[idx]
    if info.shape:
        # Já temos um shape para esse grupo, não precisamos recriar
        print(f"Shape para {idx} divisões já existe. Pulando criação.")
        return
    _group_shape(info)


def shape_area(shp, vs):
    """Return the polygon area for a shape index tuple over a vertex list."""
    return Polygon(np.array(vs)[np.array(shp)]).area


def setup():
    """Configure the sketch and precompute subdivision groups up to `divisoes`."""
    py5.size(*helpers.DIMENSOES.external, py5.P3D)
    for idx in range(1, divisoes + 1):
        grupos = start(idx, *helpers.DIMENSOES.internal)
        split_shapes(idx=idx)
        print(f"{idx} - {grupos[idx].shape.get_child_count()}")


def draw():
    """Render the current subdivision group and update frame overlay metadata."""
    py5.background(cor_fundo)
    info = grupos[divisoes]
    if grupo := info.shape:
        with py5.push():
            py5.shape_mode(py5.CENTER)
            py5.translate(*helpers.DIMENSOES.centro)
            py5.shape(grupo)

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
    """Handle keyboard controls for saving, subdividing, and distortion."""
    global divisoes
    key = py5.key
    if key == " ":
        save_and_close()
    elif key == "r":
        start(*helpers.DIMENSOES.internal)
    elif key == "a":
        divisoes -= 1 if divisoes > 1 else 0
        split_shapes(divisoes)
    elif key == "d":
        divisoes += 1
        split_shapes(divisoes)
    elif key == "w":
        distort(divisoes)


def save_and_close():
    """Stop rendering, save the current frame, and exit the sketch."""
    py5.no_loop()
    canvas.save_sketch_image(sketch)
    py5.exit_sketch()


if __name__ == "__main__":
    py5.run_sketch()
