"""2025-12-19
18263 days after
Círculo da vida, 18263 dias depois
ericof.com
png
Sketch,py5,CreativeCoding
"""

from datetime import datetime
from datetime import timedelta
from sketches.utils.draw import canvas
from sketches.utils.helpers import sketches as helpers
from zoneinfo import ZoneInfo

import py5


sketch = helpers.info_for_sketch(__file__, __doc__)

tzone = ZoneInfo("America/Sao_Paulo")
nasc = datetime(1975, 12, 19, 14, 0, 0, tzinfo=tzone)
hoje = datetime(2025, 12, 19, 14, 0, 0, tzinfo=tzone)
dias_vividos = (hoje - nasc).days


def calcula_cores() -> dict[int, tuple[float, bool]]:
    cores = {}
    dias = list(range(dias_vividos))
    h_base = 0
    passo = 340 / max(dias)
    for dia in dias:
        cor = py5.color(h_base + (dia * passo), 100, 100)
        data = nasc + timedelta(days=dia)
        aniversario = (data.month, data.day) == (12, 19)
        cores[dia] = (cor, aniversario)
    return cores


def pontos_espiral(
    x0: float, y0: float, offset: float, raio_max: int
) -> list[tuple[float, float, str, float, bool]]:
    pontos = []
    cores = calcula_cores()
    peso = 1
    total_pontos = len(cores)
    for dia, (cor, aniversario) in cores.items():
        ponto = False
        if aniversario:
            peso += 0.05
            ponto = True
        angulo = py5.radians(dia * 2.4 + offset)
        r = dia * raio_max / total_pontos
        x = x0 + r * py5.cos(angulo)
        y = y0 + r * py5.sin(angulo)
        pontos.append((x, y, cor, peso, ponto))
    return pontos


def adiciona_aniversario(x, y, z, cor, peso):
    with py5.push():
        py5.translate(0, 0, z + 2)
        py5.stroke(cor)
        py5.stroke_weight(2)
        py5.fill("#000")
        py5.circle(x, y, peso + 4)


def setup():
    py5.size(*helpers.DIMENSOES.external, py5.P3D)
    cor_fundo = py5.color(0)
    py5.background(cor_fundo)
    py5.color_mode(py5.HSB, 360, 100, 100)
    espiral = pontos_espiral(0, 0, 37, 400)
    py5.stroke("#FFF")
    py5.stroke_weight(1)
    with py5.push():
        py5.translate(*helpers.DIMENSOES.centro, -680)
        x0, y0 = 0, 0
        z = 0
        for x, y, cor, peso, ponto in espiral:
            py5.stroke(cor)
            py5.stroke_weight(peso)
            py5.line(x0, y0, z, x, y, z)
            if ponto:
                z += 12
                adiciona_aniversario(x, y, z, cor, peso)
            x0, y0 = x, y
        adiciona_aniversario(x, y, z, cor, peso)

    with py5.push():
        py5.translate(0, 0, 0)
        # Credits and go
        canvas.sketch_frame(
            sketch, py5.color(0), "large_transparent_white", "transparent_white"
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
