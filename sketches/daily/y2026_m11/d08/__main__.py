"""2026-11-08
Cores e esferóide 04
Exercício de uso de gradientes em faces de um esferóide
ericof.com
png
Sketch,py5,CreativeCoding
"""

from collections import deque
from sketches.utils.draw import canvas
from sketches.utils.draw.cores import lerp_color_rgba
from sketches.utils.draw.cores.paletas import gera_paleta
from sketches.utils.helpers import sketches as helpers

import numpy as np
import py5


sketch = helpers.info_for_sketch(__file__, __doc__)

cor_fundo = py5.color(0)
paleta: deque[int] = gera_paleta("brasil-03", como_deque=True)

RAIO = 300
NIVEIS = 8
PROB_DIVISAO = 0.95
TRACO = 0.6
BRILHO = 40.0
EMISSAO = 12
# Altura do ponto de luz: entre a frente da esfera (z = RAIO) e a câmera
# padrão do P3D (z ≈ 150 numa tela de 1000 px)
LUZ_Z = 150

CUBO_VERTICES = (
    (-1, -1, -1),
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, 1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, 1, 1),
)
CUBO_FACES = (
    (0, 1, 2, 3),
    (5, 4, 7, 6),
    (4, 0, 3, 7),
    (1, 5, 6, 2),
    (4, 5, 1, 0),
    (3, 2, 6, 7),
)

niveis = NIVEIS
brilho = BRILHO
facetado = True
luz_x = 0.0
luz_y = 0.0

vertices: list[np.ndarray] = []
faces: list[tuple[int, ...]] = []
cores: list[tuple[int, int]] = []
forma: py5.Py5Shape | None = None


def _normaliza(v: np.ndarray) -> np.ndarray:
    """Projeta ``v`` na esfera unitária."""
    return v / np.linalg.norm(v)


def _novo_vertice(vs: list[np.ndarray], ponto: np.ndarray) -> int:
    """Adiciona ``ponto``, projetado na esfera, e retorna seu índice."""
    vs.append(_normaliza(ponto))
    return len(vs) - 1


def _aresta(a: int, b: int) -> tuple[int, int]:
    """Chave canônica de uma aresta, independente da ordem dos vértices."""
    return (a, b) if a < b else (b, a)


def divide_quadrado(quad: tuple[int, ...], vs: list[np.ndarray]) -> list[tuple]:
    """Divide uma face do cubo em triângulos, como em 2026-10-01.

    Todo ponto novo é interno à face, então a malha continua sem frestas.

    :param quad: Índices dos quatro vértices da face.
    :param vs: Lista de vértices, que recebe os pontos novos.
    :returns: Triângulos resultantes (2, 4 ou 4 com centro deslocado).
    """
    a, b, c, d = quad
    div = py5.random_int(2, 4)
    if div == 4:
        g = _novo_vertice(vs, vs[a] + vs[b] + vs[c] + vs[d])
        return [(a, b, g), (b, c, g), (c, d, g), (d, a, g)]
    ac = np.linalg.norm(vs[a] - vs[c])
    bd = np.linalg.norm(vs[b] - vs[d])
    p, q, r, s = (a, b, c, d) if ac < bd else (b, c, d, a)
    if div == 2:
        return [(p, q, r), (p, r, s)]
    g = _novo_vertice(vs, vs[p] + vs[q] + vs[r])
    return [(p, q, g), (q, r, g), (r, p, g), (p, r, s)]


def _meios(tri: tuple[int, ...], meios: dict) -> tuple[int | None, ...]:
    """Pontos médios já criados para as arestas ``ab``, ``bc`` e ``ca``."""
    return tuple(meios.get(_aresta(tri[i], tri[(i + 1) % 3])) for i in range(3))


def divide_triangulo(tri: tuple[int, ...], meios: dict) -> list[tuple]:
    """Divide um triângulo conforme as arestas marcadas para divisão.

    :param tri: Índices dos três vértices.
    :param meios: Mapa aresta -> índice do ponto médio, compartilhado entre
        vizinhos, o que mantém a malha conforme.
    :returns: De 1 a 4 triângulos.
    """
    mab, mbc, mca = _meios(tri, meios)
    divididas = sum(m is not None for m in (mab, mbc, mca))
    if divididas == 0:
        return [tri]
    a, b, c = tri
    if divididas == 3:
        return [(a, mab, mca), (mab, b, mbc), (mca, mbc, c), (mab, mbc, mca)]
    # Gira o triângulo até que ``ab`` esteja dividida e ``ca`` não
    while mab is None or mca is not None:
        a, b, c = b, c, a
        mab, mbc, mca = _meios((a, b, c), meios)
    if mbc is None:
        return [(a, mab, c), (mab, b, c)]
    return [(mab, b, mbc), (a, mab, mbc), (a, mbc, c)]


