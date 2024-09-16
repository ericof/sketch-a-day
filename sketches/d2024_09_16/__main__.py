"""2024-09-16
Rotating Drum 1
Estudos para a criação de uma tômbola para sorteios.
png
Sketch,py5,CreativeCoding
"""

import math

import py5

from utils import helpers

sketch = helpers.info_for_sketch(__file__, __doc__)


LADOS = []
H = 220
S = 50
B = 100


def fonte(nome: str, tamanho: float = 20.0) -> py5.Py5Font:
    todas = py5.Py5Font.list()
    if nome not in todas:
        raise ValueError(f"Fonte {nome} não disponível")
    fonte = py5.create_font(nome, tamanho)
    return fonte


def cria_face(
    largura: int, altura: int, fundo: py5.color, cor: py5.color, texto: str
) -> py5.Py5Graphics:
    image = py5.create_graphics(largura, abs(altura), py5.P3D)
    with image.begin_draw():
        image.background(fundo)
        image.color(cor)
        image.text_font(fonte("UbuntuMonoDerivativePowerline-Regular"))
        image.text_align(py5.CENTER, py5.CENTER)
        image.text(texto, largura / 2, altura / 2)
    return image


def desenha_cilindro(raio: float, altura: float, lados: int):
    angulo_passo = py5.TWO_PI / lados  # Angulo entre cada segmento
    # Desenha os lados
    forma = py5.create_shape()
    with forma.begin_shape(py5.QUAD_STRIP):
        for idx, i in enumerate(range(lados + 1)):
            s = 50 if idx % 2 else 100
            cor = py5.color(H, s, B)
            forma.fill(cor)
            forma.no_stroke()
            angulo = idx * angulo_passo
            x = raio * math.cos(angulo)
            z = raio * math.sin(angulo)
            forma.vertex(x, -altura / 2, z)  # Vertex da base
            forma.vertex(x, altura / 2, z)  # Vertex do topo
    py5.shape(forma)
    # Desenha o topo do cilindro
    with py5.begin_shape(py5.TRIANGLE_FAN):
        py5.vertex(0, -altura / 2, 0)  # Ponto central do círculo superio
        for idx, i in enumerate(range(lados + 1)):
            angulo = i * angulo_passo
            x = raio * math.cos(angulo)
            z = raio * math.sin(angulo)
            py5.vertex(x, -altura / 2, z)

    # Desenhamos a base do cilindro
    with py5.begin_shape(py5.TRIANGLE_FAN):
        py5.vertex(0, altura / 2, 0)  # Ponto central da base do círculo
        for idx, i in enumerate(range(lados + 1)):
            angulo = i * angulo_passo
            x = raio * math.cos(-angulo)
            z = raio * math.sin(-angulo)
            py5.vertex(x, altura / 2, z)


def setup():
    global LADOS
    py5.size(helpers.LARGURA, helpers.ALTURA, py5.P3D)
    py5.background(0)
    py5.color_mode(py5.HSB, 360, 100, 100)
    for idx in range(20):
        texto = "py5coding.org"
        s = 50 if idx % 2 else 100
        fundo = py5.color(H, s, B)
        image = cria_face(200, 200 // 3, fundo, py5.color(H, 0, 100), texto)
        LADOS.append((image, fundo))


def draw():
    py5.background(0)
    py5.lights()  # Enable lighting
    with py5.push_matrix():
        py5.translate(py5.width / 2, py5.height / 2, 400)
        py5.rotate_x(-py5.PI / 6)
        py5.rotate_z(py5.radians(90))
        py5.rotate_y(py5.frame_count * 0.02)
        desenha_cilindro(raio=100, altura=200, lados=len(LADOS))
    helpers.write_legend(sketch=sketch)


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
