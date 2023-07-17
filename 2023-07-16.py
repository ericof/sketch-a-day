"""2023-07-16"""
from helpers import HEIGHT
from helpers import save_image
from helpers import WIDTH
from helpers import write_legend
from pathlib import Path

import py5

IMG_NAME = Path(__file__).name.replace(".py", "")

PONTOS = []


def sorteia_cores():
    h1 = 210
    h2 = 30
    s = py5.random(22, 90)
    b = py5.random(50, 75)
    return (py5.color(h2, s, b), py5.color(h1, s, b + 10))


def poligono() -> py5.Py5Shape:
    s = py5.create_shape()
    with s.begin_closed_shape():
        s.vertex(0, 0)
        s.vertex(60, 0)
        s.vertex(60, 60)
        s.vertex(0, 60)
    return s


def circulo() -> py5.Py5Shape:
    s = py5.create_shape(py5.ELLIPSE, -25, 0, 50, 50)
    return s


def setup():
    py5.size(WIDTH, HEIGHT, py5.P3D)
    py5.color_mode(py5.HSB, 360, 100, 100)
    buffer = 1
    largura = HEIGHT // 10
    linhas = HEIGHT + (buffer * largura) // largura
    colunas = HEIGHT + (buffer * largura) // largura
    buffer_linha = 0
    for i in range(linhas):
        y = i * largura - buffer_linha
        buffer_coluna = 0
        for j in range(colunas):
            x = j * largura - buffer_coluna
            PONTOS.append((x, y, largura))
    print(f"Finalizado Setup com {linhas} {colunas}")


def draw():
    forma1 = circulo()
    forma2 = poligono()
    total_pontos = len(PONTOS)
    py5.ellipse_mode(py5.CENTER)
    py5.shape_mode(py5.CENTER)
    with py5.push_matrix():
        py5.translate(WIDTH / 2, HEIGHT / 2)
        py5.rotate(py5.radians(0))
        print(f"{total_pontos}")
        for idx, (base_x, base_y, largura) in enumerate(PONTOS):
            if idx % 100 == 0:
                print(f"  - {(idx / total_pontos) * 100}")
            x = base_x - WIDTH
            y = base_y - HEIGHT
            cor1, cor2 = sorteia_cores()
            # Desenha circulo
            largura_circulo = largura * 0.8
            forma1.set_fill(cor2)
            py5.shape(forma1, x, y, largura_circulo, largura_circulo)
            # Desenha quadrado
            forma2.set_fill(cor1)
            py5.shape(forma2, x, y, largura, largura)
    write_legend(img_name=IMG_NAME)
    save_image(IMG_NAME, "png")
    py5.no_loop()


def key_pressed():
    key = py5.key
    if key == " ":
        save_image(IMG_NAME, "png")
        py5.exit_sketch()


py5.run_sketch()
