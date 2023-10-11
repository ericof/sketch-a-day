"""2023-10-11"""
from helpers import CelulaV4 as Celula
from helpers import Grade
from helpers import HEIGHT
from helpers import save_image
from helpers import WIDTH
from helpers import write_legend
from pathlib import Path

import py5


IMG_NAME = Path(__file__).name.replace(".py", "")

CORES = [
    py5.color(240),
]

LADO = 50

FATOR = 0.6
FATOR_LARGURA_INTERNA = 0.85


def forma_01():
    limite = LADO * FATOR
    bz1 = LADO * FATOR
    s = py5.create_shape()
    with s.begin_shape():
        s.vertex(0, 0)
        s.vertex(0, LADO)
        s.vertex(limite, LADO)
        s.bezier_vertex(limite, LADO, bz1, bz1, LADO, limite)
        s.vertex(LADO, limite)
        s.vertex(LADO, 0)
        s.vertex(0, 0)
    return s


def forma_02():
    limite = LADO * FATOR
    bz1 = LADO * FATOR
    bz2 = (LADO - limite) * FATOR
    s = py5.create_shape()
    with s.begin_shape():
        s.vertex(0, 0)
        s.vertex(0, limite)
        s.bezier_vertex(0, limite, bz2, bz1, LADO - limite, LADO)
        s.vertex(LADO - limite, LADO)
        s.vertex(limite, LADO)
        s.bezier_vertex(limite, LADO, bz1, bz1, LADO, limite)
        s.vertex(LADO, 0)
        s.vertex(0, 0)
    return s


def forma_03():
    limite = LADO * FATOR
    bz1 = LADO * FATOR
    bz2 = (LADO - limite) * FATOR
    s = py5.create_shape()
    with s.begin_shape():
        s.vertex(0, 0)
        s.vertex(0, LADO)
        s.vertex(limite, LADO)
        s.bezier_vertex(limite, LADO, bz1, bz1, LADO, limite)
        s.vertex(LADO, limite)
        s.vertex(LADO, LADO - limite)
        s.bezier_vertex(LADO, LADO - limite, bz1, bz2, limite, 0)
        s.vertex(limite, 0)
        s.vertex(0, 0)
    return s


def circulo(s, inicio, meio, fim):
    s.vertex(inicio, meio)
    s.bezier_vertex(inicio, meio, inicio, inicio, meio, inicio)
    s.vertex(meio, inicio)
    s.bezier_vertex(meio, inicio, fim, inicio, fim, meio)
    s.vertex(fim, meio)
    s.bezier_vertex(fim, meio, fim, fim, meio, fim)
    s.vertex(meio, fim)
    s.bezier_vertex(meio, fim, inicio, fim, inicio, meio)
    s.vertex(inicio, meio)


def forma_centro():
    inicio = 0
    fim = LADO
    meio = fim // 2
    s = py5.create_shape()
    with s.begin_shape():
        circulo(s, inicio, meio, fim)
        with s.begin_contour():
            inicio = 6
            fim = LADO - inicio
            meio = (fim - inicio) // 2
            circulo(s, inicio, meio, fim)

    return s


def _factory(pontos):
    s = py5.create_shape()
    with s.begin_shape():
        for x, y in pontos:
            s.vertex(x, y)
    return s


def setup():
    py5.size(WIDTH, HEIGHT, py5.P3D)
    py5.background(py5.color(120))
    formas = [forma_01(), forma_02(), forma_03(), forma_centro()]
    linhas = 36
    colunas = 36
    margem = -1600
    bloco = 3
    largura = (py5.width - (2 * margem)) / colunas
    grade = Grade(0, 0, WIDTH, HEIGHT, colunas, linhas, margem, margem)
    for idx, slot in enumerate(grade):
        linha = idx // colunas
        coluna = idx % colunas
        coluna_interna = coluna % bloco
        linha_interna = linha % bloco
        forma = formas[1] if (linha_interna + coluna_interna) % 2 else formas[0]
        largura_interna = largura * FATOR_LARGURA_INTERNA
        x, y, largura_celula = slot.x, slot.y, largura
        if linha_interna == 1:
            # Linha do meio
            forma = formas[2]
            if coluna_interna == 1:
                largura_interna = largura
                forma = formas[3]
        celula = Celula(
            x,
            y,
            largura_celula,
            [forma],
            CORES,
            border=0,
        )
        celula.largura_interna = largura_interna
        celula.espelhada = coluna_interna == 2
        celula.espelhada_vertical = linha_interna == 2
        if linha_interna == coluna_interna == 1:
            celula.fill = True
            celula.largura_interna = largura

        slot.celulas.append(celula)
    with py5.push_matrix():
        py5.translate(WIDTH // 2, HEIGHT // 2)
        py5.rotate_x(py5.radians(60))
        py5.translate(-(WIDTH // 2), -(HEIGHT // 2))
        grade.desenha()
    write_legend([py5.color(0, 0, 0)], IMG_NAME)


def key_pressed():
    key = py5.key
    if key == " ":
        save_and_close()


def save_and_close():
    py5.no_loop()
    save_image(IMG_NAME, "png")
    py5.exit_sketch()


py5.run_sketch()
