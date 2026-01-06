"""2026-01-06
Waves 06 (P2D)
Celebração do ano novo com ondas fluídas e cores suaves.
ericof.com|https://openprocessing.org/sketch/2687965
png
Sketch,py5,CreativeCoding
"""

from sketches.utils.draw import canvas
from sketches.utils.draw.cores.paletas import gera_paleta
from sketches.utils.helpers import sketches as helpers

import py5


sketch = helpers.info_for_sketch(__file__, __doc__)


cores_escuras = gera_paleta("azul-02")
cores_claras = gera_paleta("azul-01")
cores_fundo = gera_paleta("bege-01")
cor_fundo = py5.random_choice(cores_fundo)
cor_borda = "#FFFFFF"
curva = py5.random(0.5, 0.9)
sep = py5.random(0.6, 1.25)
camadas = py5.random_int(12, 20)
buffer = py5.random_int(200, 300)


def setup():
    py5.size(*helpers.DIMENSOES.external, py5.P3D)
    py5.background(cor_fundo)
    py5.frame_rate(30)


def desenha_fundo(largura, altura):
    with py5.push():
        py5.fill(cor_fundo)
        py5.no_stroke()
        py5.rect(0, 0, largura, altura)


def desenha_borda(largura, altura):
    with py5.push():
        # Draw border
        py5.no_fill()
        py5.stroke(cor_borda)
        py5.stroke_weight(10)
        py5.rect(0, 0, largura, altura)


def desenha_camada(largura, altura, direcao, k, w_num, W, passos, resolution):
    frame = py5.frame_count * direcao
    offset_t = k * 0.35
    palette = cores_escuras if (k % 2 == 1) else cores_claras

    n = py5.noise(w_num * 0.75, k * 0.75)
    color_index = int(py5.floor(py5.remap(n, 0, 1, 0, len(palette))))
    color_index = max(0, min(color_index, len(palette) - 1))

    fill_color = py5.color(palette[color_index])
    py5.fill(fill_color, 50 + 20 * k)
    py5.stroke(palette[color_index])
    py5.stroke_weight(0.5 + 0.1 * k)
    with py5.begin_shape():
        previous_j = -1
        is_new_line = True

        passo = 0
        while passo <= passos:
            T = passo / W / 3
            T = T / sep + offset_t

            _j = passo % W
            j = W / 4 + _j

            X = j
            Y = 0.0
            time_falloff = 1 - T / 5
            wave_size = 5 / time_falloff

            if _j < previous_j:
                # Close previous wave
                py5.vertex(
                    largura + buffer,
                    Y + wave_size + 5000 / j - altura / 4,
                )
                py5.vertex(largura + buffer, altura + buffer)
                py5.vertex(-buffer, altura + buffer)
                py5.end_shape(py5.CLOSE)
                py5.begin_shape()
                is_new_line = True
                w_num += 1

            previous_j = _j

            while wave_size < W / 5 / time_falloff:
                A = ((X / wave_size + T + frame * 0.05) % 1) * wave_size - wave_size / 2
                deform = (1 - ((A * A) / (wave_size * wave_size)) * 4) * direcao
                C = py5.cos(deform)
                S = py5.sin(deform)

                X += A * C + Y * S - A - 20
                Y = Y * C - A * S

                wave_size /= 0.6

            final_y = Y + wave_size + 5000 / j - altura / 4

            if is_new_line:
                py5.vertex(-buffer, final_y)
                py5.vertex(X - W / 7, final_y)
                is_new_line = False
            else:
                # Original had curveVertex commented out, so we keep vertex()
                py5.vertex(X - W / 7, final_y)

            passo += resolution


def draw():
    py5.window_title(
        f"Camadas: {camadas}, Sep: {sep:.2f}, Curve: {curva}, Buffer: {buffer}"
    )
    largura, altura = helpers.DIMENSOES.internal
    with py5.push():
        py5.translate(*helpers.DIMENSOES.pos_interno)
        desenha_fundo(largura, altura)

        py5.curve_tightness(curva)

        W = largura + 100
        resolution = 1
        passos = 1500
        direcao = -1
        w_num = 0
        for k in range(int(camadas)):
            desenha_camada(largura, altura, direcao, k, w_num, W, passos, resolution)

        desenha_borda(largura, altura)
    # Credits and go
    canvas.sketch_frame(
        sketch, py5.color(0), "large_transparent_white", "transparent_white"
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
