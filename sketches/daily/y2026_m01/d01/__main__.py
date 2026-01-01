"""2026-01-01
Waves 01
Celebração do ano novo com ondas fluídas e cores suaves.
ericof.com|https://openprocessing.org/sketch/2687965
png
Sketch,py5,CreativeCoding
"""

from sketches.utils.draw import canvas
from sketches.utils.helpers import sketches as helpers

import py5


sketch = helpers.info_for_sketch(__file__, __doc__)


cores_escuras = ["#03045e", "#023e8a", "#124559", "#0077b6", "#0096c7"]
cores_claras = ["#48cae4", "#90e0ef", "#ade8f4", "#caf0f8", "#EEEEFF"]
cores_fundo = ["#fdf0d5", "#fcf6bd", "#d0f4de", "#ffccd5"]
cor_fundo = py5.random_choice(cores_fundo)
cor_borda = py5.random_choice(cores_escuras)
sep = py5.random(0.5, 0.8)
num_layers = py5.random_choice([2, 3, 4])


def regenerate_scene():
    global cor_fundo, cor_borda, sep, num_layers
    cor_borda = py5.random_choice(cores_escuras)
    sep = py5.random(0.5, 0.8)
    num_layers = py5.random_choice([2, 3, 4])


def setup():
    py5.size(*helpers.DIMENSOES.external, py5.P3D)
    py5.background(cor_fundo)
    py5.frame_rate(30)
    regenerate_scene()


def draw():
    with py5.push():
        py5.translate(*helpers.DIMENSOES.pos_interno)
        py5.fill(cor_fundo)
        py5.no_stroke()
        py5.rect(0, 0, *helpers.DIMENSOES.internal)

        py5.curve_tightness(0.75)

        W = helpers.DIMENSOES.internal[0] + 100
        resolution = 1
        steps = 8000
        w_num = 0

        for k in range(int(num_layers)):
            offset_t = k * 0.15
            palette = cores_escuras if (k % 2 == 1) else cores_claras

            n = py5.noise(w_num * 0.5, k * 0.5)
            color_index = int(py5.floor(py5.remap(n, 0, 1, 0, len(palette))))
            color_index = max(0, min(color_index, len(palette) - 1))

            fill_color = py5.color(palette[color_index])
            py5.fill(fill_color, 50 + 20 * k)
            py5.stroke(palette[color_index])
            py5.stroke_weight(0.5 + 0.1 * k)

            with py5.begin_shape():
                previous_j = -1
                is_new_line = True

                step = 0
                while step <= steps:
                    T = step / W / 3
                    T = T / sep + offset_t

                    _j = step % W
                    j = W / 4 + _j

                    X = j
                    Y = 0.0
                    time_falloff = 1 - T / 5
                    wave_size = 5 / time_falloff

                    if _j < previous_j:
                        # Close previous wave
                        py5.vertex(
                            helpers.DIMENSOES.internal[0] + 200,
                            Y
                            + wave_size
                            + 5000 / j
                            - helpers.DIMENSOES.internal[1] / 4,
                        )
                        py5.vertex(py5.width + 200, py5.height + 200)
                        py5.vertex(-200, py5.height + 200)
                        py5.end_shape(py5.CLOSE)
                        py5.begin_shape()
                        is_new_line = True
                        w_num += 1

                    previous_j = _j

                    while wave_size < W / 5 / time_falloff:
                        A = (
                            (X / wave_size + T + py5.frame_count * 0.05) % 1
                        ) * wave_size - wave_size / 2
                        deform = 1 - ((A * A) / (wave_size * wave_size)) * 4
                        C = py5.cos(deform)
                        S = py5.sin(deform)

                        X += A * C + Y * S - A - 20
                        Y = Y * C - A * S

                        wave_size /= 0.6

                    final_y = Y + wave_size + 5000 / j - py5.height / 4

                    if is_new_line:
                        py5.vertex(-200, final_y)
                        py5.vertex(X - W / 7, final_y)
                        is_new_line = False
                    else:
                        # Original had curveVertex commented out, so we keep vertex()
                        py5.vertex(X - W / 7, final_y)

                    step += resolution

        # Draw border
        py5.no_fill()
        py5.stroke(cor_borda)
        py5.stroke_weight(10)
        py5.rect(0, 0, *helpers.DIMENSOES.internal)
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
