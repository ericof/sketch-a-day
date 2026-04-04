"""2026-04-04
Maria is 13
Pixelado de corações aplicado sobre foto da minha filha Maria
ericof.com
png
Sketch,py5,CreativeCoding
"""

from collections.abc import Callable
from dataclasses import dataclass
from sketches.utils.draw import canvas
from sketches.utils.draw.cores import rgb_to_hsb
from sketches.utils.helpers import sketches as helpers
from sketches.utils.helpers.images import image_as_array
from sketches.utils.helpers.recursos import caminho_arquivo
from sketches.utils.helpers.window import title

import numpy as np
import py5


sketch = helpers.info_for_sketch(__file__, __doc__)

cor_fundo = py5.color(0)
largura, altura = helpers.DIMENSOES.internal

TAM_PIXEL: int = 8


@dataclass
class CentroPixelado:
    dx: int = 24
    dy: int = -39


FOCO = CentroPixelado()


def pixelar(
    img_array: np.ndarray,
    tam_pixel: int = 24,
    largura: int = helpers.DIMENSOES.internal[0],
    altura: int = helpers.DIMENSOES.internal[1],
    func: Callable[..., np.ndarray] = np.median,
) -> list[tuple[int, int, int, int, tuple[float, float, float]]]:
    """Amostra a imagem em blocos e converte cada bloco para cor HSB.

    :param img_array: Array NumPy da imagem (H, W, C).
    :param tam_pixel: Tamanho do bloco de amostragem em pixels.
    :param largura: Largura da área a amostrar.
    :param altura: Altura da área a amostrar.
    :param func: Função de agregação por bloco (ex: ``np.average``).
    :returns: Lista de tuplas ``(idx, idy, x, y, (h, s, b))``.
    """
    pontos = []
    for idx, x in enumerate(range(0, largura, tam_pixel)):
        for idy, y in enumerate(range(0, altura, tam_pixel)):
            bloco = img_array[y : y + tam_pixel, x : x + tam_pixel]
            cor = func(bloco, axis=(0, 1))
            h, s, b = rgb_to_hsb(cor[0], cor[1], cor[2])
            pontos.append((idx, idy, x, y, (h, s, b)))
    return pontos


def calcula_raio(centro_x: float, centro_y: float, idx: int, idy: int) -> float:
    """Calcula fator de escala radial (gaussiano) para uma célula da grade.

    Células próximas ao centro recebem raio maior (até 1.0),
    células nas bordas recebem raio menor (mínimo ``base``).

    :param centro_x: Índice central da grade no eixo X.
    :param centro_y: Índice central da grade no eixo Y.
    :param idx: Índice da célula no eixo X.
    :param idy: Índice da célula no eixo Y.
    :returns: Fator de escala entre 0.2 e 0.75.
    """
    banda = min(centro_x, centro_y) * 1.8
    base = 0.2
    topo = 0.75
    mult = 1 / base
    dx = idx - centro_x
    dy = idy - centro_y
    distancia = dx**2 + dy**2
    valor = np.exp(-distancia / (mult * banda**2))
    return base + (topo - base) * valor


def inicializa() -> None:
    """Carrega a imagem e calcula os pontos pixelados para as esferas."""
    global pontos
    with title("Carregando imagem"):
        caminho = caminho_arquivo("2026-maria.jpg")
        img_array = image_as_array(caminho)
    with title("Calculando pontos para esferas 3D"):
        pontos = pixelar(
            img_array,
            TAM_PIXEL,
            largura,
            altura,
            np.average,
        )


def desenha_coracao(tamanho: float) -> None:
    """Desenha um coração centralizado na origem usando curvas de Bézier.

    :param tamanho: Tamanho (diâmetro aproximado) do coração.
    """
    s = tamanho / 2
    py5.begin_shape()
    py5.vertex(0, s)  # ponta inferior
    py5.bezier_vertex(-s, 0, -s, -s, 0, -s * 0.5)  # lado esquerdo
    py5.bezier_vertex(s, -s, s, 0, 0, s)  # lado direito
    py5.end_shape(py5.CLOSE)


def desenha_imagem() -> None:
    """Desenha a imagem pixelada como corações."""
    centro_x = (largura / TAM_PIXEL) / 2 + FOCO.dx
    centro_y = (altura / TAM_PIXEL) / 2 + FOCO.dy
    with py5.push():
        py5.translate(*helpers.DIMENSOES.centro)
        py5.no_stroke()
        for idx, idy, xb, yb, cor in pontos:
            x = idx * TAM_PIXEL - largura // 2
            y = idy * TAM_PIXEL - altura // 2
            if idx == idy == 10:
                print(xb, x, yb, y)
            raio = calcula_raio(centro_x, centro_y, idx, idy)
            with py5.push():
                py5.translate(x, y)
                py5.fill(*cor)
                desenha_coracao(TAM_PIXEL * raio * 2)


def setup() -> None:
    """Inicializa o sketch: carrega imagem, pixela e desenha esferas 3D."""
    py5.size(*helpers.DIMENSOES.external, py5.P3D)
    py5.color_mode(py5.HSB, 360, 100, 100)
    inicializa()


def draw() -> None:
    """Renderiza o frame: fundo, esferas e créditos."""
    py5.background(cor_fundo)
    with title(f"Desenhando reticulado {TAM_PIXEL}px {FOCO.dx},{FOCO.dy}"):
        desenha_imagem()
    # Credits and go
    canvas.sketch_frame(
        sketch,
        cor_fundo,
        "large_transparent_white",
        "transparent_white",
        version=2,
    )


def key_pressed() -> None:
    """Captura teclas: ``espaço`` salva, ``+``/``-`` ajusta tamanho do pixel."""
    global TAM_PIXEL
    key = py5.key
    match key:
        case " ":
            save_and_close()
        case "+":
            TAM_PIXEL += 1
            inicializa()
        case "-":
            TAM_PIXEL -= 1
            inicializa()
    match py5.key_code:
        case py5.UP:
            FOCO.dy -= 3
        case py5.DOWN:
            FOCO.dy += 3
        case py5.LEFT:
            FOCO.dx -= 3
        case py5.RIGHT:
            FOCO.dx += 3


def save_and_close() -> None:
    """Para o loop, salva a imagem do sketch e encerra."""
    py5.no_loop()
    canvas.save_sketch_image(sketch)
    py5.exit_sketch()


if __name__ == "__main__":
    py5.run_sketch()
