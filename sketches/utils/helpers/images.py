from pathlib import Path
from PIL import Image

import cv2
import numpy as np
import py5
import sketches
import tempfile


ROOT_FOLDER = Path(sketches.__file__).parent
RESOURCES_FOLDER = ROOT_FOLDER / "_resources"

__all__ = [
    "contornos_da_mascara",
    "estencil_como_forma",
    "image_as_array",
    "resource_image_as_array",
    "save_frame",
]


def image_as_array(path: Path) -> np.ndarray:
    """Abre um arquivo de imagem e retorna como array NumPy.

    :param path: Caminho do arquivo de imagem.
    :returns: Array NumPy com os dados da imagem.
    """
    image = Image.open(path)
    return np.array(image)


def resource_image_as_array(filename: str) -> np.ndarray:
    """Abre uma imagem da pasta de recursos e retorna como array NumPy.

    :param filename: Nome do arquivo na pasta de recursos.
    :returns: Array NumPy com os dados da imagem.
    """
    path = RESOURCES_FOLDER / filename
    return image_as_array(path)


def tmp_path() -> Path:
    """Cria e retorna o caminho de um diretório temporário.

    :returns: Caminho do diretório temporário criado.
    """
    return Path(tempfile.mkdtemp())


def save_frame(tmp_path: Path, img_name: str, frame: int) -> Path:
    """Salva o frame atual do py5 como imagem PNG.

    :param tmp_path: Diretório temporário para salvar o frame.
    :param img_name: Nome base do arquivo de imagem.
    :param frame: Número do frame.
    :returns: Caminho do arquivo PNG salvo.
    """
    path = tmp_path / f"{img_name}_{frame:03d}.png"
    py5.save_frame(path)
    return path


def contornos_da_mascara(
    arr: np.ndarray, limiar: int = 127, epsilon: float = 2.0
) -> list[list[tuple[float, float]]]:
    """Extrai os contornos poligonais da regiao transparente de uma mascara RGBA.

    Limiariza o canal alpha e simplifica cada contorno externo da regiao
    transparente (``alpha <= limiar``) com Douglas-Peucker.

    :param arr: Mascara RGBA no formato ``(h, w, 4)``.
    :param limiar: Corte de alpha; pixels com alpha menor ou igual viram recorte.
    :param epsilon: Tolerancia da simplificacao, em pixels.
    :returns: Lista de contornos, cada um uma lista de vertices ``(x, y)``.
    """
    transp = (arr[:, :, 3] <= limiar).astype(np.uint8) * 255
    cnts, _ = cv2.findContours(transp, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    poligonos = []
    for c in cnts:
        ap = cv2.approxPolyDP(c, epsilon, True).reshape(-1, 2)
        poligonos.append([(float(x), float(y)) for x, y in ap])
    return poligonos


def _area_assinada(poly: list[tuple[float, float]]) -> float:
    """Area assinada (shoelace) de um poligono; o sinal indica a orientacao.

    :param poly: Vertices ``(x, y)`` do poligono.
    :returns: Area assinada -- o sinal revela o sentido de giro do contorno.
    """
    s = 0.0
    n = len(poly)
    for i in range(n):
        x0, y0 = poly[i]
        x1, y1 = poly[(i + 1) % n]
        s += x0 * y1 - x1 * y0
    return s / 2.0


def estencil_como_forma(
    arr: np.ndarray, cor: int, limiar: int = 127, epsilon: float = 2.0
) -> py5.Py5Shape:
    """Constroi o estencil da mascara: o painel preenchido com a silhueta vazada.

    O contorno externo e o retangulo do painel; cada silhueta transparente vira
    um furo (``begin_contour``), com giro oposto ao do painel para que o py5 o
    interprete como negativo -- e por esses furos que os caquinhos aparecem.

    :param arr: Mascara RGBA no formato ``(h, w, 4)``.
    :param cor: Cor de preenchimento do painel.
    :param limiar: Corte de alpha repassado a :func:`contornos_da_mascara`.
    :param epsilon: Tolerancia repassada a :func:`contornos_da_mascara`.
    :returns: ``Py5Shape`` plano do painel com os recortes vazados.
    """
    h, w = arr.shape[:2]
    painel = [(0.0, 0.0), (float(w), 0.0), (float(w), float(h)), (0.0, float(h))]
    giro_painel = _area_assinada(painel)
    forma = py5.create_shape()
    forma.set_fill(cor)
    forma.set_stroke_weight(0)
    with forma.begin_closed_shape():
        for x, y in painel:
            forma.vertex(x, y)
        for poly in contornos_da_mascara(arr, limiar, epsilon):
            # O furo precisa girar ao contrario do painel para virar negativo.
            if _area_assinada(poly) * giro_painel > 0:
                poly = list(reversed(poly))
            with forma.begin_contour():
                for x, y in poly:
                    forma.vertex(x, y)
    return forma
