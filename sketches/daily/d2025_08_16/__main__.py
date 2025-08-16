"""2025-08-16
All Good Things
Nuvem de palavras do script de All Good Things, de Star Trek: The Next Generation
ericof.com
png
Sketch,py5,CreativeCoding
"""

from PIL.Image import Image
from sketches.utils.draw import canvas
from sketches.utils.helpers import sketches as helpers
from sketches.utils.helpers import wc as wc_helper
from sketches.utils.helpers.images import resource_image_as_array

import numpy as np
import py5
import wordcloud


sketch = helpers.info_for_sketch(__file__, __doc__)

URL = "https://www.st-minutiae.com/resources/scripts/277.txt"


def criar_nuvem(texto: str, mascara: np.ndarray) -> Image:
    """Cria uma nuvem de palavras a partir do texto e da máscara fornecidos."""
    wc = wordcloud.WordCloud(
        background_color="black",
        stopwords=wordcloud.STOPWORDS,
        max_font_size=50,
        max_words=6000,
        mask=mascara,
        mode="RGB",
        contour_width=1,
    )
    wc.generate(texto)
    image_colors = wordcloud.ImageColorGenerator(mascara)
    wc.recolor(color_func=image_colors)
    return wc.to_image()


def setup():
    py5.size(*helpers.DIMENSOES.external, py5.P3D)
    cor_fundo = py5.color(0)
    py5.background(0)
    py5.color_mode(py5.HSB, 360, 100, 100)
    texto = wc_helper.processa_script(wc_helper.texto_de_url(URL))
    mascara = resource_image_as_array("st-mask.png")
    nuvem = criar_nuvem(texto, mascara)
    py5.image(nuvem, *helpers.DIMENSOES.pos_interno)
    # Credits and go
    canvas.sketch_frame(
        sketch, cor_fundo, "large_transparent_white", "transparent_white"
    )


def key_pressed():
    key = py5.key
    if key == " ":
        save_and_close()


def save_and_close():
    py5.no_loop()
    canvas.save_sketch_image(sketch)
    py5.exit_sketch()


if __name__ == "__main__":
    py5.run_sketch()
