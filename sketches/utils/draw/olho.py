from dataclasses import dataclass
from sketches.utils.draw.cores import extrai_rgb
from sketches.utils.draw.cores import lerp_color_rgba
from sketches.utils.helpers.timing import report_time
from typing import cast
from typing import TypedDict

import py5


class Cores(TypedDict):
    particulas: int
    area_central_01: int
    area_central_02: int
    anel_interno_01: int
    anel_interno_02: int
    anel_central_01: int
    anel_central_02: int
    anel_externo_01: int
    anel_externo_02: int
    fundo_imagem: int


CORES_PADRAO: Cores = {
    "particulas": py5.color(20, 100, 255),
    "area_central_01": py5.color(20, 20, 20, 50),
    "area_central_02": py5.color(0, 0, 0),
    "anel_interno_01": py5.color(247, 127, 0),
    "anel_interno_02": py5.color(255, 255, 255),
    "anel_central_01": py5.color(0, 255, 167),
    "anel_central_02": py5.color(255, 255, 255),
    "anel_externo_01": py5.color(51, 255, 51),
    "anel_externo_02": py5.color(17, 255, 17),
    "fundo_imagem": py5.color(255, 255, 255),
}


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


class Particulas:
    inner_radius: float = 60
    outer_radius: float = 600

    def __init__(
        self, px, py, vx, vy, ax, ay, r, inner_radius, outer_radius, cor_base: int
    ):
        self.px = px
        self.py = py
        self.vx = vx
        self.vy = vy
        self.ax = ax
        self.ay = ay
        self.r = r
        self.inner_radius = inner_radius
        self.outer_radius = outer_radius
        self.cor_base = cor_base

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
        alpha = py5.remap(dist_, self.inner_radius, self.outer_radius, 100, 0)
        alpha = py5.constrain(alpha, 0, 255)
        cor = py5.color(*extrai_rgb(self.cor_base), int(alpha))
        return Circulo(self.px, self.py, self.r, cor)