def divide_nivel(fs: list[tuple], vs: list[np.ndarray]) -> list[tuple]:
    """Aplica um nível de subdivisão a todos os triângulos.

    Cada aresta é dividida ao acaso, com chance proporcional ao seu
    comprimento, de modo que faces grandes tendem a se fragmentar primeiro.
    """
    arestas = {_aresta(f[i], f[(i + 1) % 3]) for f in fs for i in range(3)}
    comps = {e: float(np.linalg.norm(vs[e[0]] - vs[e[1]])) for e in arestas}
    maior = max(comps.values())
    meios = {
        e: _novo_vertice(vs, vs[e[0]] + vs[e[1]])
        for e, comp in comps.items()
        if py5.random(1) < PROB_DIVISAO * comp / maior
    }
    novas = []
    for f in fs:
        novas.extend(divide_triangulo(f, meios))
    return novas


def gera_malha(total: int) -> tuple[list[np.ndarray], list[tuple]]:
    """Gera a malha da esfera unitária a partir de um cubo.

    :param total: Quantidade de níveis de subdivisão (o primeiro divide as
        faces do cubo).
    :returns: Vértices e triângulos.
    """
    vs = [_normaliza(np.array(v, dtype=float)) for v in CUBO_VERTICES]
    fs = []
    for quad in CUBO_FACES:
        fs.extend(divide_quadrado(quad, vs))
    for _ in range(total - 1):
        fs = divide_nivel(fs, vs)
    return vs, fs


def constroi_forma():
    """Monta o ``GROUP`` com um ``Py5Shape`` por triângulo.

    Cada triângulo recebe um gradiente entre duas cores vizinhas da paleta e
    o material (especular, brilho, emissão) que reage às luzes. Com
    ``facetado`` a normal é a da face; sem ele, a de cada vértice.
    """
    global forma
    grupo = py5.create_shape(py5.GROUP)
    for tri, (cor, cor_proxima) in zip(faces, cores, strict=True):
        pts = [vertices[i] for i in tri]
        total = len(pts) - 1
        poly = py5.create_shape()
        with poly.begin_closed_shape():
            poly.stroke(cor_fundo)
            poly.stroke_weight(TRACO)
            poly.specular(255, 255, 255)
            poly.shininess(brilho)
            poly.emissive(EMISSAO, EMISSAO, EMISSAO)
            if facetado:
                poly.normal(*_normaliza(sum(pts)))
            for i, p in enumerate(pts):
                if not facetado:
                    poly.normal(*p)
                poly.fill(lerp_color_rgba(cor, cor_proxima, i / total))
                poly.vertex(*(p * RAIO))
        grupo.add_child(poly)
    forma = grupo


def inicializa():
    global vertices, faces, cores
    vertices, faces = gera_malha(niveis)
    cores = []
    for _ in faces:
        cores.append((paleta[0], paleta[1]))
        paleta.rotate()
    constroi_forma()
    print(f"Níveis: {niveis} - Triângulos: {len(faces)}")


def luzes():
    """Luz principal branca, preenchimento frio e um ponto quente de brilho.

    O ponto quente fica em ``(luz_x, luz_y)``, controlado pelo mouse.
    """
    py5.ambient_light(35, 35, 45)
    py5.light_specular(255, 255, 255)
    py5.directional_light(170, 170, 170, 0.5, 0.6, -1)
    py5.light_specular(120, 140, 255)
    py5.directional_light(50, 70, 140, -0.7, -0.3, -0.5)
    py5.light_specular(255, 240, 220)
    py5.point_light(255, 230, 200, luz_x, luz_y, LUZ_Z)


def setup():
    global luz_x, luz_y
    py5.size(*helpers.DIMENSOES.external, py5.P3D)
    cx, cy = helpers.DIMENSOES.centro
    luz_x, luz_y = cx - RAIO, cy - RAIO
    inicializa()


def draw():
    py5.background(cor_fundo)
    radianos = float(py5.radians(py5.frame_count))
    luzes()
    with py5.push():
        py5.translate(*helpers.DIMENSOES.centro, 0)
        py5.rotate_y(radianos)
        py5.rotate_z(radianos)
        if forma:
            py5.shape(forma)
    py5.no_lights()
    fps = py5.get_frame_rate()
    py5.window_title(f"Níveis: {niveis} - Brilho: {brilho} - FPS: {fps:.2f}")
    # Credits and go
    canvas.sketch_frame(
        sketch,
        cor_fundo,
        "large_transparent_white",
        "transparent_white",
        version=2,
    )


def key_pressed():
    global niveis, brilho, facetado
    match py5.key:
        case " ":
            save_and_close()
        case "r":
            inicializa()
        case "a" | "d" as key:
            niveis = max(1, niveis + (1 if key == "d" else -1))
            inicializa()
        case "f":
            facetado = not facetado
            constroi_forma()
        case "w" | "s" as key:
            brilho = max(1.0, brilho + (10.0 if key == "w" else -10.0))
            constroi_forma()


def mouse_moved():
    global luz_x, luz_y
    luz_x, luz_y = py5.mouse_x, py5.mouse_y


def save_and_close():
    py5.no_loop()
    canvas.save_sketch_image(sketch)
    py5.exit_sketch()


if __name__ == "__main__":
    py5.run_sketch()
