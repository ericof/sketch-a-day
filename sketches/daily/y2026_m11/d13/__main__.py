"""2026-11-13
Cores e planos 04
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
paleta: deque[int] = gera_paleta("op-2363803", como_deque=True)

NIVEIS = 9
PROB_DIVISAO = 0.98
# Menor área (px²) que uma divisão pode produzir
AREA_MINIMA = 120.0
TRACO = 1.1
# Curvas: cada triângulo vira uma grade com TESSELA divisões por aresta, e
# todos os pontos são deslocados por um campo de ruído (ONDULACAO em px)
TESSELA = 6
ONDULACAO = 30.0
FREQUENCIA = 0.004


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


def _grade(n: int) -> tuple[np.ndarray, np.ndarray, list[tuple], list[int]]:
    """Grade baricêntrica que divide um triângulo ``abc`` em ``n²`` partes.

    :param n: Divisões por aresta.
    :returns: Pesos ``(a, b, c)`` de cada ponto; a posição de cada ponto no
        gradiente (0 em ``a``, 0.5 em ``b``, 1 em ``c``, como nos vértices do
        triângulo original); os subtriângulos, na mesma orientação de ``abc``;
        e o contorno ``a -> b -> c``.
    """
    idx: dict[tuple[int, int], int] = {}
    pesos = []
    for i in range(n + 1):
        for j in range(n + 1 - i):
            idx[i, j] = len(pesos)
            pesos.append((n - i - j, i, j))
    tris = []
    for i in range(n):
        for j in range(n - i):
            tris.append((idx[i, j], idx[i + 1, j], idx[i, j + 1]))
            if i + j < n - 1:
                tris.append((idx[i + 1, j], idx[i + 1, j + 1], idx[i, j + 1]))
    borda = (
        [idx[i, 0] for i in range(n)]
        + [idx[n - j, j] for j in range(n)]
        + [idx[0, n - j] for j in range(n)]
    )
    w = np.array(pesos, dtype=float) / n
    return w, w[:, 1] * 0.5 + w[:, 2], tris, borda


GRADE = _grade(TESSELA)


def _ondula(
    pts: np.ndarray, amplitude: float, minimo: np.ndarray, maximo: np.ndarray
) -> np.ndarray:
    """Desloca pontos do plano por um campo de ruído, sem sair do retângulo.

    O deslocamento vem de dois canais do ``os_noise`` amostrados na posição
    do ponto, então o mesmo ponto sempre se move igual. Em cada eixo ele é
    atenuado pela distância à borda: nunca passa da metade dessa distância,
    e um ponto na borda só desliza ao longo dela (os cantos ficam fixos). A
    rampa de atenuação vai até ``2 * amplitude``; uma rampa mais curta
    comprime os pontos junto à borda a ponto de dobrar a malha.

    :param pts: Array ``(..., 2)`` de pontos.
    :param amplitude: Tamanho máximo do deslocamento, em px.
    :param minimo: Canto ``(x0, y0)`` do retângulo.
    :param maximo: Canto ``(x1, y1)`` do retângulo.
    :returns: Array do mesmo formato, com os pontos deslocados.
    """
    if amplitude <= 0:
        return pts
    q = pts.reshape(-1, 2) * FREQUENCIA
    canais = [py5.os_noise(*(q + o).T) for o in (0.0, 31.7)]
    desvio = np.stack(canais, axis=-1).reshape(pts.shape)
    folga = np.minimum(pts - minimo, maximo - pts)
    atenuacao = np.clip(folga / (2 * amplitude), 0.0, 1.0)
    return pts + amplitude * desvio * atenuacao


def curva_malha(vertices: list[np.ndarray], faces: list[tuple[int, ...]]) -> np.ndarray:
    """Subdivide cada triângulo pela grade e ondula os pontos.

    Um ponto compartilhado por triângulos vizinhos se move igual nos dois
    (ver :func:`_ondula`), então a malha continua sem frestas. ``ONDULACAO``
    controla a amplitude; ``FREQUENCIA``, o tamanho das ondas.

    :param vertices: Vértices ``(x, y)`` da malha.
    :param faces: Triângulos, como índices em ``vertices``.
    :returns: Array ``(triângulos, pontos da grade, 2)``.
    """
    pesos = GRADE[0]
    vs = np.array(vertices)
    fs = np.array(faces)
    pts = sum(pesos[None, :, k : k + 1] * vs[fs[:, k]][:, None, :] for k in range(3))
    return _ondula(pts, ONDULACAO, vs.min(axis=0), vs.max(axis=0))


def cria_forma(
    vertices: list[np.ndarray], faces: list[tuple[int, ...]], paleta: deque[int]
) -> py5.Py5Shape:
    """Monta o ``GROUP`` com o preenchimento e os contornos curvos.

    Como em 2026-11-09, cada triângulo recebe duas cores consecutivas da
    paleta, que gira a cada face, num gradiente de ``a`` (primeira) a ``c``
    (segunda). O preenchimento é um único ``TRIANGLES`` sem traço; os
    contornos ficam num ``LINES`` à parte, só na borda de cada triângulo,
    para que a grade interna não apareça.

    :param vertices: Vértices ``(x, y)`` da malha.
    :param faces: Triângulos, como índices em ``vertices``.
    :param paleta: Cores da paleta; é girada ao longo das faces.
    :returns: A forma pronta para ``py5.shape``.
    """
    _, posicoes, tris, borda = GRADE
    retalhos = curva_malha(vertices, faces)
    preenchimento = py5.create_shape()
    with preenchimento.begin_shape(py5.TRIANGLES):
        preenchimento.no_stroke()
        for pts in retalhos:
            cor, cor_proxima = paleta[0], paleta[1]
            paleta.rotate(py5.random_int(2, 6))
            gradiente = [lerp_color_rgba(cor, cor_proxima, t) for t in posicoes]
            for tri in tris:
                for i in tri:
                    preenchimento.fill(gradiente[i])
                    preenchimento.vertex(*pts[i], 0)
    contornos = py5.create_shape()
    with contornos.begin_shape(py5.LINES):
        contornos.stroke(cor_fundo)
        contornos.stroke_weight(TRACO)
        for pts in retalhos:
            for i, j in zip(borda, borda[1:] + borda[:1], strict=True):
                contornos.vertex(*pts[i], 0)
                contornos.vertex(*pts[j], 0)
    forma = py5.create_shape(py5.GROUP)
    forma.add_child(preenchimento)
    forma.add_child(contornos)
    return forma


def inicializa():
    global forma
    # Campo de ruído novo a cada malha, para as curvas mudarem com ``r``
    py5.os_noise_seed(py5.random_int(1_000_000))
    vertices, faces = subdivide_retangulo(0, 0, *helpers.DIMENSOES.internal)
    forma = cria_forma(vertices, faces, paleta)


def setup():
    py5.size(*helpers.DIMENSOES.external, py5.P3D)
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
