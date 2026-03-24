"""2026-03-24
Esfera de Retalhos 05
Esfera formada por um cilindro com gradientes de cores diversas
ericof.com
png
Sketch,py5,CreativeCoding
"""

from collections import deque
from collections.abc import Mapping
from dataclasses import dataclass
from random import shuffle
from sketches.utils.draw import canvas
from sketches.utils.draw.cores import lerp_color_rgba
from sketches.utils.draw.cores.paletas import gera_paleta
from sketches.utils.draw.cores.paletas import lista_paletas
from sketches.utils.helpers import sketches as helpers

import numpy as np
import py5


sketch = helpers.info_for_sketch(__file__, __doc__)

cor_fundo = py5.color(0)

z_factor = 0.04

paletas = [
    gera_paleta(name, True) for name in lista_paletas() if name.startswith("op-")
]


@dataclass
class EsferaRotacao:
    x: float = -15
    y: float = 45
    z: float = 0
    dist_z: float = -2000


rotacao = EsferaRotacao()
forma: py5.Py5Shape
cilindro_polos: py5.Py5Shape


def gera_caminho_espiral(raio: float, num_pontos: int, n_sub: int) -> np.ndarray:
    """Gera caminho denso da espiral Fibonacci sobre a superfície da esfera.

    Trata o índice como parâmetro contínuo — sem interpolação externa.
    Produz (num_pontos - 1) * n_sub + 1 pontos na superfície.

    :param n_sub: amostras entre cada par de pontos Fibonacci consecutivos.
    :return: array (total, 3)
    """
    angulo_dourado = np.pi * (3.0 - np.sqrt(5.0))
    total = (num_pontos - 1) * n_sub + 1
    t = np.linspace(0.0, num_pontos - 1, total)
    y = 1.0 - (2.0 * t) / (num_pontos - 1)
    raio_xy = np.sqrt(np.maximum(0.0, 1.0 - y * y))
    theta = angulo_dourado * t
    coords = np.stack([np.cos(theta) * raio_xy, y, np.sin(theta) * raio_xy], axis=-1)
    return coords * raio


def gera_caminho_bezier_cubico(
    p0: np.ndarray,
    p1: np.ndarray,
    p2: np.ndarray,
    p3: np.ndarray,
    n: int,
) -> np.ndarray:
    """Gera n pontos ao longo de uma curva Bézier cúbica."""
    t = np.linspace(0.0, 1.0, n)[:, None]
    return (
        (1 - t) ** 3 * p0
        + 3 * (1 - t) ** 2 * t * p1
        + 3 * (1 - t) * t**2 * p2
        + t**3 * p3
    )


