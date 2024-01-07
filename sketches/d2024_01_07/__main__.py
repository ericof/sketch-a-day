"""2024-01-07
Genuary 07 - Progress Bar.
Barra de progresso que 'afunda' ao ficar mais pesada.
gif
Sketch,py5,CreativeCoding,genuary,genuary7
"""
import py5
import py5_tools

from utils import helpers

sketch = helpers.info_for_sketch(__file__, __doc__)


BARRA_X = (-300, 300)
BARRA_Y = (-100, 100)


def _desenha_barra():
    py5.no_fill()
    py5.stroke(360, 0, 100)
    py5.stroke_weight(7)
    py5.rect(0, 0, 600, 100)


def setup():
    py5.size(helpers.LARGURA, helpers.ALTURA, py5.P3D)
    py5.color_mode(py5.HSB, 360, 100, 100)
    py5.rect_mode(py5.CENTER)


def draw():
    py5.background(360, 0, 0)
    frame = py5.frame_count
    altura = frame + 100
    rotacoes = list(range(-90, 91))
    if altura >= 700:
        py5.no_loop()
    with py5.push_matrix():
        py5.translate(helpers.LARGURA / 2, frame + 100, 0)
        rotacao = rotacoes[frame % 180]
        py5.rotate_x(py5.radians(rotacao))
        _desenha_barra()
        py5.translate(0, 0, -2)
        # Atualiza a barra
        for idx in range(0, frame):
            x = -300 + idx
            if x >= 300:
                break
            h = idx / 600 * 100
            py5.stroke(h, 100, 100)
            py5.stroke_weight(2)
            py5.line(x, -40, x, 40)
    helpers.write_legend(sketch=sketch)


def key_pressed():
    key = py5.key
    if key == " ":
        save_and_close()


def save_and_close():
    py5.no_loop()
    py5.exit_sketch()


if __name__ == "__main__":
    py5_tools.animated_gif(
        f"{sketch.path}/{sketch.day}.gif",
        count=90,
        period=0.1,
        duration=0.00,
        block=False,
    )
    py5.run_sketch()
