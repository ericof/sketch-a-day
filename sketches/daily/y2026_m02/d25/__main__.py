"""2026-02-25
Eyes Collective 05
Desenho que se assemelha a um coletivo de olhos alienígenas
ericof.com|https://openprocessing.org/sketch/1307209
png
Sketch,py5,CreativeCoding
"""

from dataclasses import dataclass
from functools import cache
from sketches.utils.draw import canvas
from sketches.utils.draw.formas import pontos_esfera
from sketches.utils.helpers import recursos
from sketches.utils.helpers import sketches as helpers
from sketches.utils.helpers.timing import report_time
from typing import cast

import numpy as np
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

perimetro = 1000
perimetro_pontos = 1000
esfera_raio = outer_r / 8.0

noise_amp = 40
noise_factor = 80
inner_noise_factor = 40

inner_alpha = 100
outer_alpha = 80

thick = 2
step = 0.8
point_step = 0.8

z_factor = 0.75

PG_DIMENSAO = 2000, 1000
PG_MEIO = 1000, 500


@dataclass
class EsferaInfo:
    esfera: py5.Py5Shape
    x: float
    y: float
    z: float
    rotacoes: list[float]
    controle: list[float]
    escala: float = 1.0
    vizinhos: list = None


esferas: list[EsferaInfo] = []

luz_x = 500
luz_y = 500
luz_z = -1200
brilho = 5
escala = 1.0
fator_escala = 1.00


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

        c5 = py5.color(51, 255, 51)
        c6 = py5.color(17, 255, 17)
        ci = lerp_color_rgba(c6, c5, mix)

        cor = py5.color(py5.red(ci), py5.green(ci), py5.blue(ci), alpha)
        circulos.append(Circulo(i, 0, raio, cor))

        point_index += 1
        i += point_step
    return Iteracao(rotacao=rotacao, circulos=circulos)


def vizinhos_knn_esfera(points: np.ndarray, idx: int, k: int = 6) -> np.ndarray:
    """
    points: (N, 3)
    idx: índice do ponto base
    k: número de vizinhos desejado
    retorna: índices dos k vizinhos mais próximos (por distância angular)
    """
    if points.ndim != 2 or points.shape[1] != 3:
        raise ValueError("points precisa ter shape (N, 3)")
    n = points.shape[0]
    if not (0 <= idx < n):
        raise IndexError("idx fora do range")
    if k <= 0:
        return np.array([], dtype=int)
    if n <= 1:
        return np.array([], dtype=int)

    # normaliza para raio 1 (remove efeito do raio na métrica angular)
    p = points / np.linalg.norm(points, axis=1, keepdims=True)

    # similaridade angular = cos(angulo) = dot(u, v); maior => mais perto
    sims = p @ p[idx]
    sims[idx] = -np.inf  # exclui o próprio ponto

    k = min(k, n - 1)
    # pega top-k por similaridade (sem ordenar tudo)
    nn = np.argpartition(-sims, kth=k - 1)[:k]
    # opcional: ordenar do mais próximo para o menos próximo
    nn = nn[np.argsort(-sims[nn])]
    return nn


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


def cria_imagem(iteracoes, filename: str) -> py5.Py5Graphics | py5.Py5Image:
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
    recursos.salva_imagem_cache(pg, filename)
    return pg


def cria_esfera(
    textura: py5.Py5Graphics | py5.Py5Image, raio: float, rotacoes: list[float]
) -> py5.Py5Shape:
    esfera = py5.create_shape(py5.SPHERE, raio)
    esfera.set_texture(textura)
    esfera.set_texture_mode(py5.IMAGE)
    esfera.set_stroke(False)
    esfera.rotate_x(py5.radians(rotacoes[0]))
    esfera.rotate_y(py5.radians(rotacoes[1]))
    esfera.rotate_z(py5.radians(rotacoes[2]))
    return esfera


