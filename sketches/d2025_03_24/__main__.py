"""2025-03-24
DF on LSD
Exercício no uso das colunas do Palácio da Alvorada em círculos concêntricos
png
Sketch,py5,CreativeCoding
"""

from collections import deque
from random import shuffle

import py5

from utils import helpers
from utils.draw import gera_paleta

sketch = helpers.info_for_sketch(__file__, __doc__)


def coluna(largura: float = 300, altura: float = 400) -> py5.Py5Shape:
    # Computa os pontos a serem utilizados
    largura_2 = largura / 2
    lb = largura_2 // 20
    altura_2 = altura / 2
    altura_inter = altura_2 - (altura_2 / 3)
    ab1 = altura_inter - (altura_2 / 20)
    ab2 = altura_inter + (altura_2 / 20)
    p1 = (0, -altura_2)
    pb1 = (lb, ab1)
    p2 = (largura_2, altura_inter)
    pb2 = (lb, ab2)
    p3 = (0, altura_2)
    pb3 = (-lb, ab2)
    p4 = (-largura_2, altura_inter)
    pb4 = (-lb, ab1)
    pontos = (p1, pb1, p2, pb2, p3, pb3, p4, pb4, p1)
    coluna = py5.create_shape()
    with coluna.begin_shape():
        for idx, ponto in enumerate(pontos):
            ponto = [ponto[0] + largura, ponto[1] + altura]
            if idx % 2 == 0:
                coluna.vertex(*ponto)
            else:
                pa = pontos[idx - 1]
                pa = [pa[0] + largura, pa[1] + altura]
                pp = pontos[idx + 1]
                pp = [pp[0] + largura, pp[1] + altura]
                coluna.bezier_vertex(*pa, *ponto, *pp)
    return coluna


def prepara_paleta() -> deque[tuple[py5.Py5Color, py5.Py5Color]]:
    paleta_base = gera_paleta("Warhol", False)
    paleta: list[tuple[py5.Py5Color, py5.Py5Color]] = []
    for i in range(0, len(paleta_base), 2):
        paleta.append((paleta_base[i], paleta_base[i + 1]))
    shuffle(paleta)
    return deque(paleta)


def setup():
    py5.size(helpers.LARGURA, helpers.ALTURA, py5.P3D)
    cor_contraste = "#000"
    py5.background(cor_contraste)
    py5.color_mode(py5.HSB, 360, 100, 100)
    py5.shape_mode(py5.CORNERS)
    meio_x = py5.width / 2
    meio_y = py5.height / 2
    paleta = prepara_paleta()
    celula = 150
    altura = celula
    altura_forma = altura * 0.8
    largura = altura * 0.75
    largura_forma = largura * 0.8
    forma = coluna(largura_forma, altura_forma)
    total_pontos = 10
    passo = 360 / total_pontos
    xb = 40
    with py5.push():
        py5.translate(meio_x, meio_y, -50)
        for idy, yb in enumerate(range(660, 150, -110)):
            with py5.push():
                fundo, cor = paleta[0]
                paleta.rotate(1)
                if idy % 2:
                    rot = py5.radians(passo / 2)
                    py5.rotate(rot)
                for idx in range(total_pontos):
                    rot = py5.radians(passo)
                    py5.rotate(rot)
                    x0 = (-largura_forma / 2) - xb
                    y0 = (-altura_forma / 2) - yb
                    xf = (largura_forma / 2) - xb
                    yf = (altura_forma / 2) - yb
                    with py5.push():
                        py5.translate(0, 0, -70)
                        py5.fill(fundo)
                        py5.circle(0, 0, (yb * 2.2))
                    forma.set_stroke(cor_contraste)
                    forma.set_fill(cor)
                    py5.shape(forma, x0, y0, xf, yf)

        with py5.push():
            py5.translate(0, 0, -70)
            py5.fill(cor_contraste)
            py5.circle(0, 0, yb)
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
