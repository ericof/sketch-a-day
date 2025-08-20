"""2025-08-20
Interferências 01
Padrão criado com elipses sobrepostas.
ericof.com
png
Sketch,py5,CreativeCoding
"""

from sketches.utils.draw import canvas
from sketches.utils.helpers import sketches as helpers

import py5


sketch = helpers.info_for_sketch(__file__, __doc__)


def setup():
    py5.size(*helpers.DIMENSOES.external, py5.P3D)
    cor_fundo = py5.color(0)
    py5.background(0)
    py5.color_mode(py5.HSB, 360, 100, 100)
    py5.ellipse_mode(py5.CENTER)
    with py5.push():
        py5.no_fill()
        py5.stroke_weight(4)
        py5.translate(py5.width / 2, py5.height / 2)
        for y, h, buffer in (
            (0, 180, 0),
            (-300, 40, -150),
            (300, 40, -150),
            (-600, 240, 200),
            (600, 240, 200),
        ):
            py5.stroke(h, 50, 50)
            for xb in range(-600, 600, 40):
                x = xb + buffer
                py5.ellipse(x, y, 60, 600)

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
