"""2026-03-21
Esfera de Retalhos 02
Esfera formada por folhas orgânicas de cores diversas
ericof.com
png
Sketch,py5,CreativeCoding
"""

from collections import deque
from dataclasses import dataclass
from sketches.utils.draw import canvas
from sketches.utils.draw.cores.paletas import gera_paleta
from sketches.utils.draw.cores.paletas import lista_paletas
from sketches.utils.draw.esfera import pontos_esfera
from sketches.utils.helpers import sketches as helpers

import numpy as np
import py5


sketch = helpers.info_for_sketch(__file__, __doc__)

cor_fundo = py5.color(0)

z_factor = 0.02

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


def calcula_coordenadas(xb: float, yb: float, zb: float) -> tuple[float, float, float]:
    mult = py5.random(1 - z_factor, 1 + z_factor)
    return xb, yb, zb * mult


def calcula_vetores_largura(pontos: np.ndarray) -> np.ndarray:
    """Calcula vetores perpendiculares à espinha de cada folha e à superfície da esfera.

    O vetor resultante aponta "para o lado" de cada ponto, garantindo espessura
    3D independente da posição na esfera (equador, polo, etc).
    """
    total = len(pontos)
    vetores = np.empty_like(pontos)
    for i in range(total):
        # espinha local: direção ao longo da sequência de pontos
        espinha = pontos[(i + 1) % total] - pontos[(i - 1) % total]
        # produto vetorial com o vetor radial (normal à superfície da esfera)
        w = np.cross(espinha, pontos[i])
        norm = np.linalg.norm(w)
        vetores[i] = w / norm if norm > 1e-6 else np.array([0.0, 0.0, 1.0])
    return vetores


def criar_forma(pontos, local_paletas, largura: float = 10) -> py5.Py5Shape:
    """Cria a forma composta por folhas orgânicas sobre a esfera."""
    pts = np.array(pontos)
    # vetores de largura pré-calculados por ponto — garante conexão
    # entre folhas adjacentes
    vetores = calcula_vetores_largura(pts) * largura
    forma = py5.create_shape(py5.GROUP)
    total = len(pts)
    for idx in range(0, total, 2):
        i1, im, i2 = idx % total, (idx + 1) % total, (idx + 2) % total
        p1, wv1 = pts[i1], vetores[i1]
        pm, wvm = pts[im], vetores[im]
        p2, wv2 = pts[i2], vetores[i2]

        paleta = local_paletas[0]
        cor_borda = paleta[0]
        paleta.rotate()
        cor_preench = paleta[0]

        folha = py5.create_shape()
        with folha.begin_closed_shape():
            # borda frontal: p1 → p2 curvando por pm (offset positivo)
            folha.vertex(*(p1 + wv1))
            folha.quadratic_vertex(*(pm + wvm), *(p2 + wv2))
            # borda traseira: p2 → p1 curvando por pm (offset negativo)
            folha.vertex(*(p2 - wv2))
            folha.quadratic_vertex(*(pm - wvm), *(p1 - wv1))
        folha.set_stroke(cor_borda)
        folha.set_fill(cor_preench)
        forma.add_child(folha)
        local_paletas.rotate()
    return forma


def setup():
    global forma
    py5.size(*helpers.DIMENSOES.external, py5.P3D)
    pontos = pontos_esfera(800, 200)
    local_paletas = deque(paletas[:])
    forma = criar_forma(pontos, local_paletas, largura=50)


def draw():
    py5.background(cor_fundo)
    with py5.push():
        py5.translate(*helpers.DIMENSOES.centro, rotacao.dist_z)
        py5.rotate_y(py5.radians(rotacao.y))
        py5.rotate_x(py5.radians(rotacao.x))
        py5.rotate_z(py5.radians(rotacao.z))
        py5.shape(forma)

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
