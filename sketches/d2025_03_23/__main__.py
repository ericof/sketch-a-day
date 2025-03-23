"""2025-03-23
Warhol's Alvorada
Exercício no uso do estilo de Andy Warhol com as colunas do Palácio da Alvorada
png
Sketch,py5,CreativeCoding
"""

from collections import deque
from random import shuffle

import py5

from utils import helpers
from utils.draw import cria_grade, gera_paleta

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
    py5.rect_mode(py5.CENTER)
    py5.shape_mode(py5.CENTER)
    paleta = prepara_paleta()
    celula = 150
    altura = celula
    altura_forma = altura * 0.8
    largura = altura * 0.75
    largura_forma = largura * 0.8
    forma = coluna(largura_forma, altura_forma)
    grade = cria_grade(py5.width, py5.height, 100, 100, celula, celula, False)
    for x0, y0 in grade:
        x = x0 + celula / 2
        y = y0 + celula / 2
        fundo, cor = paleta[0]
        paleta.rotate(1)
        with py5.push():
            py5.translate(x, y, -50)
            # Desenha frame
            with py5.push():
                py5.fill(fundo)
                py5.stroke_weight(4)
                py5.stroke(cor_contraste)
                py5.rect(0, 0, celula, celula)
            xf = -largura_forma / 2
            yf = -altura_forma / 2
            forma.set_stroke(cor_contraste)
            forma.set_fill(cor)
            py5.shape(forma, xf, yf, largura_forma, altura_forma)
    frame, cor = paleta[0]
    helpers.write_legend(sketch=sketch, frame=frame, cor=cor)


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