def _gera_frames_caminho(centers: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Gera frames locais (normais, binormais) via parallel transport."""
    n = len(centers)
    tangents = np.empty_like(centers)
    tangents[1:-1] = centers[2:] - centers[:-2]
    tangents[0] = centers[1] - centers[0]
    tangents[-1] = centers[-1] - centers[-2]
    tangents /= np.linalg.norm(tangents, axis=-1, keepdims=True).clip(1e-10)

    t0 = tangents[0]
    up = np.array([0.0, 1.0, 0.0]) if abs(t0[1]) < 0.9 else np.array([1.0, 0.0, 0.0])
    normal = np.cross(t0, up)
    normal /= np.linalg.norm(normal)

    normals = np.empty_like(centers)
    normals[0] = normal
    for i in range(1, n):
        t = tangents[i]
        normal = normals[i - 1] - np.dot(normals[i - 1], t) * t
        norm = np.linalg.norm(normal)
        if norm < 1e-10:
            normal = np.cross(t, np.array([0.0, 0.0, 1.0]))
            norm = np.linalg.norm(normal)
        normals[i] = normal / norm

    binormals = np.cross(tangents, normals)
    return normals, binormals


def gera_aneis_cilindro(
    raio: float, raio_tubo: float, num_pontos: int, num_lados: int, n_sub: int
) -> np.ndarray:
    """Gera anéis circulares ao longo da espiral Fibonacci densa.

    :return: array (total, num_lados, 3)
    """
    caminho = gera_caminho_espiral(raio, num_pontos, n_sub)
    normals, binormals = _gera_frames_caminho(caminho)
    phi = np.linspace(0, 2 * np.pi, num_lados, endpoint=False)
    return caminho[:, None, :] + raio_tubo * (
        np.cos(phi)[None, :, None] * normals[:, None, :]
        + np.sin(phi)[None, :, None] * binormals[:, None, :]
    )


def _cor_int(c: str | int) -> int:
    """Converte valor de paleta para inteiro de cor py5."""
    return c if isinstance(c, int) else py5.color(c)


def _monta_grupo_cilindro(
    aneis: np.ndarray,
    paletas_forma: Mapping[str, deque[str | int]],
) -> py5.Py5Shape:
    """Monta um GROUP de faces quádruplas a partir de anéis pré-calculados.

    Atribui uma cor por anel e usa set_fills/set_strokes por vértice,
    produzindo gradiente suave ao longo do eixo do cilindro.
    """
    n_aneis, num_lados, _ = aneis.shape
    key = "preenchimento"
    pal = paletas_forma[key]

    pal_len = len(pal)
    direction = -1
    cores_anel = [_cor_int(pal[0])]
    for step in range(1, n_aneis):
        pal.rotate(direction)
        if step % pal_len == 0:
            direction = -direction
            pal.rotate(direction * (pal_len // 3))
        cores_anel.append(_cor_int(pal[0]))

    grupo = py5.create_shape(py5.GROUP)
    for i in range(n_aneis - 1):
        ci, cj = cores_anel[i], cores_anel[i + 1]
        bi = lerp_color_rgba(ci, py5.color("#000"), t=0.15)
        bj = lerp_color_rgba(cj, py5.color("#000"), t=0.15)

        for j in range(num_lados):
            j_next = (j + 1) % num_lados
            p0, p1 = aneis[i, j], aneis[i, j_next]
            p2, p3 = aneis[i + 1, j_next], aneis[i + 1, j]

            face = py5.create_shape()
            with face.begin_closed_shape():
                face.vertex(*p0)
                face.vertex(*p1)
                face.vertex(*p2)
                face.vertex(*p3)
            face.set_fills([ci, ci, cj, cj])
            face.set_strokes([bi, bi, bj, bj])
            grupo.add_child(face)

    return grupo


def criar_forma(
    raio: float,
    num_pontos: int,
    paletas_forma: Mapping[str, deque[str | int]],
    raio_tubo: float = 80.0,
    num_lados: int = 8,
    n_sub: int = 8,
) -> py5.Py5Shape:
    """Cria um cilindro em espiral sobre a esfera, do polo N ao polo S."""
    aneis = gera_aneis_cilindro(raio, raio_tubo, num_pontos, num_lados, n_sub)
    return _monta_grupo_cilindro(aneis, paletas_forma)


def criar_cilindro_polos(
    raio: float,
    paletas_forma: Mapping[str, deque[str | int]],
    raio_tubo: float = 30.0,
    num_lados: int = 16,
    curva: float = 0.3,
    n_pontos: int = 60,
) -> py5.Py5Shape:
    """Cria um cilindro curvado unindo o polo N ao polo S pelo interior da esfera.

    Usa uma Bézier cúbica em S: os dois pontos de controle ficam em lados
    opostos do eixo vertical, produzindo uma curva suave e simétrica.
    No ponto médio (t=0.5) o cilindro passa exatamente pelo centro da esfera.

    :param curva: deslocamento lateral dos controles como fração do raio.
    """
    p_norte = np.array([0.0, float(raio), 0.0])
    ctrl1 = np.array([curva * raio, raio / 3.0, 0.0])
    ctrl2 = np.array([-curva * raio, -raio / 3.0, 0.0])
    p_sul = np.array([0.0, -float(raio), 0.0])

    caminho = gera_caminho_bezier_cubico(p_norte, ctrl1, ctrl2, p_sul, n_pontos)
    normals, binormals = _gera_frames_caminho(caminho)

    phi = np.linspace(0, 2 * np.pi, num_lados, endpoint=False)
    aneis = caminho[:, None, :] + raio_tubo * (
        np.cos(phi)[None, :, None] * normals[:, None, :]
        + np.sin(phi)[None, :, None] * binormals[:, None, :]
    )
    return _monta_grupo_cilindro(aneis, paletas_forma)


def inicializa():
    global forma, cilindro_polos
    local_paletas = paletas[:]
    shuffle(local_paletas)

    paletas_espiral: dict[str, deque[str | int]] = {
        "preenchimento": deque(local_paletas[0]),
    }
    forma = criar_forma(800, 60, paletas_espiral, raio_tubo=30.0, num_lados=16, n_sub=8)

    paletas_polos: dict[str, deque[str | int]] = {
        "preenchimento": deque(local_paletas[1]),
    }
    cilindro_polos = criar_cilindro_polos(800, paletas_polos)


def setup():
    py5.size(*helpers.DIMENSOES.external, py5.P3D)
    inicializa()


def draw():
    py5.background(cor_fundo)
    with py5.push():
        py5.translate(*helpers.DIMENSOES.centro, rotacao.dist_z)
        py5.rotate_y(py5.radians(rotacao.y))
        py5.rotate_x(py5.radians(rotacao.x))
        py5.rotate_z(py5.radians(rotacao.z))
        py5.shape(forma)
        py5.shape(cilindro_polos)

    # Créditos e encerramento
    canvas.sketch_frame(
        sketch,
        cor_fundo,
        "large_transparent_white",
        "transparent_white",
        version=2,
    )


def key_pressed():
    key = py5.key
    match py5.key:
        case " ":
            save_and_close()
        case "r":
            inicializa()
        case "+":
            rotacao.dist_z += 50
        case "-":
            rotacao.dist_z -= 50
    match py5.key_code:
        case py5.UP:
            rotacao.x += 3
        case py5.DOWN:
            rotacao.x -= 3
        case py5.LEFT:
            rotacao.y += 3
        case py5.RIGHT:
            rotacao.y -= 3
    if key == " ":
        save_and_close()


def save_and_close():
    py5.no_loop()
    canvas.save_sketch_image(sketch)
    py5.exit_sketch()


if __name__ == "__main__":
    py5.run_sketch()
