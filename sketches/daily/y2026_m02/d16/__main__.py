"""2026-02-16
Eye 06
Desenho que se assemelha a um olho alienígena
ericof.com|https://openprocessing.org/sketch/1307209
png
Sketch,py5,CreativeCoding
"""

from dataclasses import dataclass
from functools import cache
from sketches.utils.draw import canvas
from sketches.utils.helpers import sketches as helpers
from sketches.utils.helpers.timing import report_time
from typing import cast

import py5


sketch = helpers.info_for_sketch(__file__, __doc__)

cor_fundo = py5.color(0)

bolas: list["Bola"] = []

status = True

inner_radius_i = 50
inner_radius = 60
inner_radius_sa = 160
outer_radius = 600

num_balls = 12_000
inner_r = inner_radius
outer_r = 600


noise_amp = 40
noise_factor = 80
inner_noise_factor = 40

inner_alpha = 100
outer_alpha = 80

thick = 2
step = 0.8
point_step = 0.8

PG_DIMENSAO = 2000, 1000
PG_MEIO = 1000, 500

pg: py5.Py5Graphics | None = None

esfera_rot_x = 0
esfera_rot_y = 90
esfera_rot_z = 0

luz_x = 590
luz_y = 410
luz_z = -880


@dataclass
class Circulo:
    x: float
    y: float
    raio: float
    cor: int


@dataclass
class Iteracao:
    rotacao: float
    circulos: list[Circulo]


@cache
def lerp_color_rgba(c1: int, c2: int, t) -> int:
    t = py5.constrain(t, 0, 1)
    r = float(py5.lerp(py5.red(c1), py5.red(c2), t))
    g = float(py5.lerp(py5.green(c1), py5.green(c2), t))
    b = float(py5.lerp(py5.blue(c1), py5.blue(c2), t))
    a = float(py5.lerp(py5.alpha(c1), py5.alpha(c2), t))
    return py5.color(r, g, b, a)


class Bola:
    def __init__(self, px, py, vx, vy, ax, ay, r):
        self.px = px
        self.py = py
        self.vx = vx
        self.vy = vy
        self.ax = ax
        self.ay = ay
        self.r = r

    def update(self):
        # Integrate
        self.vx += self.ax
        self.vy += self.ay
        self.px += self.vx
        self.py += self.vy

        # Flow field-ish noise steering (same spirit as original)
        noise_fx = 35
        noise_fy = 35

        nx = py5.noise(self.px / noise_fx, self.py / noise_fy, 10)
        ny = py5.noise(self.px / noise_fx, self.py / noise_fy, 100)

        self.vx = py5.remap(nx, 0, 1, -1, 1) * 2.5
        self.vy = py5.remap(ny, 0, 1, -1, 1) * 2.5

    def draw(self) -> Circulo:
        dist_ = py5.sqrt(self.px * self.px + self.py * self.py)
        alpha = py5.remap(dist_, inner_radius, outer_radius, 100, 0)
        alpha = py5.constrain(alpha, 0, 255)
        cor = py5.color(20, 100, 255, int(alpha))
        return Circulo(self.px, self.py, self.r, cor)


def area_central(rotacao: float, idx: int, raio: int = 1) -> Iteracao:
    j = 0
    circulos = [Circulo(0, 0, 10, py5.color(20, 20, 20, 50))]
    while j < inner_radius_sa:
        alpha = float(py5.remap(j, 0, inner_radius_sa, inner_alpha, 20))
        cor = py5.color(0, 0, 0, alpha)
        y = float(py5.noise(j / noise_factor / 3, idx) * noise_amp)
        circulos.append(Circulo(j, y, raio, cor))
        j += point_step
    return Iteracao(rotacao=rotacao, circulos=circulos)


