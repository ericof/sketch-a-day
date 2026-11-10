"""2026-11-10
Cores e planos 01
Exercício de uso de gradientes e subdivisão de um plano
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

NIVEIS = 8
PROB_DIVISAO = 0.95
# Menor área (px²) que uma divisão pode produzir
AREA_MINIMA = 80.0
TRACO = 0.3


def _novo_vertice(vs: list[np.ndarray], ponto: np.ndarray) -> int:
    """Adiciona ``ponto`` à lista de vértices e retorna seu índice."""
    vs.append(ponto)
    return len(vs) - 1


def _aresta(a: int, b: int) -> tuple[int, int]:
    """Chave canônica de uma aresta, independente da ordem dos vértices."""
    return (a, b) if a < b else (b, a)


def _area(vs: list[np.ndarray], tri: tuple[int, ...]) -> float:
    """Área de um triângulo no plano."""
    a, b, c = (vs[i] for i in tri)
    (ux, uy), (wx, wy) = b - a, c - a
    return 0.5 * abs(float(ux * wy - uy * wx))


def _divide_quadrado(quad: tuple[int, ...], vs: list[np.ndarray]) -> list[tuple]:
    """Divide o retângulo inicial em triângulos, como em 2026-11-09.

    :param quad: Índices dos quatro vértices, em ordem.
    :param vs: Lista de vértices, que recebe os pontos novos.
    :returns: Triângulos resultantes (2, 4 ou 4 com centro deslocado).
    """
    a, b, c, d = quad
    div = py5.random_int(2, 4)
    if div == 4:
        g = _novo_vertice(vs, (vs[a] + vs[b] + vs[c] + vs[d]) / 4)
        return [(a, b, g), (b, c, g), (c, d, g), (d, a, g)]
    ac = np.linalg.norm(vs[a] - vs[c])
    bd = np.linalg.norm(vs[b] - vs[d])
    p, q, r, s = (a, b, c, d) if ac < bd else (b, c, d, a)
    if div == 2:
        return [(p, q, r), (p, r, s)]
    g = _novo_vertice(vs, (vs[p] + vs[q] + vs[r]) / 3)
    return [(p, q, g), (q, r, g), (r, p, g), (p, r, s)]


def _meios(tri: tuple[int, ...], meios: dict) -> tuple[int | None, ...]:
    """Pontos médios já criados para as arestas ``ab``, ``bc`` e ``ca``."""
    return tuple(meios.get(_aresta(tri[i], tri[(i + 1) % 3])) for i in range(3))


def _divide_triangulo(tri: tuple[int, ...], meios: dict) -> list[tuple]:
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


def _divide_nivel(
    fs: list[tuple], vs: list[np.ndarray], area_minima: float
) -> list[tuple]:
    """Aplica um nível de subdivisão a todos os triângulos.

    Cada aresta é dividida ao acaso, com chance proporcional ao seu
    comprimento. Só é candidata a aresta cujos triângulos tenham ao menos
    ``4 * area_minima``: um quarto da área é o menor pedaço que uma divisão
    produz.
    """
    menor: dict[tuple[int, int], float] = {}
    for f in fs:
        area = _area(vs, f)
        for i in range(3):
            e = _aresta(f[i], f[(i + 1) % 3])
            menor[e] = min(menor.get(e, area), area)
    comps = {e: float(np.linalg.norm(vs[e[0]] - vs[e[1]])) for e in menor}
    maior = max(comps.values())
    meios = {
        e: _novo_vertice(vs, (vs[e[0]] + vs[e[1]]) / 2)
        for e, comp in comps.items()
        if menor[e] >= 4 * area_minima and py5.random(1) < PROB_DIVISAO * comp / maior
    }
    novas = []
    for f in fs:
        novas.extend(_divide_triangulo(f, meios))
    return novas


def subdivide_retangulo(
    x0: float,
    y0: float,
    x1: float,
    y1: float,
    niveis: int = NIVEIS,
    area_minima: float = AREA_MINIMA,
) -> tuple[list[np.ndarray], list[tuple[int, int, int]]]:
    """Subdivide o retângulo ``(x0, y0)`` a ``(x1, y1)`` em triângulos.

    Mesmo processo da esfera de 2026-11-09, no plano: o primeiro nível divide
    o retângulo em 2 ou 4 triângulos; os seguintes dividem arestas ao acaso,
    compartilhando os pontos médios entre vizinhos, então a malha não tem
    frestas.

    :param x0: Coordenada x de um canto.
    :param y0: Coordenada y de um canto.
    :param x1: Coordenada x do canto oposto.
    :param y1: Coordenada y do canto oposto.
    :param niveis: Quantidade de níveis de subdivisão.
    :param area_minima: Menor área (px²) que uma divisão pode produzir.
    :returns: Vértices (arrays ``(x, y)``) e triângulos (índices nos
        vértices), todos na mesma orientação do retângulo.
    """
    vs = [np.array(p, dtype=float) for p in ((x0, y0), (x1, y0), (x1, y1), (x0, y1))]
    fs = _divide_quadrado((0, 1, 2, 3), vs)
    for _ in range(niveis - 1):
        fs = _divide_nivel(fs, vs, area_minima)
    return vs, fs


def cria_forma(
    vertices: list[np.ndarray], faces: list[tuple[int, ...]], paleta: deque[int]
) -> py5.Py5Shape:
    """Monta um ``TRIANGLES`` com um gradiente em cada triângulo.

    Como em 2026-11-09, cada triângulo recebe duas cores consecutivas da
    paleta, que gira a cada face: ``a`` usa a primeira, ``c`` a segunda e
    ``b`` a cor intermediária. O traço, na cor do fundo, marca as arestas.

    :param vertices: Vértices ``(x, y)`` da malha.
    :param faces: Triângulos, como índices em ``vertices``.
    :param paleta: Cores da paleta; é girada ao longo das faces.
    :returns: A forma pronta para ``py5.shape``.
    """
    forma = py5.create_shape()
    with forma.begin_shape(py5.TRIANGLES):
        forma.stroke(cor_fundo)
        forma.stroke_weight(TRACO)
        for face in faces:
            cor, cor_proxima = paleta[0], paleta[1]
            paleta.rotate()
            gradiente = (cor, lerp_color_rgba(cor, cor_proxima, 0.5), cor_proxima)
            for i, cor_vertice in zip(face, gradiente, strict=True):
                forma.fill(cor_vertice)
                forma.vertex(*vertices[i], 0)
    return forma


def inicializa():
    global forma
    vertices, faces = subdivide_retangulo(0, 0, *helpers.DIMENSOES.internal)
    forma = cria_forma(vertices, faces, paleta)


def setup():
    py5.size(*helpers.DIMENSOES.external, py5.P3D)
    py5.color_mode(py5.HSB, 360, 100, 100)
    inicializa()


def draw():
    py5.background(cor_fundo)
    with py5.push():
        py5.translate(*helpers.DIMENSOES.pos_interno, 0)
        py5.shape(forma)

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
