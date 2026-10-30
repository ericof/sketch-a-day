"""2026-10-30
Esfera 04
Execício de criação de esfera
ericof.com
png
Sketch,py5,CreativeCoding
"""

from sketches.utils.draw import canvas
from sketches.utils.helpers import sketches as helpers

import py5


sketch = helpers.info_for_sketch(__file__, __doc__)

cor_fundo = py5.color(0)

RAIO = 300
ZIGUES = 40
PONTOS_PERNA = 40
PONTOS = 2 * ZIGUES * PONTOS_PERNA
AMPLITUDE = float(py5.radians(75))
TORCAO = 1.8
TRACO = 4
SATURACAO = 80
BRILHO = 100
RAIO_MIOLO = RAIO * 0.98
DETALHE_MIOLO = 60


def ponto_zigue_zague(t):
    """Ponto do traço em ``t``, de 0 a 1, dando uma volta completa na esfera.

    O azimute avança sempre enquanto a latitude sobe e desce em onda
    triangular, por isso o traço não se cruza e termina onde começou.
    ``TORCAO`` inclina as pernas sem alterar essas duas propriedades.
    """
    fase = (ZIGUES * t) % 1
    desvio = AMPLITUDE * (4 * abs(fase - 0.5) - 1)
    polar = py5.HALF_PI + desvio
    azimute = py5.TWO_PI * t + TORCAO * desvio
    seno = py5.sin(polar)
    return (
        float(RAIO * seno * py5.cos(azimute)),
        float(RAIO * py5.cos(polar)),
        float(RAIO * seno * py5.sin(azimute)),
    )


def cor_traco(t, matiz):
    """Cor em ``t``: o matiz dá uma volta inteira e fecha em ``matiz``."""
    h = int(matiz + 360 * t) % 360
    return py5.color(h, SATURACAO, BRILHO)


def inicializa():
    global esfera
    esfera = []
    matiz = py5.random(360)
    for i in range(PONTOS):
        t = i / PONTOS
        esfera.append((ponto_zigue_zague(t), cor_traco(t, matiz)))


def setup():
    py5.size(*helpers.DIMENSOES.external, py5.P3D)
    py5.color_mode(py5.HSB, 360, 100, 100)
    inicializa()


def draw():
    py5.background(cor_fundo)
    frame = py5.frame_count
    radianos = float(py5.radians(frame))
    with py5.push():
        py5.translate(*helpers.DIMENSOES.centro, 0)
        py5.rotate_y(radianos)
        py5.rotate_z(radianos)
        # Miolo opaco: esconde o lado de trás, que pareceria cruzar o traço
        py5.no_stroke()
        py5.fill(cor_fundo)
        py5.sphere_detail(DETALHE_MIOLO)
        py5.sphere(RAIO_MIOLO)
        py5.no_fill()
        py5.stroke_weight(TRACO)
        with py5.begin_closed_shape():
            for ponto, cor in esfera:
                py5.stroke(cor)
                py5.vertex(*ponto)
    # Credits and go
    canvas.sketch_frame(
        sketch,
        cor_fundo,
        "large_transparent_white",
        "transparent_white",
        version=2,
    )


def key_pressed():
    key = py5.key
    if key == " ":
        save_and_close()
    elif key == "r":
        inicializa()


def save_and_close():
    py5.no_loop()
    canvas.save_sketch_image(sketch)
    py5.exit_sketch()


if __name__ == "__main__":
    py5.run_sketch()
