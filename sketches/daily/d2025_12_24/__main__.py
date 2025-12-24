"""2025-12-24
Hamlet (Mondrian)
Espiral com o texto de Hamlet.
ericof.com
png
Sketch,py5,CreativeCoding
"""

from sketches.utils.draw import canvas
from sketches.utils.draw.cores.paletas import gera_paleta
from sketches.utils.helpers import sketches as helpers
from sketches.utils.helpers import text as txt_helpers

import math
import py5


sketch = helpers.info_for_sketch(__file__, __doc__)

ESP_EXTRA = 0.1
MARGEM = 40
CENTRALIZAR_GLIFO = True
INNER_STEP_SCALE = 1.0
CLOSE_EPS = 2.0
TAMANHO_FONTE = 10
paleta = gera_paleta("mondrian")


def lado_atual(
    lado: int, left: float, top: float, right: float, bottom: float
) -> tuple[float, float, float]:
    if lado == 0:  # top: (left, top) -> (right, top)
        x0, y0 = left, top
        side_len = right - left
    elif lado == 1:  # right: (right, top) -> (right, bottom)
        x0, y0 = right, top
        side_len = bottom - top
    elif lado == 2:  # bottom: (right, bottom) -> (left, bottom)
        x0, y0 = right, bottom
        side_len = right - left
    else:  # left: (left, bottom) -> (left, top)
        x0, y0 = left, bottom
        side_len = bottom - top
    return x0, y0, side_len


def espiral_retangular(
    texto: str,
    limites: tuple[float, float, float, float],
    lista_fontes: list[str],
    tamanho: int = 16,
    esp_extra: float = 0.0,
):
    left, top, right, bottom = limites
    if not texto:
        return

    fontes = [py5.create_font(fonte, tamanho) for fonte in lista_fontes]
    # Precompute line height and inner step (how much we inset per loop).
    line_height = py5.text_ascent() + py5.text_descent()
    inner_step = max(1.0, line_height * INNER_STEP_SCALE)

    # Directions: 0:right, 1:down, 2:left, 3:up
    # Each entry: (dx, dy, angle)
    dirs = (
        (1.0, 0.0, 0.0),  # → along top
        (0.0, 1.0, math.pi / 2),  # ↓ along right
        (-1.0, 0.0, math.pi),  # ← along bottom
        (0.0, -1.0, -math.pi / 2),  # ↑ along left
    )

    i = 0  # index into text
    s = 0.0  # distance along current side
    side = 0  # 0..3 which side we are drawing

    while True:
        cor = py5.random_choice(paleta)
        py5.fill(cor)
        fonte = py5.random_choice(fontes)
        # Stop if rectangle collapsed
        if right - left <= CLOSE_EPS or bottom - top <= CLOSE_EPS:
            break

        x0, y0, side_len = lado_atual(side, left, top, right, bottom)
        dx, dy, ang = dirs[side]
        # Degenerate side—advance to next side (and possibly inset) then continue
        if side_len <= CLOSE_EPS:
            side += 1
            if side == 4:
                # completed a full loop; inset and restart at side 0
                side = 0
                left += inner_step
                top += inner_step
                right -= inner_step
                bottom -= inner_step
                s = 0.0
            continue

        # Current glyph and its advance
        ch = texto[i]
        py5.text_font(fonte)
        w = py5.text_width(ch)
        adv = w + esp_extra

        # Where we want the glyph: centered or left-aligned on s
        place_at = s + (0.5 * w if CENTRALIZAR_GLIFO else 0.0)

        # If this placement would exceed the current side, carry surplus to next side
        if place_at > side_len - CLOSE_EPS:
            surplus = place_at - side_len
            side += 1
            if side == 4:
                # full loop finished → inset and restart on top side
                side = 0
                left += inner_step
                top += inner_step
                right -= inner_step
                bottom -= inner_step
            s = max(0.0, surplus)  # carry leftover distance to the new side
            continue

        # Compute world position and draw the glyph
        px = x0 + dx * place_at
        py = y0 + dy * place_at
        with py5.push_matrix():
            py5.translate(px, py)
            py5.rotate(ang)
            py5.text_align(py5.CENTER if CENTRALIZAR_GLIFO else py5.LEFT, py5.CENTER)
            py5.text(ch, 0, 0)

        # Advance along side and move to next character
        s += adv
        i += 1
        if i >= len(texto):
            i = 0


def setup():
    py5.size(*helpers.DIMENSOES.external, py5.P3D)
    cor_fundo = py5.color(0)
    py5.background(0)
    py5.color_mode(py5.HSB, 360, 100, 100)
    py5.fill(py5.color(120, 80, 100))
    texto = txt_helpers.resource_text("hamlet.txt")
    limites = (MARGEM, MARGEM, py5.width - MARGEM, py5.height - MARGEM)
    fontes = [py5.random_choice(py5.Py5Font.list()) for _ in range(10)]
    espiral_retangular(
        texto,
        lista_fontes=fontes,
        limites=limites,
        tamanho=TAMANHO_FONTE,
        esp_extra=ESP_EXTRA,
    )
    # Credits and go
    canvas.sketch_frame(
        sketch, cor_fundo, "large_transparent_white", "transparent_white"
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
