"""2026-08-12
Acumulando Pontos 06
Usando polígonos regulares, criamos uma circunferência de pontos.
ericof.com|https://ericof.com/en/sketches/2023-09-03
png
Sketch,py5,CreativeCoding
"""

from sketches.padroes.poligonos import gera_poligono_regular
from sketches.padroes.poligonos import vertices_poligono_regular
from sketches.utils.draw import canvas
from sketches.utils.draw.cores.paletas import gera_paleta
from sketches.utils.helpers import sketches as helpers

import numpy as np
import py5


sketch = helpers.info_for_sketch(__file__, __doc__)

cor_fundo = py5.color(0)

lados = 9
rotacao = 0.1

pontos_por_frame = 20
fator_atracao = 0.666
peso_ponto = 7
faixas_peso = 8
escala_ruido = 0.003
paleta = gera_paleta("Okazz-230905a")


vertices: np.ndarray
camada: py5.Py5Graphics
poligono: py5.Py5Shape


def inicializa() -> None:
    """Cria o polígono-carimbo, a camada acumuladora e o polígono-contorno.

    O polígono-carimbo é a forma replicada a cada ponto por
    :func:`acumula_pontos`. O polígono-contorno delimita a região onde os
    pontos nascem; seus vértices vêm de :func:`vertices_poligono_regular`, em
    coordenadas locais da área interna.
    """
    global vertices, camada, poligono
    poligono = gera_poligono_regular(lados, peso_ponto, peso_ponto, rotacao)
    camada = py5.create_graphics(*helpers.DIMENSOES.internal, py5.P3D)
    with camada.begin_draw():
        camada.color_mode(py5.HSB, 360, 100, 100)
        camada.clear()
    largura, altura = camada.width, camada.height
    vertices = vertices_poligono_regular(largura, altura, lados, rotacao)


def dentro_do_poligono(x: float, y: float) -> bool:
    """Verifica se um ponto está dentro do polígono convexo.

    :param x: Coordenada x, em coordenadas locais da área interna.
    :param y: Coordenada y, em coordenadas locais da área interna.
    :returns: ``True`` se o ponto estiver dentro do polígono.
    """
    arestas = np.roll(vertices, -1, axis=0) - vertices
    para_ponto = np.array([x, y]) - vertices
    cruzados = arestas[:, 0] * para_ponto[:, 1] - arestas[:, 1] * para_ponto[:, 0]
    return bool(np.all(cruzados >= 0) or np.all(cruzados <= 0))


def sorteia_ponto_interno() -> tuple[float, float]:
    """Sorteia um ponto uniforme dentro do polígono, por rejeição na bounding box.

    :returns: Par ``(x, y)`` em coordenadas locais da área interna.
    """
    x_min, y_min = vertices.min(axis=0)
    x_max, y_max = vertices.max(axis=0)
    while True:
        x = py5.random(x_min, x_max)
        y = py5.random(y_min, y_max)
        if dentro_do_poligono(x, y):
            return x, y


def cor_do_ponto() -> int:
    """Escolhe a cor de um ponto acumulado.

    Ponto de extensão: define a cor sem tocar na geometria nem no tamanho.

    :returns: Uma cor da paleta do sketch.
    """
    return py5.random_choice(paleta)


def tamanho_ponto(x: float, y: float) -> int:
    """Calcula o tamanho do carimbo de um ponto acumulado.

    Ponto de extensão análogo a :func:`cor_do_ponto`: define a escala com que
    o polígono-carimbo é desenhado, sem tocar na posição nem na cor. O valor
    vem de um campo de ruído amostrado na posição final do ponto, de modo que
    pontos vizinhos tendem a ter tamanhos próximos e o acúmulo forma manchas
    irregulares.

    :param x: Coordenada x final do ponto, em coordenadas locais da camada.
    :param y: Coordenada y final do ponto, em coordenadas locais da camada.
    :returns: Largura e altura do carimbo em pixels, de ``peso_ponto`` a
        ``peso_ponto + faixas_peso - 1``.
    """
    ruido = float(py5.noise(x * escala_ruido, y * escala_ruido))
    faixa = py5.remap(ruido, 0.25, 0.75, 0, faixas_peso)
    return int(py5.constrain(faixa, 0, faixas_peso - 1)) + peso_ponto


def acumula_pontos(quantidade: int) -> None:
    """Desenha na camada uma cópia do polígono-carimbo por ponto sorteado.

    Cada ponto nasce numa posição uniforme dentro do polígono-contorno e é
    deslocado ``fator_atracao`` do caminho até um vértice sorteado. A cor fica
    a cargo de :func:`cor_do_ponto` e o tamanho, de :func:`tamanho_ponto`.

    :param quantidade: Número de carimbos a acrescentar nesta chamada.
    """
    with camada.begin_draw():
        for _ in range(quantidade):
            x0, y0 = sorteia_ponto_interno()
            idx = py5.random_int(0, lados - 1)
            x1, y1 = vertices[idx]
            x = float(py5.lerp(x0, x1, fator_atracao))
            y = float(py5.lerp(y0, y1, fator_atracao))
            with py5.push():
                cor = cor_do_ponto()
                tamanho = tamanho_ponto(x, y)
                poligono.set_stroke(cor)
                poligono.set_stroke_weight(1)
                poligono.set_fill(cor)
                camada.shape(poligono, x, y, tamanho, tamanho)


def setup():
    py5.pixel_density(py5.display_density())
    py5.size(*helpers.DIMENSOES.external, py5.P3D)
    py5.color_mode(py5.HSB, 360, 100, 100)
    inicializa()
    acumula_pontos(pontos_por_frame)


def draw():
    py5.background(cor_fundo)
    acumula_pontos(pontos_por_frame)
    with py5.push():
        py5.translate(*helpers.DIMENSOES.pos_interno)
        if camada is not None:
            largura = helpers.DIMENSOES.internal[0] * py5.display_density()
            altura = helpers.DIMENSOES.internal[1] * py5.display_density()
            py5.image(camada, 0, 0, largura, altura)
    # Credits and go
    canvas.sketch_frame(
        sketch,
        cor_fundo,
        "large_transparent_white",
        "transparent_white",
        version=2,
    )


def key_pressed():
    key = py5.key
    if key == " ":
        save_and_close()


def save_and_close():
    py5.no_loop()
    canvas.save_sketch_image(sketch)
    py5.exit_sketch()


if __name__ == "__main__":
    py5.run_sketch()
