"""2026-03-02
Recursive Division 03
Desenho de subdivisões recursivas a partir de um quadrilátero
ericof.com|https://openprocessing.org/sketch/1307209
png
Sketch,py5,CreativeCoding
"""

from dataclasses import dataclass
from sketches.utils.draw import canvas
from sketches.utils.draw import vetores as vh
from sketches.utils.draw.cores.paletas import gera_paleta
from sketches.utils.helpers import sketches as helpers

import numpy as np
import py5


sketch = helpers.info_for_sketch(__file__, __doc__)


@dataclass
class Limites:
    """Limites do quadrilátero."""

    v1: np.ndarray
    v2: np.ndarray
    v3: np.ndarray
    v4: np.ndarray


cor_fundo_base = py5.color(0)
# Variáveis globais
limites: Limites | None = None
paleta = gera_paleta("Navy-Orange")
largura_canvas, altura_canvas = helpers.DIMENSOES.internal
lado_menor = min(largura_canvas, altura_canvas)
largura_fundo = lado_menor
largura_minima = largura_fundo * 0.95
meia_largura_minima = largura_minima / 2
raio2_minimo = meia_largura_minima * meia_largura_minima

cor_fundo = None


class CelulaRecursiva:
    """Objeto recursivo que subdivide quadrilátero e desenha contornos arredondados."""

    contador: int
    numero_divisoes_atual: int
    limite_divisoes: int
    divisoes: int
    razao_folga: float
    subobjetos: list["CelulaRecursiva"]
    amplitude_deslocamento: float
    cor: int
    limite: Limites
    direcao_divisao: str
    semente_ruido: float
    velocidade_ruido: float
    frequencia: float
    min_ruido: float
    max_ruido: float
    intervalo_ruido: float
    exibir_sub: list[bool]
    obj_id: str

    def __init__(
        self,
        numero_divisoes_atual: int,
        limite: Limites,
        obj_id: str,
        divisoes: int = 20,
        limite_divisoes: int = 15,
        razao_folga: float = 0.75,
        amplitude_divisor: float = 800,
    ):
        """Cria uma instância e possivelmente a subdivide em dois subobjetos."""
        self.obj_id = obj_id
        self.contador = 0
        self.numero_divisoes_atual = numero_divisoes_atual
        self.limite_divisoes = limite_divisoes
        self.razao_folga = razao_folga
        self.divisoes = divisoes
        self.subobjetos: list[CelulaRecursiva] = []

        self.amplitude_deslocamento = largura_minima / amplitude_divisor
        self.cor = py5.color(py5.random_choice(paleta))

        probabilidade_divisao = 1.0
        e_primeiro = self.numero_divisoes_atual == 1
        pode_dividir = self.numero_divisoes_atual < self.limite_divisoes
        sorteou = py5.random(1) < probabilidade_divisao

        self.limite = limite

        if (pode_dividir and sorteou) or e_primeiro:
            self.dividir_objeto()

    def dividir_objeto(self) -> None:
        """Define direção e parâmetros de ruído e cria dois subobjetos."""
        self.direcao_divisao = "vertical" if py5.random(1) < 0.5 else "horizontal"

        self.semente_ruido = float(py5.random(1000))
        self.velocidade_ruido = 0.0015
        self.frequencia = 6
        self.min_ruido = 0.2
        self.max_ruido = 0.8
        self.intervalo_ruido = self.max_ruido - self.min_ruido
        self.contador = 0

        proximo = self.numero_divisoes_atual + 1
        self.subobjetos = [
            CelulaRecursiva(proximo, limite=self.limite, obj_id=f"{self.obj_id}/0"),
            CelulaRecursiva(proximo, limite=self.limite, obj_id=f"{self.obj_id}/1"),
        ]

    def atualizar(
        self,
        limite: Limites,
    ) -> None:
        """Atualiza cantos e repassa para subobjetos (se existirem)."""
        self.limite = limite

        self.exibir_sub = [True, True]

        if self.subobjetos:
            passo = self.velocidade_ruido * self.contador
            ruido_base = py5.noise(self.semente_ruido + passo)
            ang = py5.TAU * self.frequencia * ruido_base
            seno = py5.sin(ang)
            metade_intervalo = self.intervalo_ruido / 2
            valor_ruido = float((seno + 1) * metade_intervalo + self.min_ruido)
            func = (
                self._atualizar_vertical
                if self.direcao_divisao == "vertical"
                else self._atualizar_horizontal
            )
            func(self.limite, valor_ruido)

        self.contador += 1

    def _atualizar_vertical(
        self,
        limite_base: Limites,
        valor_ruido: float,
    ) -> None:
        """Atualiza subdivisão vertical."""
        limite = Limites(
            limite_base.v1,
            vh.interpolar_vetor(limite_base.v1, limite_base.v2, valor_ruido),
            vh.interpolar_vetor(limite_base.v4, limite_base.v3, valor_ruido),
            limite_base.v4,
        )

        r1 = self.redimensionar_objeto_deslocamento_fixo(
            limite, self.amplitude_deslocamento
        )
        self.exibir_sub[0] = r1[1]
        if self.exibir_sub[0]:
            self.subobjetos[0].atualizar(limite)

        limite2 = Limites(
            limite.v2,
            limite_base.v2,
            limite_base.v3,
            limite.v3,
        )

        r2 = self.redimensionar_objeto_deslocamento_fixo(
            limite2, self.amplitude_deslocamento
        )
        self.exibir_sub[1] = r2[1]
        if self.exibir_sub[1]:
            self.subobjetos[1].atualizar(limite2)

    def _atualizar_horizontal(
        self,
        limite_base: Limites,
        valor_ruido: float,
    ) -> None:
        """Atualiza subdivisão horizontal."""
        limite = Limites(
            limite_base.v1,
            limite_base.v2,
            vh.interpolar_vetor(limite_base.v2, limite_base.v3, valor_ruido),
            vh.interpolar_vetor(limite_base.v1, limite_base.v4, valor_ruido),
        )

        r1 = self.redimensionar_objeto_deslocamento_fixo(
            limite, self.amplitude_deslocamento
        )
        self.exibir_sub[0] = r1[1]
        if self.exibir_sub[0]:
            self.subobjetos[0].atualizar(limite)

        limite2 = Limites(
            limite.v4,
            limite.v3,
            limite_base.v3,
            limite_base.v4,
        )

        r2 = self.redimensionar_objeto_deslocamento_fixo(
            limite2, self.amplitude_deslocamento
        )
        self.exibir_sub[1] = r2[1]
        if self.exibir_sub[1]:
            self.subobjetos[1].atualizar(limite2)

    def desenhar(self) -> None:
        """Desenha o objeto e recursivamente os subobjetos visíveis."""
        py5.fill(self.cor)
        print(f"- Desenhando {self.obj_id} e {self.numero_divisoes_atual}")
        if self.verificar_desenho():
            self.desenhar_linha_externa()

        if self.subobjetos:
            if self.exibir_sub[0]:
                self.subobjetos[0].desenhar()
            if self.exibir_sub[1]:
                self.subobjetos[1].desenhar()

    def verificar_desenho(self) -> bool:
        """True se os 4 cantos estiverem dentro do círculo (usa dist²)."""
        v1x, v1y = self.limite.v1
        v2x, v2y = self.limite.v2
        v3x, v3y = self.limite.v3
        v4x, v4y = self.limite.v4

        d1 = v1x * v1x + v1y * v1y
        d2 = v2x * v2x + v2y * v2y
        d3 = v3x * v3x + v3y * v3y
        d4 = v4x * v4x + v4y * v4y

        return (
            d1 < raio2_minimo
            and d2 < raio2_minimo
            and d3 < raio2_minimo
            and d4 < raio2_minimo
        )

    def redimensionar_objeto_deslocamento_fixo(
        self,
        limite_base: Limites,
        amplitude: float,
    ) -> tuple[Limites, bool]:
        """Desloca arestas e retorna [v1s, v2s, v3s, v4s, exibir]."""
        exibir = True

        v1: np.ndarray = limite_base.v1
        v2: np.ndarray = limite_base.v2
        v3: np.ndarray = limite_base.v3
        v4: np.ndarray = limite_base.v4

        n12 = vh.ajustar_magnitude(vh.normal_90(v2 - v1), amplitude)
        n23 = vh.ajustar_magnitude(vh.normal_90(v3 - v2), amplitude)
        n34 = vh.ajustar_magnitude(vh.normal_90(v4 - v3), amplitude)
        n41 = vh.ajustar_magnitude(vh.normal_90(v1 - v4), amplitude)

        v1_12 = v1 + n12
        v2_12 = v2 + n12

        v2_23 = v2 + n23
        v3_23 = v3 + n23

        v3_34 = v3 + n34
        v4_34 = v4 + n34

        v4_41 = v4 + n41
        v1_41 = v1 + n41

        limite = Limites(
            vh.calcular_cruzamento(v4_41, v1_41, v1_12, v2_12),
            vh.calcular_cruzamento(v1_12, v2_12, v2_23, v3_23),
            vh.calcular_cruzamento(v2_23, v3_23, v3_34, v4_34),
            vh.calcular_cruzamento(v3_34, v4_34, v4_41, v1_41),
        )

        if limite.v1[0] >= limite.v2[0] or limite.v1[1] >= limite.v4[1]:
            exibir = False
        return limite, exibir

    def desenhar_linha_externa(self) -> None:
        """Desenha o contorno externo arredondado."""
        v1, v2, v3, v4 = self.limite.v1, self.limite.v2, self.limite.v3, self.limite.v4
        parametros = (
            (v4, v1, v2),
            (v1, v2, v3),
            (v2, v3, v4),
            (v3, v4, v1),
        )
        z = py5.random_int(-20, 20)
        with py5.begin_shape():
            for v in parametros:
                pontos = self.calcular_canto_externo(*v)
                for x, y in pontos:
                    py5.vertex(float(x), float(y), z)

    def calcular_canto_externo(
        self,
        v1: np.ndarray,
        v2: np.ndarray,
        v3: np.ndarray,
    ) -> np.ndarray:
        """Gera pontos do arco externo no canto v2 (v1-v2-v3)."""
        deslocamento = self.amplitude_deslocamento * self.razao_folga

        centro21 = vh.ajustar_magnitude(vh.normal_90(v1 - v2), deslocamento)
        centro23 = vh.ajustar_magnitude(vh.normal_90(v2 - v3), deslocamento)

        # Ângulo entre vetores
        a = centro21
        b = centro23
        dot = float(a[0] * b[0] + a[1] * b[1])
        na = float(np.hypot(a[0], a[1]))
        nb = float(np.hypot(b[0], b[1]))
        cosang = dot / (na * nb)
        cosang = float(np.clip(cosang, -1.0, 1.0))
        ang_externo = float(np.arccos(cosang))

        divisoes = self.divisoes
        passo = ang_externo / divisoes

        # Rotações incrementais com matriz 2x2 (NumPy)
        c = float(np.cos(passo))
        s = float(np.sin(passo))
        rot = np.array([[c, -s], [s, c]], dtype=np.float64)

        pontos = np.empty((divisoes + 1, 2), dtype=np.float64)
        atual = centro21.copy()

        for i in range(divisoes + 1):
            pontos[i] = v2 + atual
            atual = rot @ atual

        return pontos


def criar_objeto_principal() -> CelulaRecursiva:
    """Cria o objeto principal."""
    global cor_fundo, limites

    limites = Limites(
        vh.criar_vetor(-meia_largura_minima, -meia_largura_minima),
        vh.criar_vetor(+meia_largura_minima, -meia_largura_minima),
        vh.criar_vetor(+meia_largura_minima, +meia_largura_minima),
        vh.criar_vetor(-meia_largura_minima, +meia_largura_minima),
    )

    paleta.append("#FFF4EC")
    cor_fundo = py5.color(py5.random_choice(paleta))
    objeto = CelulaRecursiva(numero_divisoes_atual=1, limite=limites, obj_id="0")
    objeto.atualizar(limites)
    return objeto


def setup():
    py5.size(*helpers.DIMENSOES.external, py5.P3D)
    py5.color_mode(py5.HSB, 360, 100, 100)
    py5.background(cor_fundo_base)
    principal = criar_objeto_principal()

    with py5.push():
        py5.translate(*helpers.DIMENSOES.centro)
        py5.stroke(cor_fundo_base)
        py5.stroke_weight(1)
        principal.desenhar()

    # Credits and go
    canvas.sketch_frame(
        sketch,
        cor_fundo_base,
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
