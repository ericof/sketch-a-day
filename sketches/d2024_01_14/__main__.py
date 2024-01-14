"""2024-01-14
Genuary 14 - 1kb.
Mandala gerada com menos de 1Kb de código.
png
Sketch,py5,CreativeCoding,genuary,genuary14
"""
import py5

from utils import helpers as H

sketch = H.info_for_sketch(__file__, __doc__)
X = H.LARGURA
Y = H.ALTURA


def setup():
    py5.size(X, Y)
    py5.background(0)
    py5.stroke_weight(1)
    py5.no_fill()
    py5.rect_mode(py5.CENTER)
    d = 800
    while d > 10:
        r = py5.remap(d, 0, 800, 0, 255)
        for A in range(0, 360, 12):
            g = (A / 2) * 1.5
            b = py5.random_int(20, 255)
            with py5.push_matrix():
                py5.stroke(r, g, b)
                py5.translate(X / 2, Y / 2)
                py5.rotate(py5.radians(A))
                py5.rect(0, 0, d, d)
        d = d / 1.5
    H.write_legend(sketch)
    H.save_sketch_image(sketch)
    py5.exit_sketch()


if __name__ == "__main__":
    py5.run_sketch()
