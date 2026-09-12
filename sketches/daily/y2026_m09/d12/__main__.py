"""2026-09-12
Padrões 08
Exercício de padrões coloridos
ericof.com
png
Sketch,py5,CreativeCoding
"""

from sketches.padroes import biblioteca as b
from sketches.padroes.tipos import CoresPadrao
from sketches.utils.draw import canvas
from sketches.utils.draw.cores.paletas import gera_paleta
from sketches.utils.draw.grade import cria_grade
from sketches.utils.helpers import sketches as helpers

import py5


sketch = helpers.info_for_sketch(__file__, __doc__)

cor_fundo = py5.color(0)

paleta = gera_paleta("azul-02", True)

largura_x = 100
largura_y = 100
padrao_largura = largura_x * 0.95
padrao_altura = largura_y * 0.95
densidade = 2
traco = 2
angulos = [0, 45, 90]


def inicializa():
    payload = {
        "traco": traco,
        "largura": padrao_largura,
        "altura": padrao_altura,
        "densidade": densidade,
    }
    padroes = [
        padrao(**payload) for padrao in b.Biblioteca.get_categoria("quadrados").values()
    ]
    posicoes = cria_grade(
        *helpers.DIMENSOES.internal, 0, 0, largura_x, largura_y, False
    )
    grade = []
    for x, y in posicoes:
        padrao = py5.random_choice(padroes)
        cores = CoresPadrao(
            py5.color("#CCCCCC"),
            py5.color(paleta[0]),
            py5.color(paleta[3]),
        )
        paleta.rotate(py5.random_int(1, len(paleta)))
        rotacao = float(py5.random_choice(angulos))
        grade.append((x, y, padrao, cores, rotacao))
    return grade


def setup():
    global grade
    py5.size(*helpers.DIMENSOES.external, py5.P3D)
    py5.image_mode(py5.CENTER)
    grade = inicializa()


def draw():
    py5.background(cor_fundo)
    with py5.push():
        py5.translate(*helpers.DIMENSOES.pos_interno, -2)
        for x, y, padrao, cores, rotacao in grade:
            # O padrao rasteriza em `densidade`x e devolve uma imagem desse
            # tamanho; o destino explicito a traz de volta ao tamanho nominal.
            imagem = padrao(rotacao, cores)
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
