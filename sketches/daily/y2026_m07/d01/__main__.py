"""2026-07-01
Caquinhos Redux 11
Pisos de caquinhos de São Paulo, grade 2x2.
ericof.com
png
Sketch,py5,CreativeCoding,Voronoi
"""

from opensimplex import OpenSimplex
from random import shuffle
from sketches.padroes.cacos import popula_cacos
from sketches.utils.draw import canvas
from sketches.utils.draw.grade import cria_grade
from sketches.utils.helpers import sketches as helpers
from sketches.utils.helpers.images import estencil_como_forma
from sketches.utils.helpers.images import resource_image_as_array
from sketches.utils.helpers.timing import report_time

import py5


sketch = helpers.info_for_sketch(__file__, __doc__)

cor_fundo = py5.color(226, 214, 187)
cor_fundo_interna = py5.color(60, 60, 45)

CORES_PESOS = (
    (py5.color(152, 59, 47), 93),
    (py5.color(218, 160, 57), 2),
    (py5.color(0), 3),
)

celula_x = 15
celula_y = 15
mult_x = 17
mult_y = 17
borda = 0.20
faixa_bagunca = 15
profundidade_caco = 4
profundidade_estencil = 20

estencil: py5.Py5Shape | None = None

# Ponto de luz controlado pelo mouse: x,y vem do cursor, altura (z) e tom sao
# fixos. A ambiente baixa evita que os cacos longe da luz fiquem pretos.
luz_altura = 800
luz_cor = py5.color(255, 244, 214)
luz_ambiente = py5.color(40, 40, 40)

# Distancia do anel de sementes-sentinela alem da area interna. Precisa ser
# maior que o deslocamento maximo de uma semente interna (mult + faixa_bagunca)
# para que toda semente visivel fique cercada e sua celula seja finita.
margem_guarda = 400

noise_generator = OpenSimplex(seed=py5.random_int(20_000))

cacos: list[py5.Py5Shape] = []


def cores_pesos() -> list[int]:
    """Expande ``CORES_PESOS`` numa lista com cada cor repetida conforme seu peso.

    A lista e embaralhada e serve de base para o sorteio ponderado de cores
    em :func:`cor_caco`.

    :returns: Lista de cores com repeticao proporcional ao peso de cada uma.
    """
    cores = []
    for cor, peso in CORES_PESOS:
        cores.extend([cor] * peso)
    shuffle(cores)
    return cores


CORES = cores_pesos()


def inicializa():
    global cacos, estencil
    grade = cria_grade(*helpers.DIMENSOES.external, 0, 0, celula_x, celula_y)
    with report_time("Calculando..."):
        cacos = popula_cacos(
            *helpers.DIMENSOES.external,
            celula_x,
            celula_y,
            grade,
            mult_x,
            mult_y,
            faixa_bagunca,
            margem_guarda,
            borda,
            profundidade_caco,
            noise_generator,
            CORES,
        )
    arr_cidade = resource_image_as_array("sampa-reverso.png")
    arr_estado = resource_image_as_array("sao-paulo.png")
    # Grade 2x2 em xadrez (estado/cidade) unida num unico GROUP. Cada celula
    # mede metade do painel interno; cada estencil e construido ja escalado e
    # posicionado na sua celula (escala/origem), entao o draw desenha a grade
    # inteira com um so py5.shape().
    meia_x = helpers.DIMENSOES.internal[0] / 2
    meia_y = helpers.DIMENSOES.internal[1] / 2
    layout = (
        (arr_estado, 0, 0),
        (arr_cidade, 1, 0),
        (arr_cidade, 0, 1),
        (arr_estado, 1, 1),
    )
    grade_estencil = py5.create_shape(py5.GROUP)
    for arr, col, lin in layout:
        grade_estencil.add_child(
            estencil_como_forma(
                arr,
                cor_fundo,
                profundidade=profundidade_estencil,
                escala=meia_x / arr.shape[1],
                origem=(col * meia_x, lin * meia_y),
            )
        )
    estencil = grade_estencil


def setup():
    py5.size(*helpers.DIMENSOES.external, py5.P3D)
    inicializa()


def desenha_fundo(cor: int):
    """Desenha o fundo por baixo dos caquinhos."""
    with py5.push():
        py5.fill(cor)
        py5.no_stroke()
        py5.rect(0, 0, *helpers.DIMENSOES.external)


def draw():
    py5.background(cor_fundo)
    # Posicao da luz no espaco interno: o mouse e screen-space, entao
    # descontamos a origem do painel (pos_interno).
    luz_x = py5.mouse_x - helpers.DIMENSOES.pos_interno[0]
    luz_y = py5.mouse_y - helpers.DIMENSOES.pos_interno[1]
    with py5.push():
        py5.translate(0, 0, -25)
        # Fundo desenhado antes das luzes para manter o rejunte chapado; os
        # prismas se assentam nele (base em z=0) e sobem em direcao a camera.
        desenha_fundo(cor_fundo_interna)
        # Luz pontual seguindo o mouse + ambiente baixa, no mesmo espaco dos
        # cacos. Iluminam tambem o estencil, para o poco ganhar relevo.
        py5.ambient_light(
            py5.red(luz_ambiente), py5.green(luz_ambiente), py5.blue(luz_ambiente)
        )
        py5.point_light(
            py5.red(luz_cor),
            py5.green(luz_cor),
            py5.blue(luz_cor),
            luz_x,
            luz_y,
            luz_altura,
        )
        for forma in cacos:
            py5.shape(forma)
        # Estencil iluminado: as paredes verticais do poco sombreiam diferente
        # da face frontal, revelando a profundidade. A base do poco assenta
        # logo acima do topo dos cacos.
        with py5.push():
            py5.translate(*helpers.DIMENSOES.pos_interno, profundidade_caco)
            py5.shape(estencil)
    py5.no_lights()

    msg = (
        f"celula (x - y): {celula_x} - {celula_y} | "
        f"borda: {borda:.2f} | "
        f"bagunca: {faixa_bagunca} | "
        f"prof: {profundidade_caco} | "
        f"est: {profundidade_estencil} | "
        f"luz (x - y): {luz_x} - {luz_y}"
    )
    # Credits and go
    canvas.sketch_frame(
        sketch,
        py5.color(0),
        "large_transparent_white",
        "transparent_white",
        version=2,
        msg=msg,
    )


def key_pressed():
    global celula_x, celula_y, borda, faixa_bagunca, profundidade_caco
    global profundidade_estencil, estencil
    key = py5.key
    match key:
        case "r":
            inicializa()
        case ">" | "<":
            passo = 2 if key == ">" else -2
            celula_x = max(4, celula_x + passo)
            celula_y = max(4, celula_y + passo)
            inicializa()
        case "w" | "s":
            borda = min(0.6, max(0.0, borda + (0.05 if key == "w" else -0.05)))
            inicializa()
        case "+" | "-":
            faixa_bagunca = max(0, faixa_bagunca + (5 if key == "+" else -5))
            inicializa()
        case "e" | "d":
            profundidade_caco = max(0, profundidade_caco + (1 if key == "e" else -1))
            inicializa()
        case "o" | "l":
            profundidade_estencil = max(
                0, profundidade_estencil + (2 if key == "o" else -2)
            )
            inicializa()
        case " ":
            save_and_close()


def save_and_close():
    py5.no_loop()
    canvas.save_sketch_image(sketch)
    py5.exit_sketch()


if __name__ == "__main__":
    py5.run_sketch()
