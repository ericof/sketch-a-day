"""2026-04-10
Dyson 01 / Language 13
Dodecaedro que atua como uma esfera de Dyson com textura de grades compostas por padrões de traços e círculos.
ericof.com
png
Sketch,py5,CreativeCoding
"""  # noqa: E501

from collections.abc import Sequence
from dataclasses import dataclass
from random import shuffle
from sketches.padroes import biblioteca as b
from sketches.padroes import tipos as t
from sketches.padroes.fabrica import GradeLinearPadroes
from sketches.utils.draw import canvas
from sketches.utils.draw.cores.paletas import gera_paleta
from sketches.utils.helpers import sketches as helpers
from sketches.utils.helpers.window import title

import math
import numpy as np
import py5


sketch = helpers.info_for_sketch(__file__, __doc__)

cor_fundo = py5.color(0)
celula_fundo = py5.color("#222")
celulas = 32
espacamento = 0
traco = 2
rotacoes = range(0, 360, 45)
camadas = 3
fundo = py5.color("#000")
borda = t.Borda(fundo, espacamento)
raio_dodecaedro = 300
profundidade_face = 20


@dataclass
class Rotacao:
    x: float = -64
    y: float = 21
    z: float = 0
    dist_z: float = -600
    explosao: float = 80


rotacao = Rotacao()


def gera_colecao(largura: float, altura: float) -> list[t.Padrao]:
    """Cria instâncias de todos os padrões da categoria "tracos".

    :param largura: Largura de cada padrão em pixels.
    :param altura: Altura de cada padrão em pixels.
    :returns: Lista de instâncias de :class:`t.Padrao`.
    """
    payload = {"traco": traco, "largura": largura, "altura": altura}
    colecao = [
        padrao(**payload) for padrao in b.Biblioteca.get_categoria("tracos").values()
    ]
    return colecao


def gera_paletas() -> tuple[Sequence[int | str], ...]:
    """Carrega as paletas de cores usadas no sketch.

    :returns: Tupla com paletas que comecem com `op-`.
    """
    paletas = []
    nomes_paletas = ["pastel"]
    for nome in nomes_paletas:
        paletas.append(gera_paleta(nome))
    shuffle(paletas)
    return tuple(paletas)


PALETAS = gera_paletas()


def gera_cores_padrao(idy: int) -> t.CoresPadrao:
    """Sorteia cores distintas de uma paleta para um padrão.

    :param idy: Índice da linha que estamos utilizando.
    :returns: :class:`t.CoresPadrao` com traço e preenchimento distintos
        e diferentes de branco.
    """
    paleta_id = idy % len(PALETAS)
    paleta = PALETAS[paleta_id]
    fundo = None
    valida = False
    while not valida:
        preenchimento = py5.random_choice(paleta)
        traco = py5.random_choice(paleta)
        valida = preenchimento != traco != celula_fundo
    return t.CoresPadrao(traco, preenchimento, fundo)


def calcula_celulas(
    largura: float,
    altura: float,
    celulas_x: int,
    celulas_y: int,
    espacamento_x: int,
    espacamento_y: int,
    colecao: list[t.Padrao],
    borda: t.Borda | None,
) -> list[tuple[t.Celula, tuple[t.Padrao, float, t.CoresPadrao, float]]]:
    """Calcula células e associa padrões, rotações e cores para cada camada.

    Gera 3 camadas sobrepostas (``idz`` 0-2) com profundidades z distintas.
    As cores são sorteadas por linha (``celula.idy``), usando paletas ``op-``.

    :param largura: Largura total da grade em pixels.
    :param altura: Altura total da grade em pixels.
    :param celulas_x: Número de colunas da grade.
    :param celulas_y: Número de linhas da grade.
    :param espacamento_x: Espaçamento horizontal entre células em pixels.
    :param espacamento_y: Espaçamento vertical entre células em pixels.
    :param colecao: Instâncias de padrões disponíveis para sorteio.
    :param borda: Borda opcional a aplicar em cada célula.
    :returns: Lista de tuplas ``(celula, (padrao, rotacao, cores, z))``.
    """
    celulas = []
    for idz in range(0, camadas):
        grade = GradeLinearPadroes(
            largura,
            altura,
            celulas_x,
            celulas_y,
            (espacamento_x, espacamento_y),
            colecao,
            borda=borda,
        )
        grade_padroes = grade.padroes
        z = -10 + idz
        for celula in grade.celulas:
            cores = gera_cores_padrao(celula.idy)
            cores.fundo = celula_fundo
            padrao = next(grade_padroes)
            rotacao = py5.random_choice(rotacoes)
            celulas.append((celula, (padrao, rotacao, cores, z)))
    return celulas


