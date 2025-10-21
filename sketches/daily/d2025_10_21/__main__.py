"""2025-10-21
MSX Basic: Padrões Axiais 10
Desenho de padrões axiais baseado em código MSX Basic.
ericof.com|https://github.com/gilbertfrancois/msx/blob/master/src/basic/spirals1.bas
png
Sketch,py5,CreativeCoding
"""

from sketches.utils.draw import canvas
from sketches.utils.draw.cores.paletas import gera_paleta
from sketches.utils.helpers import sketches as helpers

import py5


sketch = helpers.info_for_sketch(__file__, __doc__)

RAIO: int = 2500
PASSO_RAIO: int = -3
IDX: int = 6
EPS: float = 25
PI: float = py5.PI
PD: float = PI * 2 - EPS
PH: float = PI / IDX
PY: float = IDX / RAIO * PI * IDX
LW: int = 80
NC: int = 2
Z_0: int = -RAIO
Z_PASSO: int = 2


def axial():
    paleta = gera_paleta("pastel", True)
    tamanho = len(paleta)
    for j in range(0, LW):
        c = paleta[int(j / LW * tamanho)]
        z = Z_0
        for r in range(RAIO, 0, PASSO_RAIO):
            with py5.push():
                py5.translate(0, 0, z)
                as_ = py5.cos(r * PY) + j * PD / LW
                if as_ >= PD:
                    as_ = as_ - PD
                if as_ <= 0:
                    as_ = as_ + PD
                ae = as_ + PD / LW
                if ae >= PD:
                    ae = ae - PD
                if ae <= 0:
                    ae = ae + PD
                x0 = r * py5.cos(as_)
                y0 = r * py5.sin(as_)
                x1 = (r + 1) * py5.cos(ae)
                y1 = (r + 1) * py5.sin(ae)
                py5.stroke(c)
                py5.stroke_weight(py5.random_int(1, 3))
                py5.line(x0, y0, x1, y1)
                z += Z_PASSO


def setup():
    py5.size(*helpers.DIMENSOES.external, py5.P3D)
    py5.color_mode(py5.HSB, 360, 100, 100)


def draw():
    cor_fundo = py5.color(0)
    py5.background(cor_fundo)
    with py5.push():
        py5.translate(*helpers.DIMENSOES.centro, -100)
        axial()
    parametros = f"Params: {RAIO} - {PASSO_RAIO} - {EPS} - {LW} - {NC} - {IDX}"
    py5.window_title(parametros)
    # Credits and go
    canvas.sketch_frame(
        sketch, cor_fundo, "large_transparent_white", "transparent_white"
    )
    with py5.push():
        py5.translate(0, 0, 10)
        canvas.draw_text_box(
            parametros, style_name="transparent_white", x=20, y=950, align=py5.LEFT
        )


def key_pressed():  # noQA: C901
    global RAIO, PASSO_RAIO, EPS, LW, NC, IDX
    key = py5.key
    match key:
        case " ":
            save_and_close()
        case "+":
            RAIO += 10
        case "-":
            RAIO -= 10 if RAIO > 20 else 0
        case ">":
            PASSO_RAIO += 1
        case "<":
            PASSO_RAIO -= 1 if PASSO_RAIO > 2 else 0
        case "t":
            EPS *= 1.1
        case "g":
            EPS *= 0.9
        case "w":
            LW += 1
        case "s":
            LW -= 1 if LW > 1 else 0
        case "]":
            IDX += 1
        case "[":
            IDX -= 1 if IDX > 3 else 0


def save_and_close():
    py5.no_loop()
    canvas.save_sketch_image(sketch)
    py5.exit_sketch()


if __name__ == "__main__":
    py5.run_sketch()