def anel_interno(rotacao: float, idx: int, raio: int = 1) -> Iteracao:
    seed = idx / inner_noise_factor / 10
    circulos = []
    inicio = float(
        inner_radius_i
        + py5.noise(py5.sin(seed), py5.cos(seed)) * 15
        + py5.random(-3, 3)
    )
    j = inicio
    while j < outer_radius:
        alpha = float(
            py5.remap(j, inner_radius_i, outer_radius, inner_alpha, outer_alpha)
        )
        mix = float(py5.remap(j, 0, (outer_radius - inner_radius), 0, 1))
        c3 = py5.color(247, 127, 0)
        c4 = py5.color(255, 255, 255)
        ci = lerp_color_rgba(c4, c3, mix)
        cor = py5.color(py5.red(ci), py5.green(ci), py5.blue(ci), alpha)
        y = float(py5.noise(j / noise_factor / 3, py5.frame_count) * noise_amp)
        circulos.append(Circulo(j, y, raio, cor))
        j += point_step
    return Iteracao(rotacao=rotacao, circulos=circulos)


def anel_central(rotacao: float, idx: int, point_index: int, raio: int = 1) -> Iteracao:
    circulos = []
    i = float(
        inner_radius
        + 10 * py5.sin(20 * idx)
        + py5.noise(idx / inner_noise_factor) * 50
        + py5.random(-5, 5)
    )
    while i < outer_radius:
        alpha = float(
            py5.remap(i, inner_radius, outer_radius, inner_alpha, outer_alpha)
        )
        mix = float(py5.remap(i, 0, (outer_radius - inner_radius), 0, 1))

        c1 = py5.color(0, 255, 167)
        c2 = py5.color(255, 255, 255)
        ci = lerp_color_rgba(c2, c1, mix)

        thick1 = (
            py5.noise(idx * 10) * thick
            + 20 * (py5.sin(10 * idx) + 1)
            + py5.random(-5, 5)
        )
        raio_ = 1.6 if point_index < thick1 else raio
        cor = py5.color(py5.red(ci), py5.green(ci), py5.blue(ci), alpha)
        y = float(py5.noise(i / noise_factor, idx) * noise_amp)
        circulos.append(Circulo(i, y, raio_, cor))

        point_index += 1
        i += point_step
    return Iteracao(rotacao=rotacao, circulos=circulos)


def anel_externo(rotacao: float, idx: int, point_index: int, raio: int = 1) -> Iteracao:
    circulos = []
    i = cast(
        float,
        (
            inner_radius_sa
            - 10 * py5.sin(2.5 * idx)
            - py5.noise(idx / inner_noise_factor / 1.1) * 40
            - py5.random(-3, 3)
        ),
    )
    while i < outer_radius:
        # Menor alpha próximo ao centro, maior quanto mais distante
        alpha = float(
            py5.remap(i, inner_radius, outer_radius, outer_alpha + 20, inner_alpha - 15)
        )
        mix = float(py5.remap(i, 0, (outer_radius - inner_radius), 0, 1))

        c5 = py5.color(255, 51, 51)
        c6 = py5.color(255, 17, 17)
        ci = lerp_color_rgba(c6, c5, mix)

        cor = py5.color(py5.red(ci), py5.green(ci), py5.blue(ci), alpha)
        circulos.append(Circulo(i, 0, raio, cor))

        point_index += 1
        i += point_step
    return Iteracao(rotacao=rotacao, circulos=circulos)


def calcula_desenho() -> dict[int, list[Iteracao]]:
    limite = 20
    d = 0.0
    e = 0.0
    g = 0.0
    point_index = 0

    full_turn = py5.TWO_PI
    iteracoes = {}

    idx = 0
    while g < full_turn:
        grupo = []
        if d < full_turn:
            grupo.append(area_central(d, idx, 6))
            grupo.append(anel_interno(d, idx, 1))

        if e < full_turn:
            grupo.append(anel_central(e, idx, point_index))

        if g < full_turn:
            percentual = (g / full_turn) * 100
            if percentual > limite:
                limite += 20
                print(f"{percentual:02f}")
            grupo.append(anel_externo(g, idx, point_index, 1))
            circulos = []
            for b in bolas:
                b.update()
                circulos.append(b.draw())
            grupo.append(Iteracao(0, circulos))

        iteracoes[idx] = grupo
        d += float(py5.radians(step * py5.random(0.5, 0.75)))
        e += float(py5.radians(step * py5.random(0.5, 0.75)))
        g += float(py5.radians(step * py5.random(0.3, 0.5)))
        idx += 1
        point_index = 0

    return iteracoes


