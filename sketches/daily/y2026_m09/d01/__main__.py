"""2026-09-01
Zooming Out 03/06
Experimentando com pixelização de imagens e zoom interativo.
ericof.com
png
Sketch,py5,CreativeCoding,Basketball
"""

from collections.abc import Callable
from dataclasses import dataclass
from dataclasses import replace
from sketches.padroes.poligonos import gera_poligono_regular
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
imagem: py5.Py5Graphics
pontos: list[tuple[int, int, int, int, tuple[float, float, float]]] = []
selecao_centro: tuple[int, int] | None = None


@dataclass
class Zoom:
    cx: int = 500
    cy: int = 360
    lado: int = 300


TAM_PIXEL: int = 4
ZOOM_INICIAL = Zoom()
ZOOM = replace(ZOOM_INICIAL)
LADOS: int = 8
ARQUIVO_IMAGEM: str = "basketball.jpg"


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


def regiao_zoom(zoom: Zoom) -> tuple[int, int, int, int]:
    """Calcula o recorte de ``zoom`` em coordenadas da área interna.

    O lado é limitado ao tamanho da área interna e o centro é deslocado para
    dentro dela quando fica perto de uma borda, de modo que o recorte continue
    quadrado.

    :param zoom: Recorte desejado, em coordenadas da área interna.
    :returns: Tupla ``(u1, v1, u2, v2)`` com os cantos do recorte.
    """
    lado = max(TAM_PIXEL, min(zoom.lado, largura, altura))
    meio = lado // 2
    cx = min(max(zoom.cx, meio), largura - meio)
    cy = min(max(zoom.cy, meio), altura - meio)
    return cx - meio, cy - meio, cx + meio, cy + meio


def desenha_zoom(
    pontos: list[tuple[int, int, int, int, tuple[float, float, float]]],
    zoom: Zoom,
) -> py5.Py5Graphics:
    """Desenha o recorte de ``zoom`` preenchendo a área interna.

    Cada bloco amostrado vira um polígono regular já desenhado na escala final,
    em vez de um pixel ampliado depois — é o que mantém a borda nítida em
    qualquer nível de zoom.

    :param pontos: Lista de tuplas ``(idx, idy, x, y, (h, s, b))``.
    :param zoom: Recorte a desenhar.
    :returns: Camada do tamanho da área interna, com fundo transparente.
    """
    u1, v1, u2, v2 = regiao_zoom(zoom)
    escala = largura / (u2 - u1)
    tamanho = TAM_PIXEL * escala
    forma = gera_poligono_regular(
        lados=LADOS, largura=tamanho, altura=tamanho, rotacao=py5.PI / LADOS
    )
    forma.disable_style()
    pg = py5.create_graphics(largura, altura, py5.P3D)
    with pg.begin_draw():
        pg.color_mode(py5.HSB, 360, 100, 100)
        pg.clear()
        for _idx, _idy, x, y, cor in pontos:
            if not (u1 <= x < u2 and v1 <= y < v2):
                continue
            with pg.push():
                pg.translate((x - u1) * escala, (y - v1) * escala)
                pg.fill(*cor)
                pg.stroke(*cor)
                pg.shape(forma)
    return pg


def atualiza_zoom(novo: Zoom) -> None:
    """Aplica um novo recorte e redesenha a camada na escala correspondente.

    :param novo: Recorte a passar a valer.
    """
    global ZOOM, imagem
    ZOOM = novo
    with title(f"Desenhando {novo.cx}, {novo.cy}, {novo.lado}"):
        imagem = desenha_zoom(pontos, novo)
    print(f"ZOOM = {ZOOM}")


def inicializa() -> None:
    """Carrega a imagem de origem e amostra os blocos em ``pontos``."""
    global pontos
    with title("Carregando imagem"):
        caminho = caminho_arquivo(ARQUIVO_IMAGEM)
        img_array = image_as_array(caminho)
    with title("Calculando pontos"):
        pontos = pixelar(
            img_array,
            TAM_PIXEL,
            largura,
            altura,
            np.average,
        )


def setup():
    py5.size(*helpers.DIMENSOES.external, py5.P3D)
    py5.color_mode(py5.HSB, 360, 100, 100)
    inicializa()
    atualiza_zoom(ZOOM)


def draw():
    py5.background(cor_fundo)
    with py5.push():
        py5.translate(*helpers.DIMENSOES.pos_interno)
        d = py5.display_density()
        py5.image(imagem, 0, 0, largura * d, altura * d)
    msg = f"ZOOM: {ZOOM.cx}, {ZOOM.cy}, {ZOOM.lado}"
    # Credits and go
    canvas.sketch_frame(
        sketch,
        cor_fundo,
        "large_transparent_white",
        "transparent_white",
        version=2,
        msg=msg,
    )


def pos_interna(x: int, y: int) -> tuple[int, int]:
    """Converte coordenadas do canvas para coordenadas da área interna.

    :param x: Coordenada x no canvas externo.
    :param y: Coordenada y no canvas externo.
    :returns: Tupla ``(x, y)`` relativa a ``DIMENSOES.pos_interno``.
    """
    origem_x, origem_y = helpers.DIMENSOES.pos_interno
    return x - origem_x, y - origem_y


def mouse_pressed():
    global selecao_centro
    if py5.mouse_button != py5.LEFT:
        return
    selecao_centro = pos_interna(py5.mouse_x, py5.mouse_y)
    print(f"centro: {selecao_centro[0]}, {selecao_centro[1]}")


def mouse_released():
    if py5.mouse_button != py5.LEFT or selecao_centro is None:
        return
    cx, cy = selecao_centro
    x, y = pos_interna(py5.mouse_x, py5.mouse_y)
    meio_lado = max(abs(x - cx), abs(y - cy))
    if meio_lado == 0:
        return
    atualiza_zoom(Zoom(cx, cy, meio_lado * 2))


def key_pressed():
    key = py5.key
    match key:
        case " ":
            save_and_close()
        case "r":
            atualiza_zoom(replace(ZOOM_INICIAL))


def save_and_close():
    py5.no_loop()
    canvas.save_sketch_image(sketch)
    py5.exit_sketch()


if __name__ == "__main__":
    py5.run_sketch()
