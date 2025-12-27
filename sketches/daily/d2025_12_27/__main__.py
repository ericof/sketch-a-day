"""2025-12-27
Esfera de Conexões 03
Inspirado em sketch de Naoki Tsutae
ericof.com|https://openprocessing.org/sketch/2775641
png
Sketch,py5,CreativeCoding
"""

from sketches.utils.draw import canvas
from sketches.utils.draw.cores.paletas import gera_paleta
from sketches.utils.helpers import sketches as helpers

import py5


sketch = helpers.info_for_sketch(__file__, __doc__)

ESFERAS = [(400, 350, "laranja-01"), (200, 100, "tons-azul-01")]
cor_fundo = py5.color(0)

GRAFICOS = []


def popula_cantos(pontos, paleta_nome) -> tuple[list[py5.Py5Vector3D], list[int]]:
    cantos = []
    paleta = []
    total_pontos = len(pontos)
    for i in range(total_pontos):
        for j in range(i + 1, total_pontos):
            a = pontos[i]
            b = pontos[j]
            mid = (a + b) * 0.5
            radius_sq = (a - mid).mag_sq
            # Valida se há outros pontos dentro da esfera definida por a e b
            ok = True
            for k in range(len(pontos)):
                if k in (i, j):
                    continue
                dist_sq = (pontos[k] - mid).mag_sq
                if dist_sq < radius_sq:
                    ok = False
                    break
            if ok:
                cantos.append((a, b))
    base = gera_paleta(paleta_nome, True)
    for _ in range(len(cantos)):
        cor = base[0]
        paleta.append(cor)
        base.rotate(1)
    return cantos, paleta


def setup():
    py5.size(*helpers.DIMENSOES.external, py5.P3D)
    py5.background(cor_fundo)
    # Popula pontos aleatórios
    for num_pontos, raios, paleta_nome in ESFERAS:
        pontos = []
        for _ in range(num_pontos):
            p = py5.Py5Vector3D.random() * raios
            pontos.append(p)
        GRAFICOS.append(popula_cantos(pontos, paleta_nome))


def draw():
    frame_count = py5.frame_count
    with py5.push():
        py5.translate(py5.width / 2, py5.height / 2)
        py5.background(cor_fundo)
        py5.rotate_y(frame_count * -0.001)
        for cantos, paleta in GRAFICOS:
            for i, (a, b) in enumerate(cantos):
                cor = paleta[i]
                py5.stroke(cor)
                py5.stroke_weight((i % 5) + 1)
                py5.line(a.x, a.y, a.z, b.x, b.y, b.z)
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
