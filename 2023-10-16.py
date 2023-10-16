"""2023-10-16"""
from helpers import HEIGHT
from helpers import save_image
from helpers import WIDTH
from helpers import write_legend
from pathlib import Path

import py5


IMG_NAME = Path(__file__).name.replace(".py", "")

SIZE = 600
SIZE_INTERNO = 510
ALTURA_INICIAL = -230


def forma_01():
    x_1 = SIZE - SIZE_INTERNO
    x_2 = SIZE_INTERNO
    altura_1 = 25
    bezier_largura = x_1 // 3
    bezier_altura_1 = altura_1 + 2
    altura_2 = 60
    bezier_altura_2 = altura_2 + 2
    s = py5.create_shape()
    with s.begin_shape():
        s.vertex(0, 0)
        s.bezier_vertex(0, 0, bezier_largura, bezier_altura_1, x_1, altura_1)
        s.vertex(x_1, altura_1)
        s.vertex(x_2, altura_1)
        s.bezier_vertex(x_2, altura_1, SIZE - bezier_largura, bezier_altura_1, SIZE, 0)
        s.vertex(SIZE, 0)
        s.vertex(SIZE, altura_1)
        s.bezier_vertex(
            SIZE,
            altura_1,
            SIZE - bezier_largura,
            bezier_altura_2,
            x_2,
            altura_2,
        )
        s.vertex(x_2, altura_2)
        s.vertex(x_1, altura_2)
        s.bezier_vertex(x_1, altura_2, bezier_largura, bezier_altura_2, 0, altura_1)
        s.vertex(0, altura_1)
        s.vertex(0, 0)

    return s, altura_2 - 29, SIZE - 40


def forma_02():
    altura = 30
    largura = SIZE_INTERNO
    buffer = largura * 0.05
    x0 = 0
    x1 = largura
    x2 = x1 - buffer
    x3 = x0 + buffer
    s = py5.create_shape()
    with s.begin_shape():
        s.vertex(x0, 0)
        s.vertex(x1, 0)
        s.vertex(x2, altura)
        s.vertex(x3, altura)
        s.vertex(x0, 0)
    return s, altura, largura


def forma_03():
    largura = 30
    s = py5.create_shape()
    with s.begin_shape():
        s.vertex(0, 0)
        s.vertex(largura, 0)
        s.vertex(largura, largura)
        s.vertex(0, largura)
        s.vertex(0, 0)
    return s, largura, largura


def forma_04():
    return forma_02()


def forma_05():
    largura = SIZE // 6
    altura = SIZE // 1.7
    y0 = 0
    y1 = y0 + altura
    largura_interna = 25
    x0 = 40
    x1 = x0 + largura_interna
    x2 = x1 + largura_interna
    y0 = 0
    y1 = SIZE
    s = py5.create_shape(py5.QUAD, x1, y0, x2, y0, x1, y1, x0, y1)
    return s, altura, largura


def forma_06():
    s, altura, largura = forma_05()
    return s, altura, -largura


def setup():
    py5.size(WIDTH, HEIGHT, py5.P3D)
    py5.background(py5.color(255))
    py5.shape_mode(py5.CENTER)
    altura_anterior = ALTURA_INICIAL
    alturas = []
    x_meio = WIDTH // 2
    y_meio = HEIGHT // 2
    cor_v = py5.color(188, 0, 45)
    cor_1 = py5.color(0, 0, 0)
    cor_2 = py5.color(200, 200, 200)
    traco_1 = py5.color(0, 0, 0)
    traco_2 = py5.color(180, 180, 180)
    formas_cores = [
        (forma_01, cor_1, traco_1),
        (forma_02, cor_2, traco_2),
        (forma_03, cor_v, traco_2),
        (forma_04, cor_2, traco_2),
    ]
    with py5.push_matrix():
        py5.translate(x_meio, y_meio)
        py5.stroke(py5.color(0))
        py5.stroke_weight(5)
        # # Grid
        # for y in range(-200, 201, 200):
        #     py5.line(-x_meio, y, x_meio, y)

        # for x in range(-300, 601, 300):
        #     py5.line(x, -(y_meio), x, y_meio)

        for forma, cor, traco in formas_cores:
            s, altura, largura = forma()
            s.set_fill(cor)
            s.set_stroke(traco)
            s.set_stroke_weight(1)
            altura_anterior = altura_anterior + altura
            alturas.append(altura)
            py5.shape(s, 0, altura_anterior, largura, altura)
        cor, traco = cor_2, traco_2
        py5.shape_mode(py5.CORNERS)
        for forma in [forma_05, forma_06]:
            s, altura, largura = forma()
            s.set_fill(cor)
            s.set_stroke(traco)
            s.set_stroke_weight(1)
            extremo = SIZE // 2
            if largura > 0:
                x = -extremo
            else:
                x = extremo
            y = ALTURA_INICIAL + sum(alturas[0:2])
            print(largura, x, y, x + largura, y + altura)
            py5.shape(s, x, y, x + largura, y + altura)

    write_legend([cor_v], IMG_NAME)


def key_pressed():
    key = py5.key
    if key == " ":
        save_and_close()


def save_and_close():
    py5.no_loop()
    save_image(IMG_NAME, "png")
    py5.exit_sketch()


py5.run_sketch()