def inicializa_celulas():
    """Calcula as células e suas associações de padrões, rotações e cores."""
    with title("Regenerando células"):
        largura, altura = helpers.DIMENSOES.internal
        colecao = gera_colecao(largura / celulas, altura / celulas)
        retorno = calcula_celulas(
            largura, altura, celulas, celulas, espacamento, espacamento, colecao, borda
        )
    return retorno


def gera_imagem(
    celulas: list[tuple[t.Celula, tuple[t.Padrao, float, t.CoresPadrao, float]]],
):
    """Gera a imagem do sketch a partir das células calculadas.

    :param celulas: Lista de tuplas ``(celula, (padrao, rotacao, cores, z))``.
    """
    pg = py5.create_graphics(*helpers.DIMENSOES.internal, py5.P3D)
    with pg.begin_draw():
        pg.background(celula_fundo)
        for celula, (padrao, rotacao, cores, z) in celulas:
            celula(padrao, rotacao, cores, z=z, pg=pg)
    # Forçar alpha 255 em todos os pixels para evitar transparência em P3D.
    pg.load_np_pixels()
    pg.np_pixels[..., 0] = 255  # canal alpha (ARGB)
    pg.update_np_pixels()
    return pg


def _coords_canonicas_dodecaedro() -> list[tuple[float, float, float]]:
    """Gera as 20 coordenadas canônicas de um dodecaedro (não normalizado).

    :returns: Lista de 20 tuplas ``(x, y, z)``.
    """
    phi = (1 + math.sqrt(5)) / 2
    coords: list[tuple[float, float, float]] = [
        (sx, sy, sz) for sx in (-1, 1) for sy in (-1, 1) for sz in (-1, 1)
    ]
    coords.extend((0, sy / phi, sz * phi) for sy in (-1, 1) for sz in (-1, 1))
    coords.extend((sx / phi, sy * phi, 0) for sx in (-1, 1) for sy in (-1, 1))
    coords.extend((sx * phi, 0, sz / phi) for sx in (-1, 1) for sz in (-1, 1))
    return coords


def _vertices_dodecaedro(raio: float) -> list[np.ndarray]:
    """Calcula os 20 vértices de um dodecaedro regular inscrito em esfera.

    :param raio: Raio da esfera circunscrita.
    :returns: Lista de 20 arrays ``(x, y, z)``.
    """
    coords = _coords_canonicas_dodecaedro()
    vertices = []
    for c in coords:
        v = np.array(c, dtype=float)
        v = v / np.linalg.norm(v) * raio
        vertices.append(v)
    return vertices


def _adjacencia_dodecaedro(
    vertices: list[np.ndarray],
) -> dict[int, list[int]]:
    """Calcula adjacência entre vértices usando a menor distância como aresta.

    :param vertices: 20 vértices do dodecaedro.
    :returns: Dicionário de vizinhos por índice de vértice.
    """
    n = len(vertices)
    dist_min = float("inf")
    for i in range(n):
        for j in range(i + 1, n):
            d = float(np.linalg.norm(vertices[i] - vertices[j]))
            if d < dist_min:
                dist_min = d
    tolerancia = dist_min * 1.1
    vizinhos: dict[int, list[int]] = {i: [] for i in range(n)}
    for i in range(n):
        for j in range(i + 1, n):
            if np.linalg.norm(vertices[i] - vertices[j]) < tolerancia:
                vizinhos[i].append(j)
                vizinhos[j].append(i)
    return vizinhos


