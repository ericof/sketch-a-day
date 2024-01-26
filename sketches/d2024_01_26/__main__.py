"""2024-01-26
Genuary 26 - Grow a seed.
Árvore com tronco marrom, folhas amareladas e flores vermelhas.
png
Sketch,py5,CreativeCoding,genuary,genuary26
"""
import py5

from utils import helpers

sketch = helpers.info_for_sketch(__file__, __doc__)

MARGEM = 70

regras = {
    "X": "F+[![X]-X!][@X][--![XP]!]-F[-GFXP]+XP",
    "F": "FGF",
}
axioma = "X"
iteracoes = 6
max_angulo = 35
angulo = max_angulo
tamanho = 4
escala = 0.5

# cores
caule = "#452711"
flor = (200, 80, 0)
folha = (255, 200, 0)
no = (0, 255, 0)


def setup():
    global nova_frase
    py5.size(helpers.LARGURA, helpers.ALTURA, py5.P3D)
    frase_inicial = axioma
    for n in range(iteracoes):
        nova_frase = ""
        for simbolo in frase_inicial:
            nova_frase = nova_frase + regras.get(simbolo, simbolo)
        frase_inicial = nova_frase


def draw():
    global angulo
    tronco = 6
    py5.background(252, 249, 230)
    with py5.push_style():
        py5.stroke(72, 111, 56)
        py5.fill(72, 111, 56)
        py5.rect_mode(py5.CORNERS)
        py5.rect(0, py5.height - MARGEM, py5.width, py5.height)
    helpers.write_legend(sketch=sketch)
    py5.translate(py5.width / 2, py5.height - MARGEM)
    py5.rotate_y(py5.radians(py5.mouse_x))
    for simbolo in nova_frase:
        if simbolo == "F":
            py5.stroke_weight(tronco)
            py5.stroke(caule)
            py5.line(0, 0, 0, -tamanho)
            direcao = -1 if angulo > 0 else 1
            py5.bezier(
                0,
                0,
                -tamanho,
                (-tamanho / 4) * direcao,
                -tamanho,
                (-tamanho / 4) * direcao * 2,
                0,
                -tamanho,
            )
            py5.rotate_y(py5.HALF_PI / 18)
            if tronco > 1:
                tronco -= 0.1
        elif simbolo == "G":
            py5.translate(0, -tamanho)
        elif simbolo == "+":
            py5.rotate(py5.radians(-angulo))
        elif simbolo == "-":
            py5.rotate(py5.radians(angulo))
        elif simbolo == "!":
            angulo = -angulo
        elif simbolo == "[":
            py5.push_matrix()
        elif simbolo == "]":
            py5.pop_matrix()
        elif simbolo == "@":
            py5.scale(escala)
            py5.stroke_weight(tamanho)
            py5.stroke(*no)
            py5.point(0, 0)
        elif simbolo == "X":
            py5.stroke_weight(tamanho)
            py5.stroke(*folha)
            with py5.push_matrix():
                for idx in range(30, 180, 60):
                    py5.rotate(py5.radians(idx))
                    py5.point(0, +tamanho / 3)

        elif simbolo == "P":
            py5.stroke_weight(tamanho)
            py5.stroke(*flor)
            with py5.push_matrix():
                for idx in range(0, 180, 60):
                    py5.rotate(py5.radians(idx))
                    py5.point(0, +tamanho / 2)


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
