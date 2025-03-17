"""2025-03-17
Chaos / Caos I
Sistema caótico, inspirado em https://openprocessing.org/sketch/1916620
png
Sketch,py5,CreativeCoding,op-1916620
"""

import py5

from utils import helpers
from utils.draw import gera_paleta

sketch = helpers.info_for_sketch(__file__, __doc__)


paleta = gera_paleta("Colerful", True)


def cor() -> str:
    rot = py5.random_int(-3, 3)
    paleta.rotate(rot)
    return paleta[0]


def arco(a: float, b: float, c: float, d: float, inicio: float, termino: float):
    py5.arc(a, b, c, d, py5.radians(inicio), py5.radians(termino))


def setup():
    py5.size(helpers.LARGURA, helpers.ALTURA, py5.P3D)
    py5.background("#555")
    larg = py5.width
    altura = py5.height
    profundidade = 50
    meio_l = larg / 2
    meio_a = altura / 2
    g = larg / 10
    g2 = g / 2
    g2_7 = g / 2.7
    g3 = g / 3
    g4 = g / 4
    g8 = g / 8
    gX = g / 10
    x = g2
    y = 0
    limite = larg * 2 - g2
    with py5.push():
        py5.translate(meio_l, meio_a, -profundidade)
        py5.rotate(py5.radians(45))
        py5.translate(0, -altura, 0)
        py5.ellipse(0, 0, 100, 100)
        while x <= limite:
            while y <= limite:
                for x_buff in range(-larg, larg, int(g)):
                    with py5.push():
                        py5.translate(x + x_buff, y, 0)
                        rot = py5.radians(py5.random_choice([0, 90, 180, 270]))
                        py5.rotate(rot)
                        py5.scale(py5.random_choice([-1, 1]), 1)
                        py5.stroke_weight(g / 30)
                        py5.no_fill()
                        py5.stroke(cor())

                        with py5.begin_shape():
                            py5.vertex(-g2, -g4)
                            py5.bezier_vertex(-g2, -g4, -g4, -g4, 0, 0)
                            py5.vertex(0, 0)
                            py5.bezier_vertex(0, 0, 0, -g4, g4, 0)
                            py5.vertex(g4, 0)
                            py5.bezier_vertex(g4, 0, g4, -g4, g2, -g4)
                            py5.vertex(g2, -g4)

                        py5.stroke(cor())
                        with py5.begin_shape():
                            py5.vertex(-g2, g4)
                            py5.bezier_vertex(-g2, g4, -g3, -g8, -g4, g8)
                            py5.vertex(-g4, g8)
                            py5.bezier_vertex(-g4, g8, 0, 0, 0, g8)
                            py5.vertex(0, g8)
                            py5.bezier_vertex(0, g8, 0, 0, g2, g4)
                            py5.vertex(g2, g4)

                        py5.stroke(cor())
                        arco(0, 0, g2, g2, 0, 90)
                        py5.stroke(cor())
                        arco(0, g2, g2, g2, 270, 360)
                        py5.stroke(cor())
                        arco(0, -g2, g2, g2, 90, 180)

                        py5.stroke(cor())
                        with py5.begin_shape():
                            py5.vertex(-g4, g2)
                            py5.vertex(-g4, g4)
                            pf = py5.random_choice([g2, g4, -g2, -g4])
                            py5.vertex(0, pf)

                        py5.stroke(cor())
                        py5.line(g4, -g2, g8, -g4)
                        py5.stroke(cor())
                        py5.line(g4, -g4, g2, -g2)

                        py5.stroke(cor())
                        arco(g2, g4, g2, g2, 90, 180)

                        py5.stroke(cor())
                        py5.line(-g2, g2, 0, g2_7)

                        py5.stroke(cor())
                        arco(-g4, -g2, g2, g2, 90, 180)

                        with py5.push():
                            py5.translate(0, 0, profundidade // 2)
                            py5.no_stroke()
                            py5.fill(cor())
                            py5.ellipse(0, g2_7, g8, g8)
                            py5.fill(cor())
                            py5.ellipse(g8, -g4, gX, gX)
                            py5.fill(cor())
                            py5.ellipse(g4, -g4, gX, gX)
                y += g
            x += g2
    helpers.write_legend(sketch=sketch, frame="#000", cor="#FFF")


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
