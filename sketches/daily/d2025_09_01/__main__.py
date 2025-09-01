"""2025-09-01
Conexões em PI (02)
Circulo com conexões dos primeiros 1500 dígitos de PI.
ericof.com|https://web.archive.org/web/20120618223950/http://mkweb.bcgsc.ca/pi/art/
png
Sketch,py5,CreativeCoding
"""

from dataclasses import dataclass
from random import shuffle
from sketches.utils.draw import canvas
from sketches.utils.draw.canvas import draw_text_box
from sketches.utils.draw.cores.paletas import gera_paleta
from sketches.utils.helpers import sketches as helpers
from sketches.utils.helpers import text as txt_helpers

import numpy as np
import py5


sketch = helpers.info_for_sketch(__file__, __doc__)

RAIO = 300
TRACO_CIRCULO = 0
TRACO = 1.5
LIMITE = 1500
SEGMENTOS = 10
PALETA = None
LINKS = []
PASSO = 4


@dataclass
class Posicao:
    digito: int
    idx: int
    coordenadas: tuple[float, float] = (0, 0)


@dataclass
class Link:
    inicio: Posicao
    final: Posicao
    cor: int = 0


@dataclass
class Digito:
    id: int
    inicio: float
    final: float
    passo: float = 0
    cor: int = 0
    slots: int = 0


def inicializa_digitos(paleta: list[int]) -> dict[int, Digito]:
    digitos = {}
    passo = 360 / 10
    for idx in range(10):
        inicio = idx * passo
        final = inicio + passo
        cor = paleta[idx]
        digitos[idx] = Digito(id=idx, inicio=inicio, final=final, cor=cor, slots=0)
    return digitos


def _process_links_digitos(digitos: dict[int, Digito], pi: str, final: int = 1000):
    raw_links = []
    numeros = [int(d) for d in pi if d.isdigit()]
    inicio = 0
    final += inicio - 1
    for idx, digito in enumerate(numeros[inicio:final]):
        proximo = numeros[idx + 1]
        raw_links.append((int(digito), int(proximo)))

    all_links = []
    for raw_link in raw_links:
        inicio, final = raw_link
        idx_inicio = digitos[inicio].slots
        idx_final = digitos[final].slots
        link = Link(
            inicio=Posicao(digito=inicio, idx=idx_inicio),
            final=Posicao(digito=final, idx=idx_final),
            cor=digitos[inicio].cor,
        )
        all_links.append(link)
        digitos[inicio].slots += 1
    for digito in digitos.values():
        total = digito.slots
        digito.passo = 36 / (total + 1) if total > 0 else 0
    return all_links, digitos


def calcular_coordenadas(
    centro: tuple[float, float],
    raio: float,
    angulo_inicial: float,
    idx: int,
    passo: float,
) -> tuple[float, float]:
    angulo = py5.radians(angulo_inicial + (idx + 1) * passo)
    x = centro[0] + py5.cos(angulo) * raio
    y = centro[1] + py5.sin(angulo) * raio
    return (x, y)


def desenha_circunferencia(
    cx: float,
    cy: float,
    raio: float,
    traco: int,
    segmentos: int,
    paleta: list[py5.Py5Color],
):
    """Desenha uma circunferência completa usando n segmentos de arco consecutivos."""
    diametro = raio * 2
    with py5.push():
        py5.no_fill()
        py5.stroke_weight(traco)
        py5.stroke_cap(py5.SQUARE)

        arc_span = py5.TWO_PI / segmentos
        for i in range(segmentos):
            cor = paleta[i]
            py5.stroke(cor)
            start_angle = i * arc_span
            end_angle = start_angle + arc_span
            py5.arc(cx, cy, diametro, diametro, start_angle, end_angle)


def desenha_borda(
    cx: float, cy: float, raio: float, traco: int, borda_traco: int, borda_cor: str
):
    borda_raio = (raio * 2) - (traco / 2)
    py5.stroke(py5.color(borda_cor))
    py5.stroke_weight(borda_traco)
    py5.no_fill()
    py5.circle(cx, cy, borda_raio)


def desenha_legenda(cx: float, cy: float, raio: float, traco: int):
    inicial = -90
    for idx in range(10):
        diametro_legenda = raio + (2.2 * 20)
        angulo = (36 * idx) + 18 + inicial
        bx, by = calcular_coordenadas((cx, cy), diametro_legenda, angulo, 0, 0)
        draw_text_box(str(idx), "numero", bx, by, font_size=32)


