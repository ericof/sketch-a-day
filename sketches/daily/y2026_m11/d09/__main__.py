"""2026-11-09
Cores e esferóide 05
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
TRACO = 1.2
BRILHO = 90.0
EMISSAO = 20
# Altura do ponto de luz: entre a frente da esfera (z = RAIO) e a câmera
# padrão do P3D (z ≈ 150 numa tela de 1000 px)
LUZ_Z = 150
# Curvas: cada triângulo vira uma grade com TESSELA divisões por aresta, e
# todos os pontos são deslocados por um campo de ruído antes de voltar à esfera
TESSELA = 4
ONDULACAO = 0.20
FREQUENCIA = 1.5
# Menor área (px², já ondulada) que uma divisão pode produzir
AREA_MINIMA = 80.0

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
ondulacao = ONDULACAO
area_minima = AREA_MINIMA
facetado = True
luz_x = 0.0
luz_y = 0.0

vertices: list[np.ndarray] = []
faces: list[tuple[int, ...]] = []
cores: list[tuple[int, int]] = []
retalhos: np.ndarray = np.empty((0, 0, 3))
forma: py5.Py5Shape | None = None


def _normaliza(v: np.ndarray) -> np.ndarray:
    """Projeta ``v`` na esfera unitária."""
    return v / np.linalg.norm(v)


def _ondula(pts: np.ndarray, amplitude: float) -> np.ndarray:
    """Desloca pontos da esfera unitária pelo campo de ruído e os reprojeta.

    O deslocamento vem de três canais do ``os_noise`` 3D amostrados na
    posição do ponto, então o mesmo ponto sempre se move igual.

    :param pts: Array ``(..., 3)`` de pontos na esfera unitária.
    :param amplitude: Tamanho do deslocamento, em unidades do raio.
    :returns: Array do mesmo formato, de volta à esfera unitária.
    """
    q = pts.reshape(-1, 3) * FREQUENCIA
    desvio = np.stack(
        [py5.os_noise(*(q + o).T) for o in (0.0, 31.7, 71.3)], axis=-1
    ).reshape(pts.shape)
    pts = pts + amplitude * desvio
    return pts / np.linalg.norm(pts, axis=-1, keepdims=True)


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
    Só é candidata a aresta cujos triângulos, medidos depois da ondulação (em
    px²), tenham ao menos ``4 * area_minima``: um quarto da área é o menor
    pedaço que uma divisão produz.
    """
    pos = _ondula(np.array(vs), ondulacao) * RAIO
    menor: dict[tuple[int, int], float] = {}
    for f in fs:
        a, b, c = pos[list(f)]
        area = 0.5 * float(np.linalg.norm(np.cross(b - a, c - a)))
        for i in range(3):
            e = _aresta(f[i], f[(i + 1) % 3])
            menor[e] = min(menor.get(e, area), area)
    comps = {e: float(np.linalg.norm(vs[e[0]] - vs[e[1]])) for e in menor}
    maior = max(comps.values())
    meios = {
        e: _novo_vertice(vs, vs[e[0]] + vs[e[1]])
        for e, comp in comps.items()
        if menor[e] >= 4 * area_minima and py5.random(1) < PROB_DIVISAO * comp / maior
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


def curva_malha() -> np.ndarray:
    """Subdivide cada triângulo pela grade e ondula os pontos.

    Um ponto compartilhado por triângulos vizinhos se move igual nos dois
    (ver :func:`_ondula`), então a malha continua sem frestas. ``ondulacao``
    controla a amplitude; ``FREQUENCIA``, o tamanho das ondas.

    :returns: Array ``(triângulos, pontos da grade, 3)`` na esfera unitária.
    """
    pesos = GRADE[0]
    vs = np.array(vertices)
    fs = np.array(faces)
    pts = sum(pesos[None, :, k : k + 1] * vs[fs[:, k]][:, None, :] for k in range(3))
    pts = pts / np.linalg.norm(pts, axis=-1, keepdims=True)
    return _ondula(pts, ondulacao)


def constroi_forma():
    """Monta o ``GROUP`` com o preenchimento e os contornos curvos.

    O preenchimento é um único ``TRIANGLES``: os subtriângulos de cada
    triângulo recebem o gradiente entre as suas duas cores da paleta e o
    material (especular, brilho, emissão) que reage às luzes. Com
    ``facetado`` a normal é a do centro do triângulo; sem ele, a de cada
    ponto. Os contornos ficam num ``LINES`` à parte, só na borda de cada
    triângulo, para que a grade interna não apareça.
    """
    global forma
    _, posicoes, tris, borda = GRADE
    preenchimento = py5.create_shape()
    with preenchimento.begin_shape(py5.TRIANGLES):
        preenchimento.no_stroke()
        preenchimento.specular(255, 255, 255)
        preenchimento.shininess(brilho)
        preenchimento.emissive(EMISSAO, EMISSAO, EMISSAO)
        for pts, (cor, cor_proxima) in zip(retalhos, cores, strict=True):
            gradiente = [lerp_color_rgba(cor, cor_proxima, t) for t in posicoes]
            if facetado:
                preenchimento.normal(*_normaliza(pts.sum(axis=0)))
            for tri in tris:
                for i in tri:
                    if not facetado:
                        preenchimento.normal(*pts[i])
                    preenchimento.fill(gradiente[i])
                    preenchimento.vertex(*(pts[i] * RAIO))
    contornos = py5.create_shape()
    with contornos.begin_shape(py5.LINES):
        contornos.stroke(cor_fundo)
        contornos.stroke_weight(TRACO)
        for pts in retalhos:
            for i, j in zip(borda, borda[1:] + borda[:1], strict=True):
                contornos.vertex(*(pts[i] * RAIO))
                contornos.vertex(*(pts[j] * RAIO))
    grupo = py5.create_shape(py5.GROUP)
    grupo.add_child(preenchimento)
    grupo.add_child(contornos)
    forma = grupo


def inicializa():
    global vertices, faces, cores, retalhos
    # O campo de ruído vem antes da malha: a subdivisão mede áreas já ondulada
    py5.os_noise_seed(py5.random_int(1_000_000))
    vertices, faces = gera_malha(niveis)
    cores = []
    for _ in faces:
        cores.append((paleta[0], paleta[1]))
        paleta.rotate()
    retalhos = curva_malha()
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
    py5.window_title(
        f"Níveis: {niveis} - Brilho: {brilho} - Ondulação: {ondulacao:.2f}"
        f" - FPS: {fps:.2f}"
    )
    # Credits and go
    canvas.sketch_frame(
        sketch,
        cor_fundo,
        "large_transparent_white",
        "transparent_white",
        version=2,
    )


def key_pressed():
    global niveis, brilho, facetado, ondulacao, retalhos, area_minima
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
        case "e" | "q" as key:
            ondulacao = max(0.0, ondulacao + (0.05 if key == "e" else -0.05))
            retalhos = curva_malha()
            constroi_forma()
        case "x" | "z" as key:
            area_minima = max(0.0, area_minima + (20.0 if key == "x" else -20.0))
            print(f"Área mínima: {area_minima:.0f} px²")
            inicializa()


def mouse_moved():
    global luz_x, luz_y
    luz_x, luz_y = py5.mouse_x, py5.mouse_y


def save_and_close():
    py5.no_loop()
    canvas.save_sketch_image(sketch)
    py5.exit_sketch()


if __name__ == "__main__":
    py5.run_sketch()
