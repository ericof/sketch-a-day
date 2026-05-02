"""2026-05-02
STXP
Pixelado com o logo da Starfleet
ericof.com|https://ericof.com/en/sketches/2023-11-01
png
Sketch,py5,CreativeCoding
"""

from sketches.utils.draw import canvas
from sketches.utils.helpers import sketches as helpers
from sketches.utils.helpers.images import resource_image_as_array

import numpy as np
import py5


sketch = helpers.info_for_sketch(__file__, __doc__)

cor_fundo = py5.color(0)

STROKE_MOD = 0.75
total_chunks = 100
tam_min = 4.0
tam_max = 12.0
img_array: np.ndarray | None = None
pontos: list[tuple[int, int, int, np.ndarray, list[float]]] = []
altura_chunk = helpers.DIMENSOES.internal[1] / total_chunks


def _chunks_v_exponencial(
    largura: int,
    n: int = 80,
    c_min: float = 4.0,
    c_max: float = 16.0,
) -> np.ndarray:
    """Gera ``n`` chunks em V exponencial cuja soma é exatamente ``largura``.

    Os tamanhos de bloco seguem ``c(t) = c_min · 2^(alpha·|2t - 1|)`` com
    ``t ∈ [0, 1]`` discretizado em ``n`` pontos e
    ``alpha = log2(c_max / c_min)``, de modo que ``c(0) = c(1) = c_max``
    (bordas) e ``c(0.5) = c_min`` (centro). Em seguida o array é
    reescalado para que a soma bata exatamente ``largura``,
    arredondado para inteiros, e o resíduo do arredondamento é
    absorvido no chunk central (o menor) — preservando o perfil em V
    e evitando lacuna ou estouro no eixo X.

    :param largura: total de pixels a cobrir no eixo X.
    :param n: número de chunks na sequência.
    :param c_min: tamanho do bloco no centro do V (pixels).
    :param c_max: tamanho do bloco nas bordas do V (pixels).
    :returns: array de inteiros (``≥ 1``) com soma igual a ``largura``.
    """
    alpha = np.log2(c_max / c_min)
    t = np.linspace(0, 1, n)
    raw = c_min * np.power(2.0, alpha * np.abs(2 * t - 1))
    raw = raw * (largura / raw.sum())
    chunks = np.maximum(1, np.round(raw).astype(int))
    diff = largura - int(chunks.sum())
    if diff != 0:
        meio = n // 2
        chunks[meio] = max(1, chunks[meio] + diff)
    return chunks


def _pixelar(
    img_array: np.ndarray,
    altura: int,
    x: int,
    chunks: np.ndarray,
    limite: int,
) -> list[tuple[int, int, int, np.ndarray, list[float]]]:
    """Amostra a imagem em colunas com tamanho de bloco variável.

    Percorre ``chunks`` da esquerda para a direita, avançando ``x`` em
    cada iteração. Para cada tamanho de bloco varre uma coluna inteira
    no eixo Y em blocos quadrados de lado ``pixel_chunk``. Cada bloco
    devolve a cor mais intensa por canal via :func:`np.max` (e não a
    média, apesar do nome ``avg_color``), preservando bordas luminosas
    do logo da Starfleet sobre o fundo preto. O traço de cada elipse é
    uma versão atenuada da própria cor (``STROKE_MOD = 0.75``),
    criando contorno sutil sem desviar da paleta.

    Espera-se que ``chunks`` siga um perfil em V (tamanhos maiores
    nas bordas, menores no centro) — ver :func:`_chunks_v_exponencial`
    — concentrando detalhe na região focal. Encerra quando ``x``
    ultrapassa ``limite``.

    :param img_array: array NumPy da imagem ``(H, W, C)``.
    :param altura: altura útil em pixels para a varredura vertical.
    :param x: coordenada inicial do eixo X em pixels.
    :param chunks: sequência de tamanhos de bloco (em pixels).
    :param limite: largura máxima em pixels; corta a iteração ao ultrapassar.
    :returns: lista de tuplas ``(x, y, pixel_chunk, cor_max, stroke)``.
    """
    data = []
    for pixel_chunk in chunks:
        pixel_chunk = int(pixel_chunk)
        for y in range(0, altura, pixel_chunk):
            block = img_array[y : y + pixel_chunk, x : x + pixel_chunk]
            avg_color = np.max(block, axis=(0, 1))
            stroke = [c * STROKE_MOD for c in avg_color]
            data.append((x, y, pixel_chunk, avg_color, stroke))
        x += pixel_chunk
        if x >= limite:
            return data
    return data


def setup() -> None:
    """Configura janela P3D, carrega ``st-mask.png`` e pré-calcula a pixelação.

    O perfil ``pixel_chunks`` é uma curva em V exponencial gerada por
    :func:`_chunks_v_exponencial` — blocos de ``c_max`` pixels nas
    bordas decrescendo até ``c_min`` no centro segundo
    ``c(t) = c_min · 2^(alpha·|2t-1|)`` — concentrando detalhe na
    região do logo da Starfleet.
    """
    global img_array, pontos
    py5.size(*helpers.DIMENSOES.external, py5.P3D)
    py5.ellipse_mode(py5.CENTER)
    img_array = resource_image_as_array("st-mask.png")
    largura, altura = helpers.DIMENSOES.internal
    pixel_chunks = _chunks_v_exponencial(
        largura, n=total_chunks, c_min=tam_min, c_max=tam_max
    )
    pontos = _pixelar(img_array, altura, 0, pixel_chunks, largura)


def draw() -> None:
    """Renderiza o frame: fundo preto, elipses pixeladas e créditos."""
    py5.background(cor_fundo)
    with py5.push():
        py5.translate(*helpers.DIMENSOES.pos_interno, -10)
        for x, y, pixel_chunk, cor_media, stroke in pontos:
            py5.stroke(*stroke)
            py5.fill(*cor_media)
            py5.ellipse(
                x + pixel_chunk / 2, y + altura_chunk / 2, pixel_chunk, altura_chunk
            )
    # Credits and go
    canvas.sketch_frame(
        sketch,
        cor_fundo,
        "large_transparent_white",
        "transparent_white",
        version=2,
    )


def key_pressed() -> None:
    """Captura teclas: ``espaço`` salva a imagem e encerra."""
    key = py5.key
    if key == " ":
        save_and_close()


def save_and_close() -> None:
    """Para o loop, salva a imagem do sketch e encerra."""
    py5.no_loop()
    canvas.save_sketch_image(sketch)
    py5.exit_sketch()


if __name__ == "__main__":
    py5.run_sketch()
