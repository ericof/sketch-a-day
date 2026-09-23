"""2026-09-23
Padrões 19
Exercício de padrões coloridos
ericof.com
png
Sketch,py5,CreativeCoding
"""

from collections import deque
from random import shuffle
from sketches.padroes import biblioteca as b
from sketches.padroes.tipos import CoresPadrao
from sketches.utils.draw import canvas
from sketches.utils.draw.grade import cria_grade
from sketches.utils.helpers import sketches as helpers

import py5


sketch = helpers.info_for_sketch(__file__, __doc__)

cor_fundo = py5.color(0)

largura_x = 142
largura_y = 142
margem_x = 3
margem_y = 3
padrao_largura = largura_x
padrao_altura = largura_y
densidade = 2
traco = 4
angulos = [45]


def inicializa():
    payload = {
        "traco": traco,
        "largura": int(padrao_largura),
        "altura": int(padrao_altura),
        "densidade": densidade,
    }
    padroes = [
        *[padrao(**payload) for padrao in b.Biblioteca.get_categoria("ondas").values()],
    ]
    shuffle(padroes)
    posicoes = cria_grade(
        *helpers.DIMENSOES.external, margem_x, margem_y, largura_x, largura_y, True
    )
    grade = []
    paleta = deque([
        "#007749",
        "#FFB612",
        "#000000",
        "#DE3831",
        "#002395",
    ])
    for x, y in posicoes:
        padrao = py5.random_choice(padroes)
        cores = CoresPadrao(
            py5.color(paleta[0]),
            py5.color(paleta[1]),
            py5.color(paleta[2]),
        )
        paleta.rotate()
        rotacao = float(py5.random_choice(angulos))
        # Rasteriza uma vez por celula: cada chamada cria um Py5Graphics,
        # redesenha o padrao e copia os pixels — custo que nao pode ficar
        # dentro do laco de `draw()`.
        imagem = padrao(rotacao, cores)
        grade.append((x, y, imagem))
    return grade


def setup():
    global grade
    py5.size(*helpers.DIMENSOES.external, py5.P3D)
    py5.image_mode(py5.CENTER)
    grade = inicializa()


def draw():
    py5.background(cor_fundo)
    with py5.push():
        py5.translate(0, 0, -2)
        for x, y, imagem in grade:
            # A imagem foi rasterizada em `densidade`x e tem o lado desse
            # tamanho; o destino explicito a traz de volta ao tamanho nominal.
            py5.image(
                imagem,
                x + largura_x / 2,
                y + largura_y / 2,
                padrao_largura,
                padrao_altura,
            )

    # Credits and go
    canvas.sketch_frame(
        sketch,
        cor_fundo,
        "large_transparent_white",
        "transparent_white",
        version=2,
    )


def key_pressed():
    global grade
    key = py5.key
    match key:
        case "r":
            grade = inicializa()
        case " ":
            save_and_close()


def save_and_close():
    py5.no_loop()
    canvas.save_sketch_image(sketch)
    py5.exit_sketch()


if __name__ == "__main__":
    py5.run_sketch()