def cria_imagem():
    pg = py5.create_graphics(*PG_DIMENSAO, py5.P3D)
    with pg.begin_draw():
        pg.background(py5.color(255, 255, 255))
        with pg.push():
            pg.translate(*PG_MEIO)
            for _, grupos in iteracoes.items():
                for iteracao in grupos:
                    with pg.push():
                        pg.rotate(iteracao.rotacao)
                        pg.no_stroke()
                        for circulo in iteracao.circulos:
                            pg.fill(circulo.cor)
                            pg.circle(circulo.x, circulo.y, circulo.raio)
    return pg


def cria_esfera(textura: py5.Py5Graphics) -> py5.Py5Shape:
    esfera = py5.create_shape(py5.SPHERE, outer_r / 2)
    esfera.set_texture(textura)
    esfera.set_texture_mode(py5.IMAGE)
    esfera.set_stroke(False)
    for meth, angulo in (
        (esfera.rotate_x, esfera_rot_x),
        (esfera.rotate_y, esfera_rot_y),
        (esfera.rotate_z, esfera_rot_z),
    ):
        rotacao = float(py5.radians(float(angulo)))
        meth(rotacao)
    return esfera


def setup():
    global pg, iteracoes
    py5.size(*helpers.DIMENSOES.external, py5.P3D)
    py5.image_mode(py5.CENTER)

    with report_time("Cria bolas"):
        for _ in range(num_balls):
            ang = py5.random(py5.TWO_PI)  # radians
            r = py5.random(inner_r, outer_r)
            x = py5.cos(ang) * r
            y = py5.sin(ang) * r

        bolas.append(Bola(x, y, x * 1.45, y * 1.45, x * 0.018, y * 0.018, 3.5))

    with report_time("Calcula desenho"):
        iteracoes = calcula_desenho()
    with report_time("Cria imagem"):
        pg = cria_imagem()


def draw():
    global pg, luz_x, luz_y
    centro = helpers.DIMENSOES.centro
    py5.background(cor_fundo)
    if pg:
        esfera = cria_esfera(pg)
        with py5.push():
            py5.translate(*centro, -outer_r / 3)
            py5.directional_light(200, 200, 200, luz_x, luz_y, luz_z)
            py5.shape(esfera)
    py5.window_title(f"{luz_x} - {luz_y} - {luz_z}")

    # Credits and go
    canvas.sketch_frame(
        sketch,
        cor_fundo,
        "large_transparent_white",
        "transparent_white",
        version=2,
    )
    if not status:
        save_and_close()


def mouse_pressed():
    global luz_x, luz_y
    button = py5.mouse_button
    match button:
        case py5.LEFT:
            luz_x, luz_y = py5.mouse_x, py5.mouse_y


def key_pressed():
    global luz_z, esfera_rot_x, esfera_rot_y, esfera_rot_z
    key = py5.key
    match key:
        case "a":
            esfera_rot_y -= 2
        case "d":
            esfera_rot_y += 2
        case "w":
            esfera_rot_x -= 2
        case "s":
            esfera_rot_x += 2
        case "z":
            esfera_rot_z -= 2
        case "x":
            esfera_rot_z += 2
        case "r":
            luz_z -= 10
        case "f":
            luz_z += 10
        case " ":
            save_and_close()


def save_and_close():
    py5.no_loop()
    canvas.save_sketch_image(sketch)
    py5.exit_sketch()


if __name__ == "__main__":
    py5.run_sketch()