def _ciclos_pentagonais(
    n: int,
    vizinhos: dict[int, list[int]],
) -> set[tuple[int, ...]]:
    """Encontra todos os ciclos de 5 vértices adjacentes (faces pentagonais).

    :param n: Número total de vértices.
    :param vizinhos: Dicionário de adjacência.
    :returns: Conjunto de tuplas de 5 índices ordenados.
    """
    faces_set: set[tuple[int, ...]] = set()
    for a in range(n):
        for b_idx in vizinhos[a]:
            for c in vizinhos[b_idx]:
                if c == a:
                    continue
                for d in vizinhos[c]:
                    if d in (a, b_idx):
                        continue
                    for e in vizinhos[d]:
                        if e in (b_idx, c):
                            continue
                        if a in vizinhos[e]:
                            face = tuple(sorted([a, b_idx, c, d, e]))
                            faces_set.add(face)
    return faces_set


def _ordena_pentagono(
    ids: list[int],
    vertices: list[np.ndarray],
) -> list[int]:
    """Ordena 5 vértices em sentido anti-horário visto de fora.

    :param ids: 5 índices de vértices.
    :param vertices: Lista completa de vértices.
    :returns: Índices reordenados em sentido anti-horário.
    """
    centro = sum(vertices[i] for i in ids) / 5
    normal = np.cross(
        vertices[ids[1]] - vertices[ids[0]],
        vertices[ids[2]] - vertices[ids[0]],
    )
    if np.dot(normal, centro) < 0:
        normal = -normal
    eixo_x = vertices[ids[0]] - centro
    eixo_x = eixo_x / np.linalg.norm(eixo_x)
    eixo_y = np.cross(normal / np.linalg.norm(normal), eixo_x)
    angulos = [
        math.atan2(
            float(np.dot(vertices[i] - centro, eixo_y)),
            float(np.dot(vertices[i] - centro, eixo_x)),
        )
        for i in ids
    ]
    return [i for _, i in sorted(zip(angulos, ids, strict=True))]


def _faces_dodecaedro(
    vertices: list[np.ndarray],
) -> list[list[int]]:
    """Descobre as 12 faces pentagonais do dodecaedro a partir dos vértices.

    :param vertices: 20 vértices do dodecaedro.
    :returns: Lista de 12 listas de 5 índices (em ordem anti-horária).
    """
    vizinhos = _adjacencia_dodecaedro(vertices)
    ciclos = _ciclos_pentagonais(len(vertices), vizinhos)
    return [_ordena_pentagono(list(face), vertices) for face in ciclos]


def _uv_pentagono(
    vertices_3d: list[np.ndarray],
    centro: np.ndarray,
    normal: np.ndarray,
) -> list[tuple[float, float]]:
    """Calcula coordenadas UV (0..1) para um pentágono projetado no plano local.

    :param vertices_3d: 5 vértices do pentágono em coordenadas 3D.
    :param centro: Centro do pentágono.
    :param normal: Normal da face (apontando para fora).
    :returns: Lista de 5 tuplas ``(u, v)`` normalizadas em ``[0, 1]``.
    """
    normal_u = normal / np.linalg.norm(normal)
    eixo_x = vertices_3d[0] - centro
    eixo_x = eixo_x / np.linalg.norm(eixo_x)
    eixo_y = np.cross(normal_u, eixo_x)
    coords_2d = []
    for v in vertices_3d:
        rel = v - centro
        coords_2d.append((float(np.dot(rel, eixo_x)), float(np.dot(rel, eixo_y))))
    min_x = min(c[0] for c in coords_2d)
    max_x = max(c[0] for c in coords_2d)
    min_y = min(c[1] for c in coords_2d)
    max_y = max(c[1] for c in coords_2d)
    rng_x = max_x - min_x if max_x > min_x else 1.0
    rng_y = max_y - min_y if max_y > min_y else 1.0
    # Margem para evitar bleeding de textura nas bordas UV 0/1.
    margem = 0.01
    return [
        (
            margem + (1 - 2 * margem) * (c[0] - min_x) / rng_x,
            margem + (1 - 2 * margem) * (c[1] - min_y) / rng_y,
        )
        for c in coords_2d
    ]


