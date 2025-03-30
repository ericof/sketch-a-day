"""2025-03-30
Basketball 01
Exercício de criação de bola de basquete
png
Sketch,py5,CreativeCoding
"""

from pathlib import Path

import numpy as np
import py5

from utils import helpers
from utils.draw import pontos_circulo_3d

sketch = helpers.info_for_sketch(__file__, __doc__)


def carrega_padrao(relative_path: str) -> py5.Py5Image:
    path = Path(__file__).parent / relative_path
    img = helpers.image_as_array(path)
    for eixo in (0, 1):
        img = np.concatenate((img, img), axis=eixo)
    return py5.create_image_from_numpy(img, "RGB")


def gomos(
    raio: int,
) -> tuple[list[tuple[float, float, float], tuple[float, float, float]]]:
    return (
        pontos_circulo_3d(360, raio, 0, 0, 0, (1, 0, 0)),
        pontos_circulo_3d(360, raio, 0, 0, 0, (0, 1, 0)),
    )


def setup():
    py5.size(helpers.LARGURA, helpers.ALTURA, py5.P3D)
    py5.background(0)
    py5.color_mode(py5.HSB, 360, 100, 100)
    py5.sphere_detail(500)
    py5.lights()
    py5.shininess(3.0)
    padrao = carrega_padrao("padrao.jpg")
    raio = 300
    with py5.push():
        py5.translate(py5.width // 2, py5.height // 2, -400)
        py5.directional_light(0, 0, 150, 300, 100, 100)
        py5.no_stroke()
        forma = py5.create_shape(py5.SPHERE, raio)
        forma.set_fill(py5.color(40, 50, 50))
        forma.set_texture(padrao)
        forma.set_stroke_weight(0)
        py5.shape(forma)
        with py5.push():
            py5.stroke("#000")
            py5.stroke_weight(9)
            py5.rotate_y(py5.radians(30))
            for gomo in gomos(raio):
                x0 = y0 = z0 = None
                for x, y, z in gomo:
                    if not x0:
                        x0, y0, z0 = x, y, z
                    py5.line(x0, y0, z0, x, y, z)
                    x0, y0, z0 = x, y, z

    helpers.write_legend(sketch=sketch)


def key_pressed():
    key = py5.key
    if key == " ":
        save_and_close()


def save_and_close():
    py5.no_loop()
    helpers.save_sketch_image(sketch)
    py5.exit_sketch()


if __name__ == "__main__":
    py5.run_sketch()