def desenha_olho(info: EsferaInfo):
    esfera = info.esfera
    esfera.set_shininess(brilho)
    if escala != info.escala:
        info.escala *= fator_escala
        esfera.scale(fator_escala)
    x, y, z = info.x, info.y, info.z
    base = info.rotacoes
    controle = info.controle
    with py5.push():
        py5.translate(x, y, z)
        for idx, method in enumerate((
            py5.rotate_x,
            py5.rotate_y,
            py5.rotate_z,
        )):
            rot_base = base[idx]
            valor = controle[idx]
            rotacao = valor - rot_base
            if int(rotacao) != 0:
                method(float(py5.radians(rotacao)))
        py5.shape(esfera)


def desenha_nervo(info: EsferaInfo):
    x, y, z = info.x, info.y, info.z
    with py5.push():
        for nx, ny, nz in info.vizinhos:
            py5.stroke(255, 0, 0, 50)
            py5.stroke_weight(1)
            py5.line(x, y, z, nx, ny, nz)


def calcula_coordenadas(
    idx: int, xb: float, yb: float, zb: float
) -> tuple[float, float, float]:
    mult = z_factor if idx % 2 == 0 else 1.0
    return xb, yb, zb * mult


def setup():
    global esfera_central
    py5.size(*helpers.DIMENSOES.external, py5.P3D)
    py5.image_mode(py5.CENTER)
    filename = f"{sketch.day}_pg.png"

    esfera_central = py5.create_shape(py5.SPHERE, perimetro * z_factor * 0.75)
    esfera_central.set_stroke(False)
    esfera_central.set_fill("#222222")

    esfera_info = []
    rotacoes = [0.0, 90.0, 0.0]
    pontos = np.array(pontos_esfera(perimetro, perimetro_pontos))
    for idx, (xb, yb, zb) in enumerate(pontos):
        x, y, z = calcula_coordenadas(idx, xb, yb, zb)
        vizinhos = [
            tuple(calcula_coordenadas(i, *pontos[i]))
            for i in vizinhos_knn_esfera(pontos, idx, k=3)
        ]
        esfera_info.append((x, y, z, rotacoes[:], vizinhos))

    with report_time("Cria bolas"):
        for _ in range(num_balls):
            ang = py5.random(py5.TWO_PI)  # radians
            r = py5.random(inner_r, outer_r)
            x = py5.cos(ang) * r
            y = py5.sin(ang) * r
        bolas.append(Bola(x, y, x * 1.45, y * 1.45, x * 0.018, y * 0.018, 3.5))

    if not (pg := recursos.carrega_imagem_cache(filename)):
        with report_time("Calcula desenho"):
            iteracoes = calcula_desenho()
        with report_time("Cria imagem"):
            pg = cria_imagem(iteracoes, filename=filename)
    with report_time("Cria Esferas"):
        for x, y, z, rotacoes, vizinhos in esfera_info:
            base = rotacoes[:]
            esfera = cria_esfera(pg, esfera_raio, base)
            esferas.append(EsferaInfo(esfera, x, y, z, base, rotacoes, 1.0, vizinhos))


def draw():
    global luz_x, luz_y, fator_escala, escala
    centro = helpers.DIMENSOES.centro
    py5.background(cor_fundo)
    py5.directional_light(200, 200, 200, luz_x, luz_y, luz_z)
    escala *= fator_escala
    for info in esferas:
        with py5.push():
            py5.translate(*centro, -perimetro * 1.5)
            py5.shape(esfera_central)
            desenha_nervo(info)
            desenha_olho(info)
    # Reseta escala
    fator_escala = 1.0
    texto = (
        f"Frame: {py5.frame_count} - Luz: ({luz_x}, {luz_y}, {luz_z}) - "
        f"Brilho: {brilho} - Escala: {escala:.2f}"
    )
    py5.window_title(texto)

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
    global luz_z, brilho, fator_escala
    key = py5.key
    match key:
        case "r":
            luz_z -= 10
        case "f":
            luz_z += 10
        case "w":
            brilho += 1
        case "s":
            brilho -= 1
        case "a":
            fator_escala = 0.95
        case "d":
            fator_escala = 1.05
        case " ":
            save_and_close()


def save_and_close():
    py5.no_loop()
    canvas.save_sketch_image(sketch)
    py5.exit_sketch()


if __name__ == "__main__":
    py5.run_sketch()
