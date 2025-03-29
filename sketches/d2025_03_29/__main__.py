"""2025-03-29
Oliver's 12
A dot for every day in the life of my beautiful son
png
Sketch,py5,CreativeCoding
"""

from datetime import datetime, timedelta

import py5

from utils import helpers
from utils.draw import gera_paleta

sketch = helpers.info_for_sketch(__file__, __doc__)

hoje = datetime(2025, 3, 29, 15, 0)
nasc = datetime(2012, 3, 29, 14, 0)


def calcula_dias() -> int:
    delta: timedelta = hoje - nasc
    return delta.days


def ponto_ano() -> list[int]:
    anos = []
    for ano in range(2012, 2026):
        hoje = datetime(ano, 3, 29, 15, 0)
        delta: timedelta = hoje - nasc
        anos.append(delta.days)
    return anos


def calcula_cores(anos: list[int]) -> dict[int, str]:
    cores = {}
    paleta = gera_paleta("oliver-13", como_deque=True)
    for idx, ano in enumerate(anos):
        cores[ano] = paleta[idx]
    return cores


def pontos_espiral(
    x0: float, y0: float, offset: float, total_pontos: int, raio_max: int
) -> list[tuple[float, float, str, float, bool]]:
    pontos = []
    cores = calcula_cores(ponto_ano())
    cor = cores[0]
    peso = 1
    for i in range(total_pontos):
        ponto = False
        cor = cores.get(i, cor)
        if i in cores:
            cor = cores[i]
            peso += 0.5
            ponto = True
        angulo = py5.radians(i * 2.4 + offset)
        r = i * raio_max / total_pontos
        x = x0 + r * py5.cos(angulo)
        y = y0 + r * py5.sin(angulo)
        pontos.append((x, y, cor, peso, ponto))
    return pontos


def adiciona_aniversario(x, y, z, peso):
    with py5.push():
        py5.stroke("#00F")
        py5.stroke_weight(peso + 4)
        py5.point(x, y, z + 2)


def setup():
    py5.size(helpers.LARGURA, helpers.ALTURA, py5.P3D)
    py5.background(0)
    py5.color_mode(py5.HSB, 360, 100, 100)
    dias = calcula_dias()
    espiral = pontos_espiral(0, 0, 37, dias, 450)
    py5.stroke("#FFF")
    py5.stroke_weight(1)
    with py5.push():
        py5.translate(py5.width // 2, py5.height // 2, -130)
        x0, y0 = 0, 0
        z = 0
        for x, y, cor, peso, ponto in espiral:
            py5.stroke(cor)
            py5.stroke_weight(peso)
            py5.line(x0, y0, z, x, y, z)
            if ponto:
                z += 2
                adiciona_aniversario(x, y, z, peso)
            x0, y0 = x, y
        adiciona_aniversario(x, y, z, peso)

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
