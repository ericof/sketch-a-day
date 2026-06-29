from pathlib import Path
from PIL import Image

import cv2
import math
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
    arr: np.ndarray,
    cor: int,
    limiar: int = 127,
    epsilon: float = 2.0,
    profundidade: float = 1.0,
) -> py5.Py5Shape:
    """Constroi o estencil da mascara como um prisma com a silhueta vazada.

    A face frontal e o retangulo do painel com cada silhueta transparente como
    furo (``begin_contour``, giro oposto ao do painel para virar negativo). Cada
    furo ganha paredes ligando a face frontal -- em ``z = profundidade``, voltada
    para a camera -- ate a base em ``z = 0``, de modo que a abertura tenha
    profundidade visivel: um poco com a forma da silhueta por onde se ve o fundo.
    Com ``profundidade = 1`` (padrao) o prisma e praticamente plano, equivalente
    ao estencil chapado original.

    :param arr: Mascara RGBA no formato ``(h, w, 4)``.
    :param cor: Cor de preenchimento do painel e das paredes.
    :param limiar: Corte de alpha repassado a :func:`contornos_da_mascara`.
    :param epsilon: Tolerancia repassada a :func:`contornos_da_mascara`.
    :param profundidade: Altura da extrusao em z; a face frontal fica em
        ``z = profundidade`` e as paredes de cada furo descem ate ``z = 0``.
    :returns: ``GROUP`` com a face frontal vazada e as paredes de cada furo.
    """
    h, w = arr.shape[:2]
    painel = [(0.0, 0.0), (float(w), 0.0), (float(w), float(h)), (0.0, float(h))]
    giro_painel = _area_assinada(painel)
    furos = []
    for poly in contornos_da_mascara(arr, limiar, epsilon):
        # O furo precisa girar ao contrario do painel para virar negativo.
        if _area_assinada(poly) * giro_painel > 0:
            poly = list(reversed(poly))
        furos.append(poly)

    grupo = py5.create_shape(py5.GROUP)

    # Face frontal: painel vazado, voltado para a camera em z = profundidade.
    frente = py5.create_shape()
    frente.set_fill(cor)
    frente.set_stroke_weight(0)
    with frente.begin_closed_shape():
        frente.normal(0, 0, 1)
        for x, y in painel:
            frente.vertex(x, y, profundidade)
        for poly in furos:
            with frente.begin_contour():
                for x, y in poly:
                    frente.vertex(x, y, profundidade)
    grupo.add_child(frente)

    # Paredes: uma face por aresta de furo, da frente (z=profundidade) a base (z=0).
    for poly in furos:
        n = len(poly)
        for i in range(n):
            x0, y0 = poly[i]
            x1, y1 = poly[(i + 1) % n]
            dx, dy = x1 - x0, y1 - y0
            comp = math.hypot(dx, dy) or 1.0
            # Normal no plano xy apontando para dentro da abertura; inverta o
            # sinal se as paredes ficarem escuras ao habilitar luzes no estencil.
            nx, ny = -dy / comp, dx / comp
            parede = py5.create_shape()
            parede.set_fill(cor)
            parede.set_stroke_weight(0)
            with parede.begin_closed_shape():
                parede.normal(nx, ny, 0)
                parede.vertex(x0, y0, profundidade)
                parede.vertex(x1, y1, profundidade)
                parede.vertex(x1, y1, 0)
                parede.vertex(x0, y0, 0)
            grupo.add_child(parede)
    return grupo