def atualiza_coordenadas(
    centro: tuple[float, float],
    raio: float,
    digitos: dict[int, Digito],
    links: list[Link],
) -> list[Link]:
    for link in links:
        digito_inicio = digitos[link.inicio.digito]
        link.inicio.coordenadas = calcular_coordenadas(
            centro, raio, digito_inicio.inicio, link.inicio.idx, digito_inicio.passo
        )
        digito_final = digitos[link.final.digito]
        link.final.coordenadas = calcular_coordenadas(
            centro, raio, digito_final.inicio, link.final.idx, digito_final.passo
        )
    return links


def desenha_link(
    centro: tuple[float, float],
    raio: float,
    inicio: tuple[float, float],
    final: tuple[float, float],
    cor: int,
    traco: float = TRACO,
    margem: float = 20,
):
    """
    Desenha uma curva suave entre dois pontos na circunferência.
    - Tem formato de parábola
    - Sempre fica dentro do círculo
    - Nunca se aproxima a menos de `margem` do centro
    - Quanto mais próximos os pontos, mais rasa a curva
    """

    cx, cy = centro
    x1, y1 = inicio
    x2, y2 = final

    # Distância entre os pontos
    dist_entre_pontos = np.hypot(x2 - x1, y2 - y1)
    if dist_entre_pontos == 0:
        return

    # Ângulos de cada ponto em relação ao centro
    a1 = np.arctan2(y1 - cy, x1 - cx)
    a2 = np.arctan2(y2 - cy, x2 - cx)

    # Ângulo médio ao longo do arco (não da linha reta!)
    da = (a2 - a1 + 2 * np.pi) % (2 * np.pi)
    sentido = 1 if da < np.pi else -1
    a_meio = a1 + sentido * da / 2

    # Controla a curvatura com base na distância dos pontos
    curvatura_maxima = raio * 0.6
    curvatura = min(curvatura_maxima, dist_entre_pontos * 0.6)

    # Calcula ponto de controle ao longo do ângulo médio
    ctrl_x = cx + (raio - curvatura) * np.cos(a_meio)
    ctrl_y = cy + (raio - curvatura) * np.sin(a_meio)

    # Garante que o ponto de controle não invade a margem
    dist_ctrl_to_center = np.hypot(ctrl_x - cx, ctrl_y - cy)
    if dist_ctrl_to_center < margem:
        # reposiciona o ponto na borda da margem
        escala = (margem + 1) / dist_ctrl_to_center
        ctrl_x = cx + (ctrl_x - cx) * escala
        ctrl_y = cy + (ctrl_y - cy) * escala

    # Desenha a curva como Bézier quadrático manualmente
    py5.no_fill()
    py5.stroke(cor)
    py5.stroke_weight(traco)
    with py5.begin_shape():
        steps = 80
        for i in range(steps + 1):
            t = i / steps
            xt = (1 - t) ** 2 * x1 + 2 * (1 - t) * t * ctrl_x + t**2 * x2
            yt = (1 - t) ** 2 * y1 + 2 * (1 - t) * t * ctrl_y + t**2 * y2
            py5.vertex(xt, yt)


def paleta():
    paleta = gera_paleta("mandarin-redux")
    shuffle(paleta)
    return paleta


def setup():
    global PALETA, LINKS
    py5.size(*helpers.DIMENSOES.external, py5.P3D)
    py5.background(0)
    py5.color_mode(py5.HSB, 360, 100, 100)
    pi = txt_helpers.resource_text("pi.txt")
    PALETA = paleta()
    digitos = inicializa_digitos(PALETA)
    links, digitos = _process_links_digitos(digitos, pi, LIMITE)
    LINKS = atualiza_coordenadas((0, 0), RAIO, digitos, links)


def desenha(limite: int | None = None):
    cor_fundo = py5.color(0)
    centro = helpers.DIMENSOES.centro
    links = LINKS if limite is None else LINKS[:limite]
    with py5.push():
        py5.translate(*centro, 0)
        py5.rotate(py5.radians(-90))
        for link in links:
            with py5.push():
                desenha_link(
                    (0, 0),
                    RAIO,
                    link.inicio.coordenadas,
                    link.final.coordenadas,
                    link.cor,
                    1,
                    45,
                )
        desenha_circunferencia(0, 0, RAIO, TRACO_CIRCULO, SEGMENTOS, PALETA)
        desenha_borda(0, 0, RAIO, TRACO_CIRCULO, 6, "#000")

    desenha_legenda(*centro, RAIO, TRACO_CIRCULO)
    draw_text_box("π", "numero", *centro, font="Georgia-BoldItalic", font_size=56)
    # Credits and go
    canvas.sketch_frame(
        sketch, cor_fundo, "large_transparent_white", "transparent_white"
    )


def draw():
    limite = py5.frame_count * PASSO
    py5.window_title(f"Sketch - Frame {limite}")
    desenha(limite)


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
