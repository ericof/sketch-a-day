"""2026-07-10
Recursive Squares 07
Desenha quadrados recursivamente
ericof.com
png
Sketch,py5,CreativeCoding
"""

from collections import deque
from sketches.utils.draw import canvas
from sketches.utils.draw.cores.paletas import gera_paleta
from sketches.utils.helpers import sketches as helpers

import py5


sketch = helpers.info_for_sketch(__file__, __doc__)

paleta = gera_paleta("pastel")

grade_n = 9
tamanho_quadrado = 80


def constroi_areas() -> list[tuple[float, float, int, list[str | int], int]]:
    """Monta a grade ``grade_n`` x ``grade_n`` de areas centradas nas celulas.

    Cada area recebe o centro da sua celula no painel interno e o tamanho base
    ``tamanho_quadrado``. Posicionar pelo centro da celula mantem a grade valida
    para qualquer ``grade_n``. O ``z_sinal`` alterna por anel concentrico
    (distancia de Chebyshev ate a celula central ``grade_n // 2``): aneis pares
    -- centro (perimetro 1), perimetro 5, ... -- empilham em +z; aneis impares
    -- perimetro 3, 7, ... -- empilham em -z. O padrao e simetrico so em grades
    impares.

    :returns: Lista de ``(cx, cy, tamanho_quadrado, paleta, z_sinal)`` por celula.
    """
    largura, altura = helpers.DIMENSOES.internal
    meio = grade_n // 2
    return [
        (
            largura * (col + 0.5) / grade_n,
            altura * (lin + 0.5) / grade_n,
            tamanho_quadrado,
            paleta,
            1 if max(abs(col - meio), abs(lin - meio)) % 2 == 0 else -1,
        )
        for lin in range(grade_n)
        for col in range(grade_n)
    ]


areas = constroi_areas()

cor_fundo = py5.color(0)
z_base = -40
z_divisor = 4
z_passo = 12
rotacao_x = 30
rotacao_z = 0
ty_buffer = 50

traco = 2


def setup():
    py5.size(*helpers.DIMENSOES.external, py5.P3D)
    py5.color_mode(py5.HSB, 360, 100, 100)
    py5.rect_mode(py5.CENTER)


def desenha_quadrados(
    cx: float, cy: float, tamanho_base: float, paleta: deque[int], z_sinal: int
) -> None:
    # Espelhamento pela POSICAO no painel (nao por idx): areas a direita do
    # centro giram no sentido oposto (reflexo horizontal) e areas abaixo do
    # centro sao refletidas verticalmente via scale(1, -1). Chavear por posicao
    # evita o bug de ``idx // 2`` agrupar pela diagonal e misturar as linhas de
    # cima e de baixo. O tamanho usa a magnitude do angulo (loop 0->70), entao
    # espelho e reflexo so mudam a orientacao -- o tamanho aparente fica identico.
    centro_x = helpers.DIMENSOES.internal[0] / 2
    centro_y = helpers.DIMENSOES.internal[1] / 2
    reflete_h = 1 if cx < centro_x else -1
    reflete_v = cy > centro_y
    z = -40
    for ida, angulo in enumerate(range(0, 75, 3)):
        tamanho = tamanho_base * (1 - (angulo / 70)) if ida else tamanho_base
        cor = paleta[0]
        paleta.rotate()
        z = z_base + ((ida // z_divisor) * z_passo * z_sinal)
        with py5.push():
            py5.translate(cx, cy, z)
            if reflete_v:
                py5.scale(1, -1)
            py5.rotate(py5.radians(reflete_h * angulo))
            py5.stroke(cor)
            py5.square(0, 0, tamanho)


def draw() -> None:
    py5.background(cor_fundo)
    py5.no_fill()
    py5.stroke_weight(traco)

    with py5.push():
        tx = helpers.DIMENSOES.pos_interno[0]
        ty = helpers.DIMENSOES.pos_interno[1] + ty_buffer
        py5.translate(tx, ty, -420)
        py5.rotate_x(py5.radians(rotacao_x))
        py5.rotate_z(py5.radians(rotacao_z))
        for cx, cy, tamanho_base, paleta, z_sinal in areas:
            paleta_deque: deque[int] = deque(paleta)
            desenha_quadrados(cx, cy, tamanho_base, paleta_deque, z_sinal)

    msg = (
        f"grade: {grade_n}x{grade_n} | tam: {tamanho_quadrado} | "
        f"z_base: {z_base} | z_divisor: {z_divisor} | "
        f"z_passo: {z_passo} | traco: {traco}"
    )
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
    global z_base, z_divisor, z_passo, traco, grade_n, tamanho_quadrado, areas
    key = py5.key
    match key:
        case "w" | "s":
            z_base += 2 if key == "w" else -2
        case "a" | "d":
            z_passo += 1 if key == "d" else -1
        case ">" | "<":
            if key == "<" and z_divisor <= 1:
                return
            z_divisor += 1 if key == ">" else -1
        case "+" | "-":
            traco += 1 if key == "+" else -1
        case "g" | "h":
            grade_n = max(1, grade_n + (1 if key == "g" else -1))
            areas = constroi_areas()
        case "o" | "l":
            tamanho_quadrado = max(10, tamanho_quadrado + (10 if key == "o" else -10))
            areas = constroi_areas()
        case " ":
            save_and_close()


def save_and_close():
    py5.no_loop()
    canvas.save_sketch_image(sketch)
    py5.exit_sketch()


if __name__ == "__main__":
    py5.run_sketch()