class Olho:
    cores: Cores
    dimensoes: tuple[int, int]
    particulas: list[Particulas]
    inner_alpha: float
    inner_noise_factor: int
    inner_radius_i: float
    inner_radius_sa: float
    inner_radius: float
    noise_amp: int
    noise_factor: int
    outer_alpha: float
    outer_radius: float
    point_step: float
    step: float
    thick: float

    def __init__(
        self,
        dimensoes: tuple[int, int] = (2000, 1000),
        inner_alpha: float = 100,
        inner_noise_factor: int = 40,
        inner_radius_i: float = 50,
        inner_radius_sa: float = 160,
        inner_radius: float = 60,
        noise_amp: int = 40,
        noise_factor: int = 80,
        outer_alpha: float = 80,
        outer_radius: float = 600,
        point_step: float = 0.8,
        step: float = 0.8,
        thick: float = 2,
        part_numero: int = 6000,
        part_inner_r: float = 60,
        part_outer_r: float = 600,
        cores: Cores | None = None,
    ):
        self.cores = cores if cores else CORES_PADRAO
        self.dimensoes = dimensoes
        self.inner_alpha = inner_alpha
        self.inner_noise_factor = inner_noise_factor
        self.inner_radius_i = inner_radius_i
        self.inner_radius_sa = inner_radius_sa
        self.inner_radius = inner_radius
        self.noise_amp = noise_amp
        self.noise_factor = noise_factor
        self.outer_alpha = outer_alpha
        self.outer_radius = outer_radius
        self.point_step = point_step
        self.step = step
        self.thick = thick
        particulas = []
        for _ in range(part_numero):
            ang = py5.random(py5.TWO_PI)
            r = py5.random(part_inner_r, part_outer_r)
            x = py5.cos(ang) * r
            y = py5.sin(ang) * r
            particulas.append(
                Particulas(
                    x,
                    y,
                    x * 1.45,
                    y * 1.45,
                    x * 0.018,
                    y * 0.018,
                    3.5,
                    inner_radius,
                    outer_radius,
                    cor_base=self.cores["particulas"],
                )
            )
        self.particulas = particulas

    def area_central(self, rotacao: float, idx: int, raio: int = 1) -> Iteracao:
        j = 0
        cor_1 = self.cores["area_central_01"]
        cor_2 = self.cores["area_central_02"]
        circulos = [Circulo(0, 0, 10, cor_1)]
        while j < self.inner_radius_sa:
            alpha = float(py5.remap(j, 0, self.inner_radius_sa, self.inner_alpha, 20))
            cor = py5.color(*extrai_rgb(cor_2), alpha)
            y = float(py5.noise(j / self.noise_factor / 3, idx) * self.noise_amp)
            circulos.append(Circulo(j, y, raio, cor))
            j += self.point_step
        return Iteracao(rotacao=rotacao, circulos=circulos)

    def anel_interno(self, rotacao: float, idx: int, raio: int = 1) -> Iteracao:
        cor_1 = self.cores["anel_interno_01"]
        cor_2 = self.cores["anel_interno_02"]
        seed = idx / self.inner_noise_factor / 10
        circulos = []
        inicio = float(
            self.inner_radius_i
            + py5.noise(py5.sin(seed), py5.cos(seed)) * 15
            + py5.random(-3, 3)
        )
        j = inicio
        while j < self.outer_radius:
            alpha = float(
                py5.remap(
                    j,
                    self.inner_radius_i,
                    self.outer_radius,
                    self.inner_alpha,
                    self.outer_alpha,
                )
            )
            mix = float(py5.remap(j, 0, (self.outer_radius - self.inner_radius), 0, 1))
            rgb = extrai_rgb(lerp_color_rgba(cor_2, cor_1, mix))
            cor = py5.color(*rgb, alpha)
            y = float(
                py5.noise(j / self.noise_factor / 3, py5.frame_count) * self.noise_amp
            )
            circulos.append(Circulo(j, y, raio, cor))
            j += self.point_step
        return Iteracao(rotacao=rotacao, circulos=circulos)

    def anel_central(
        self, rotacao: float, idx: int, point_index: int, raio: int = 1
    ) -> Iteracao:
        cor_1 = self.cores["anel_central_01"]
        cor_2 = self.cores["anel_central_02"]
        circulos = []
        i = float(
            self.inner_radius
            + 10 * py5.sin(20 * idx)
            + py5.noise(idx / self.inner_noise_factor) * 50
            + py5.random(-5, 5)
        )
        while i < self.outer_radius:
            alpha = float(
                py5.remap(
                    i,
                    self.inner_radius,
                    self.outer_radius,
                    self.inner_alpha,
                    self.outer_alpha,
                )
            )
            mix = float(py5.remap(i, 0, (self.outer_radius - self.inner_radius), 0, 1))

            rgb = extrai_rgb(lerp_color_rgba(cor_2, cor_1, mix))

            thick1 = (
                py5.noise(idx * 10) * self.thick
                + 20 * (py5.sin(10 * idx) + 1)
                + py5.random(-5, 5)
            )
            raio_ = 1.6 if point_index < thick1 else raio
            cor = py5.color(*rgb, alpha)
            y = float(py5.noise(i / self.noise_factor, idx) * self.noise_amp)
            circulos.append(Circulo(i, y, raio_, cor))

            point_index += 1
            i += self.point_step
        return Iteracao(rotacao=rotacao, circulos=circulos)

    def anel_externo(
        self, rotacao: float, idx: int, point_index: int, raio: int = 1
    ) -> Iteracao:
        circulos = []
        cor_1 = self.cores["anel_externo_01"]
        cor_2 = self.cores["anel_externo_02"]
        i = cast(
            float,
            (
                self.inner_radius_sa
                - 10 * py5.sin(2.5 * idx)
                - py5.noise(idx / self.inner_noise_factor / 1.1) * 40
                - py5.random(-3, 3)
            ),
        )
        while i < self.outer_radius:
            # Menor alpha próximo ao centro, maior quanto mais distante
            alpha = float(
                py5.remap(
                    i,
                    self.inner_radius,
                    self.outer_radius,
                    self.outer_alpha + 20,
                    self.inner_alpha - 15,
                )
            )
            mix = float(py5.remap(i, 0, (self.outer_radius - self.inner_radius), 0, 1))
            rgb = extrai_rgb(lerp_color_rgba(cor_2, cor_1, mix))
            cor = py5.color(*rgb, alpha)
            circulos.append(Circulo(i, 0, raio, cor))

            point_index += 1
            i += self.point_step
        return Iteracao(rotacao=rotacao, circulos=circulos)

    def calcula_desenho(self) -> dict[int, list[Iteracao]]:
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
                grupo.append(self.area_central(d, idx, 6))
                grupo.append(self.anel_interno(d, idx, 1))

            if e < full_turn:
                grupo.append(self.anel_central(e, idx, point_index))

            if g < full_turn:
                percentual = (g / full_turn) * 100
                if percentual > limite:
                    limite += 20
                    print(f"{percentual:02f}")
                grupo.append(self.anel_externo(g, idx, point_index, 1))
                circulos = []
                for b in self.particulas:
                    b.update()
                    circulos.append(b.draw())
                grupo.append(Iteracao(0, circulos))

            iteracoes[idx] = grupo
            d += float(py5.radians(self.step * py5.random(0.5, 0.75)))
            e += float(py5.radians(self.step * py5.random(0.5, 0.75)))
            g += float(py5.radians(self.step * py5.random(0.3, 0.5)))
            idx += 1
            point_index = 0

        return iteracoes

    def cria_image(self, iteracoes: dict[int, list[Iteracao]]) -> py5.Py5Graphics:
        meio = self.dimensoes[0] // 2, self.dimensoes[1] // 2
        pg = py5.create_graphics(*self.dimensoes, py5.P3D)
        with pg.begin_draw():
            pg.background(self.cores["fundo_imagem"])
            with pg.push():
                pg.translate(*meio)
                for _, grupos in iteracoes.items():
                    for iteracao in grupos:
                        with pg.push():
                            pg.rotate(iteracao.rotacao)
                            pg.no_stroke()
                            for circulo in iteracao.circulos:
                                pg.fill(circulo.cor)
                                pg.circle(circulo.x, circulo.y, circulo.raio)
        return pg

    def __call__(self) -> py5.Py5Graphics:
        """Iteracoes."""
        with report_time("Calcula desenho"):
            iteracoes = self.calcula_desenho()
        with report_time("Gera imagem"):
            pg = self.cria_image(iteracoes)
        return pg


if __name__ == "__main__":
    from sketches.utils.helpers import recursos
    from sketches.utils.helpers import window

    dimensoes = (500, 250)

    def setup():
        py5.size(*dimensoes, py5.P3D)
        py5.background(0)
        py5.image_mode(py5.CENTER)
        cores = CORES_PADRAO.copy()
        cores["fundo_imagem"] = py5.color(255, 255, 255, 40)
        pg = recursos.carrega_imagem_cache("__olho.png")
        if pg is None:
            with window.title("Calculando olho..."):
                olho = Olho(
                    noise_amp=95,
                    dimensoes=dimensoes,
                )
            with window.title("Gerando olho..."):
                pg = olho()
            recursos.salva_imagem_cache(pg, "__olho.png")
        with window.title("Exibindo olho..."), py5.push():
            py5.translate(dimensoes[0] // 2, dimensoes[1] // 2)
            py5.image(pg, 0, 0)

    py5.run_sketch()