def cria_face_pentagono(
    vertices_ext: list[np.ndarray],
    centro: np.ndarray,
    normal: np.ndarray,
    profundidade: float,
    textura,
) -> py5.Py5Shape:
    """Cria um slab pentagonal com textura em todas as faces.

    O pentágono externo fica deslocado ``+profundidade/2`` ao longo da normal;
    o pentágono interno fica em ``-profundidade/2``. Ambos e as 5 laterais
    recebem a textura mapeada com UV completo.

    :param vertices_ext: 5 vértices do pentágono (em coordenadas 3D mundo).
    :param centro: Centro geométrico da face.
    :param normal: Normal unitária da face (apontando para fora).
    :param profundidade: Espessura do slab.
    :param textura: Py5Graphics aplicado em todas as faces.
    :returns: Py5Shape com o slab pentagonal texturizado.
    """
    normal_u = normal / np.linalg.norm(normal)
    d = profundidade / 2
    ext = [v + normal_u * d for v in vertices_ext]
    inn = [v - normal_u * d for v in vertices_ext]

    uvs = _uv_pentagono(vertices_ext, centro, normal)
    cx = sum(u for u, _ in uvs) / 5
    cy = sum(v for _, v in uvs) / 5

    grupo = py5.create_shape(py5.GROUP)

    # Face externa (TRIANGLE_FAN a partir do centro).
    face_ext = py5.create_shape()
    with face_ext.begin_shape(py5.TRIANGLE_FAN):
        face_ext.no_stroke()
        face_ext.fill(255)
        face_ext.texture_mode(py5.NORMAL)
        face_ext.texture(textura)
        face_ext.vertex(
            float(centro[0] + normal_u[0] * d),
            float(centro[1] + normal_u[1] * d),
            float(centro[2] + normal_u[2] * d),
            cx,
            cy,
        )
        for i in range(5):
            face_ext.vertex(
                float(ext[i][0]),
                float(ext[i][1]),
                float(ext[i][2]),
                uvs[i][0],
                uvs[i][1],
            )
        # Fechar o fan.
        face_ext.vertex(
            float(ext[0][0]),
            float(ext[0][1]),
            float(ext[0][2]),
            uvs[0][0],
            uvs[0][1],
        )
    grupo.add_child(face_ext)

    # Face interna (TRIANGLE_FAN, ordem inversa).
    face_inn = py5.create_shape()
    with face_inn.begin_shape(py5.TRIANGLE_FAN):
        face_inn.no_stroke()
        face_inn.fill(255)
        face_inn.texture_mode(py5.NORMAL)
        face_inn.texture(textura)
        face_inn.vertex(
            float(centro[0] - normal_u[0] * d),
            float(centro[1] - normal_u[1] * d),
            float(centro[2] - normal_u[2] * d),
            cx,
            cy,
        )
        for i in range(4, -1, -1):
            face_inn.vertex(
                float(inn[i][0]),
                float(inn[i][1]),
                float(inn[i][2]),
                uvs[i][0],
                uvs[i][1],
            )
        face_inn.vertex(
            float(inn[4][0]),
            float(inn[4][1]),
            float(inn[4][2]),
            uvs[4][0],
            uvs[4][1],
        )
    grupo.add_child(face_inn)

    # 5 laterais (QUADS) — cor metálica com normais para iluminação.
    cor_metalica = py5.color(180, 180, 195)
    for i in range(5):
        j = (i + 1) % 5
        # Normal da lateral: perpendicular à aresta e à normal da face.
        aresta = ext[j] - ext[i]
        lateral_normal = np.cross(aresta, normal_u)
        norm_len = np.linalg.norm(lateral_normal)
        if norm_len > 0:
            lateral_normal = lateral_normal / norm_len
        nx = float(lateral_normal[0])
        ny = float(lateral_normal[1])
        nz = float(lateral_normal[2])
        quad = py5.create_shape()
        with quad.begin_shape(py5.QUADS):
            quad.no_stroke()
            quad.fill(cor_metalica)
            quad.shininess(80)
            quad.specular(220, 220, 230)
            quad.emissive(15, 15, 20)
            quad.normal(nx, ny, nz)
            quad.vertex(float(ext[i][0]), float(ext[i][1]), float(ext[i][2]))
            quad.vertex(float(ext[j][0]), float(ext[j][1]), float(ext[j][2]))
            quad.vertex(float(inn[j][0]), float(inn[j][1]), float(inn[j][2]))
            quad.vertex(float(inn[i][0]), float(inn[i][1]), float(inn[i][2]))
        grupo.add_child(quad)

    return grupo


