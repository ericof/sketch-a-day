"""2026-04-29
Vitral 06
Inspirado em vitrais, sketch com hexágonos e octágonos.
ericof.com|https://ericof.com/en/sketches/2023-06-01
png
Sketch,py5,CreativeCoding,Mosaico,Vitral
"""

from sketches.utils.draw import canvas
from sketches.utils.draw.formas import gera_hexagono
from sketches.utils.draw.formas import gera_octagono
from sketches.utils.draw.grade import cria_grade_ex
from sketches.utils.helpers import sketches as helpers

import py5


sketch = helpers.info_for_sketch(__file__, __doc__)

cor_fundo = py5.color(0)


hexagono: py5.Py5Shape | None = None
octagono: py5.Py5Shape | None = None
tamanho = 40
h_diff = 40
grade: list[tuple[int, float, int, float]] | None = None
celula_x = 0
celula_y = 0


def calcula_grade() -> list[tuple[int, float, int, float]]:
    """Calcula a grade escalonada de células para posicionar os elementos.

    Sorteia novas dimensões de célula (``celula_x`` e ``celula_y``) num
    intervalo entre ``1.2x`` e ``1.5x`` ``tamanho`` e gera a grade
    alternada via :func:`cria_grade_ex`. Cada item devolvido é a tupla
    ``(idx, x, idy, y)`` com índices e coordenadas.

    :returns: lista de tuplas ``(idx, x, idy, y)``.
    """
    global grade, celula_x, celula_y
    celula_x = int(tamanho * py5.random(1.2, 1.5))
    celula_y = int(tamanho * py5.random(1.2, 1.5))
    grade = cria_grade_ex(
        largura=helpers.DIMENSOES.external[0],
        altura=helpers.DIMENSOES.external[1],
        margem_x=0,
        margem_y=0,
        celula_x=celula_x,
        celula_y=celula_y,
        alternada=True,
    )
    return grade


def cores_elemento(idx: int, idy: int, angulo: float) -> tuple[int, int]:
    """Deriva as cores de traço e preenchimento de um elemento da grade.

    Combina os índices de coluna (``idx``) e linha (``idy``) com pesos
    coprimos antes de aplicar ângulo dourado (matiz) e módulos primos
    (saturação e brilho), produzindo distribuição 2D quasi-aleatória —
    sem bandas horizontais nem verticais perceptíveis. O matiz percorre
    todo o círculo cromático; saturação varia em ``60..100`` (módulo
    41) e brilho em ``80..99`` (módulo 20), mantendo a paleta sempre
    luminosa. O ``angulo`` atua como offset adicional do matiz e modula
    a transparência; o traço permanece escuro, reforçando o efeito de
    vitral.

    :param idx: índice da coluna na grade.
    :param idy: índice da linha na grade.
    :param angulo: ângulo, em graus, usado como offset do matiz e
        para modular a transparência do preenchimento.
    :returns: par ``(traco, cor)`` com os valores ``py5.color`` para
        stroke e fill.
    """
    h = ((idx + idy * 17) * 137.508 + h_diff + angulo * 0.7) % 360
    s = 60 + ((idx + idy * 11) % 41)
    b = 80 + ((idx * 7 + idy * 13) % 20)
    t = angulo / 6 + 60
    traco = py5.color(h, 30, 0)
    cor = py5.color(h, s, b, t)
    return traco, cor


def setup():
    """Inicializa o sketch.

    Define o tamanho do canvas, ativa P3D e o modo de cor HSB, cria os
    shapes-base (hexágono e octágono) e calcula a grade inicial.
    """
    global hexagono, octagono
    py5.size(*helpers.DIMENSOES.external, py5.P3D)
    py5.shape_mode(py5.CENTER)
    py5.color_mode(py5.HSB, 360, 100, 100)
    hexagono = gera_hexagono()
    octagono = gera_octagono()
    calcula_grade()


def draw():
    """Desenha o quadro atual em duas passadas.

    A primeira passada renderiza os hexágonos preenchidos a uma
    profundidade ``z=-20``, com cor obtida via :func:`cores_elemento`
    (``angulo=90`` fixo) e alternância de stroke por paridade do índice
    — pares sem stroke, ímpares com traço escuro — em escala
    ``celula * 1.4`` para gerar sobreposição. A segunda passada,
    deslocada em ``z=+3``, sobrepõe os octágonos apenas em outline (sem
    fill) na escala original da célula, criando o detalhe de moldura
    típico de vitral. Ao final, renderiza a moldura de créditos do
    sketch.
    """
    py5.background(cor_fundo)
    if grade and hexagono and octagono:
        with py5.push():
            py5.translate(0, 0, -20)
            for idx, x, idy, y in grade:
                traco, cor = cores_elemento(idx, idy, 90)
                forma = hexagono
                if idx % 2:
                    forma.set_stroke(traco)
                    forma.set_stroke_weight(2)
                else:
                    forma.set_stroke(False)
                forma.set_fill(cor)
                py5.shape(forma, x, y, celula_x * 1.2, celula_y * 1.2)
            py5.translate(0, 0, 3)
            for idx, x, idy, y in grade:
                if (idx + idy) % 4 > 0:
                    continue
                traco, cor = cores_elemento(idx, idy, 90)
                forma = octagono
                forma.set_stroke(traco)
                forma.set_stroke_weight(8)
                forma.set_fill(False)
                py5.shape(forma, x, y, celula_x, celula_y)
    msg = f"T: {tamanho}, H: {h_diff}"
    # Credits and go
    canvas.sketch_frame(
        sketch,
        cor_fundo,
        "large_transparent_white",
        "transparent_white",
        version=2,
        msg=msg,
    )


def key_pressed():
    """Trata atalhos de teclado.

    - ``space``: salva a imagem e encerra o sketch.
    - ``r``: recalcula (reembaralha) a grade de pontos.
    - ``+`` / ``-``: incrementa ou decrementa o tamanho do hexágono em 2px
      e recalcula a grade.
    - ``>`` / ``<``: incrementa ou decrementa a diferença de matiz em 2 unidades
      e recalcula a grade.
    """
    global tamanho, h_diff
    key = py5.key
    match key:
        case " ":
            save_and_close()
        case "r":
            calcula_grade()
        case "+":
            tamanho += 2
            calcula_grade()
        case "-":
            tamanho -= 2
            calcula_grade()
        case ">":
            h_diff += 2
            calcula_grade()
        case "<":
            h_diff -= 2
            calcula_grade()


def save_and_close():
    """Pausa o loop, salva o PNG do sketch e encerra a execução."""
    py5.no_loop()
    canvas.save_sketch_image(sketch)
    py5.exit_sketch()


if __name__ == "__main__":
    py5.run_sketch()