def gera_faces(
    textura,
) -> list[tuple[py5.Py5Shape, np.ndarray]]:
    """Gera as 12 faces pentagonais do dodecaedro como slabs texturizados.

    Cada face é um slab pentagonal posicionado em coordenadas absolutas. A
    normal unitária é guardada para aplicar o deslocamento de explosão no
    momento do desenho.

    :param textura: Py5Graphics aplicado em todas as faces de cada slab.
    :returns: Lista ``[(shape, normal_unitaria), ...]`` com 12 entradas.
    """
    vertices = _vertices_dodecaedro(raio_dodecaedro)
    faces_idx = _faces_dodecaedro(vertices)
    resultado = []
    for ids in faces_idx:
        verts = [vertices[i] for i in ids]
        centro = sum(verts, np.zeros(3)) / 5
        normal = centro / np.linalg.norm(centro)
        forma = cria_face_pentagono(
            verts,
            centro,
            normal,
            profundidade_face,
            textura,
        )
        resultado.append((forma, normal))
    return resultado


def setup():
    """Inicializa o sketch: cria a janela, calcula grade e padrões."""
    global imagem, faces
    py5.size(*helpers.DIMENSOES.external, py5.P3D)
    py5.background(cor_fundo)
    imagem = gera_imagem(inicializa_celulas())
    faces = gera_faces(imagem)


def draw():
    """Renderiza todas as células e adiciona os créditos do sketch."""
    py5.background(cor_fundo)

    with py5.push():
        py5.translate(*helpers.DIMENSOES.centro, rotacao.dist_z)
        py5.rotate_y(float(py5.radians(rotacao.y)))
        py5.rotate_x(float(py5.radians(rotacao.x)))
        py5.rotate_z(float(py5.radians(rotacao.z)))
        # Luz pontual no centro do dodecaedro.
        py5.point_light(255, 250, 240, 0, 0, 0)
        for forma, normal in faces:
            with py5.push():
                # Empurra cada face ao longo da sua normal para fora.
                deslocamento = normal * rotacao.explosao
                py5.translate(
                    float(deslocamento[0]),
                    float(deslocamento[1]),
                    float(deslocamento[2]),
                )
                py5.shape(forma)
    msg = (
        f"R: {rotacao.x:.1f}, {rotacao.y:.1f}, {rotacao.z:.1f} | "
        f"Z: {rotacao.dist_z} | "
        f"E: {rotacao.explosao}"
    )
    # Resetar iluminação para o frame não ser afetado pela point_light.
    py5.no_lights()
    canvas.sketch_frame(
        sketch,
        cor_fundo,
        "large_transparent_white",
        "transparent_white",
        version=2,
        msg=msg,
    )


def trata_tecla(key: str) -> None:
    """Trata teclas de caractere: salvar, regenerar, zoom e explosão."""
    global imagem, faces
    match key:
        case " ":
            save_and_close()
        case "r":
            imagem = gera_imagem(inicializa_celulas())
            faces = gera_faces(imagem)
        case "+":
            rotacao.dist_z += 100
        case "-":
            rotacao.dist_z -= 100
        case "]":
            rotacao.explosao += 10
        case "[":
            rotacao.explosao = max(0, rotacao.explosao - 10)


def key_pressed():
    """Captura teclas: ``espaço`` salva e fecha o sketch."""
    trata_tecla(py5.key)
    match py5.key_code:
        case py5.UP:
            rotacao.x += 3
        case py5.DOWN:
            rotacao.x -= 3
        case py5.LEFT:
            rotacao.y += 3
        case py5.RIGHT:
            rotacao.y -= 3


def save_and_close():
    """Para o loop, salva a imagem do sketch e encerra."""
    py5.no_loop()
    canvas.save_sketch_image(sketch)
    py5.exit_sketch()


if __name__ == "__main__":
    py5.run_sketch()
