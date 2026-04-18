"""Geometria e renderização de uma bola de basquete 3D.

Uso típico::

    from sketches.utils.draw.basquete import calcula_bola_basquete, desenha_bola_basquete

    # No setup() — cálculo pesado, feito uma vez:
    dados_bola = calcula_bola_basquete(raio=200, resolucao=40)

    # No draw() — apenas renderiza:
    desenha_bola_basquete(dados_bola)
"""  # noqa: E501

from dataclasses import dataclass

import numpy as np
import py5


@dataclass
class PatchEsfera:
    """Malha curva para mapear textura sobre a superfície da esfera.

    :param vertices: Array (linhas, colunas, 3) com posições 3D na esfera.
    :param normais: Array (linhas, colunas, 3) com normais unitárias.
    :param linhas: Número de subdivisões em latitude.
    :param colunas: Número de subdivisões em longitude.
    :param rotacao_uv: Rotação da textura — ``False`` = normal, ``True`` = 90°.
    """

    vertices: np.ndarray
    normais: np.ndarray
    linhas: int
    colunas: int
    rotacao_uv: bool = False


@dataclass
class BolaSpec:
    raio: float = 200
    resolucao: int = 40
    texto_theta: float = 1.15
    texto_phi: float = 0.4
    texto_extensao: tuple[float, float] = (0.25, 0.2)
    texto_rotacao_uv: bool = False
    texto_dim: tuple[int, int] = (100, 100)
    texto_fonte: int = 40
    texto: str = ""


@dataclass
class DadosBola:
    """Geometria pré-calculada de uma bola de basquete.

    :param raio: Raio da esfera.
    :param faixas: Lista de faixas (latitude bands) — cada faixa é um array (N, 3).
    :param costuras: Lista de curvas 3D para as costuras — cada costura é um array (M, 3).
    :param patch_texto: Malha curva opcional para texto texturizado.
    """  # noqa: E501

    raio: float
    faixas: list[np.ndarray]
    costuras: list[np.ndarray]
    patch_texto: PatchEsfera | None = None


def _gera_faixas_esfera(
    raio: float,
    resolucao: int,
) -> list[np.ndarray]:
    """Gera faixas de latitude como pares de vértices para QUAD_STRIP.

    Cada faixa contém vértices alternados entre duas latitudes consecutivas,
    prontos para serem renderizados com ``begin_shape(QUAD_STRIP)``.

    :param raio: Raio da esfera.
    :param resolucao: Número de subdivisões em latitude e longitude.
    :returns: Lista de arrays com shape ``(2*(resolucao+1), 3)``.
    """
    faixas = []
    for i in range(resolucao):
        theta0 = np.pi * i / resolucao
        theta1 = np.pi * (i + 1) / resolucao
        vertices = []
        for j in range(resolucao + 1):
            phi = 2 * np.pi * j / resolucao
            for theta in (theta0, theta1):
                x = raio * np.sin(theta) * np.cos(phi)
                y = raio * np.cos(theta)
                z = raio * np.sin(theta) * np.sin(phi)
                vertices.append([x, y, z])
        faixas.append(np.array(vertices))
    return faixas


def _grande_circulo(
    raio: float,
    eixo: str,
    num_pontos: int = 200,
) -> np.ndarray:
    """Gera pontos ao longo de um grande círculo (equador ou meridiano).

    :param raio: Raio da curva.
    :param eixo: ``"equador"`` (plano XZ) ou ``"meridiano"`` (plano XY).
    :param num_pontos: Número de pontos na curva.
    :returns: Array com shape ``(num_pontos, 3)``.
    """
    t = np.linspace(0, 2 * np.pi, num_pontos)
    if eixo == "equador":
        return np.column_stack([
            raio * np.cos(t),
            np.zeros(num_pontos),
            raio * np.sin(t),
        ])
    return np.column_stack([raio * np.cos(t), raio * np.sin(t), np.zeros(num_pontos)])


def _elipse_lateral(
    raio: float,
    extensao_polar: float = 0.65,
    largura: float = 1.25,
    offset_phi: float = 0.0,
    num_pontos: int = 200,
) -> np.ndarray:
    """Gera uma elipse sobre a superfície da esfera, em um dos hemisférios.

    A elipse cruza o meridiano (costura polar) em dois pontos, espaçados
    ao máximo ao longo do eixo polar.

    :param raio: Raio da esfera.
    :param extensao_polar: Semi-eixo polar em radianos (~1.25 ≈ 72°).
        Controla quão perto dos polos os cruzamentos chegam.
    :param largura: Semi-eixo em longitude em radianos (~0.85 ≈ 49°).
        Controla a "barriga" lateral da elipse.
    :param offset_phi: ``0`` para o hemisfério frontal, ``π`` para o traseiro.
    :param num_pontos: Número de pontos na curva.
    :returns: Array com shape ``(num_pontos, 3)``.
    """
    t = np.linspace(0, 2 * np.pi, num_pontos)
    # theta oscila de polo a polo; phi fica confinado a um hemisfério
    theta = np.pi / 2 + extensao_polar * np.sin(t)
    phi = offset_phi + largura * np.cos(t)

    x = raio * np.sin(theta) * np.cos(phi)
    y = raio * np.cos(theta)
    z = raio * np.sin(theta) * np.sin(phi)
    return np.column_stack([x, y, z])


def _gera_patch_esfera(
    raio: float,
    theta_centro: float,
    phi_centro: float,
    theta_extensao: float,
    phi_extensao: float,
    subdivisoes: int = 12,
) -> PatchEsfera:
    """Gera uma malha curva retangular sobre a esfera para mapear textura.

    :param raio: Raio da esfera (ligeiramente acima da superfície).
    :param theta_centro: Centro do patch em ângulo polar.
    :param phi_centro: Centro do patch em ângulo azimutal.
    :param theta_extensao: Semi-extensão em theta (radianos).
    :param phi_extensao: Semi-extensão em phi (radianos).
    :param subdivisoes: Subdivisões em cada direção.
    :returns: :class:`PatchEsfera` com vértices e normais.
    """
    linhas = subdivisoes + 1
    colunas = subdivisoes + 1
    thetas = np.linspace(
        theta_centro - theta_extensao,
        theta_centro + theta_extensao,
        linhas,
    )
    phis = np.linspace(
        phi_centro - phi_extensao,
        phi_centro + phi_extensao,
        colunas,
    )
    theta_grid, phi_grid = np.meshgrid(thetas, phis, indexing="ij")

    x = raio * np.sin(theta_grid) * np.cos(phi_grid)
    y = raio * np.cos(theta_grid)
    z = raio * np.sin(theta_grid) * np.sin(phi_grid)

    vertices = np.stack([x, y, z], axis=-1)
    normais = vertices / raio

    return PatchEsfera(
        vertices=vertices,
        normais=normais,
        linhas=subdivisoes,
        colunas=subdivisoes,
    )


def calcula_bola_basquete(spec: BolaSpec) -> DadosBola:
    """Pré-calcula toda a geometria da bola de basquete.

    :param raio: Raio da esfera.
    :param resolucao: Subdivisões para a malha da esfera.
    :param texto_theta: Ângulo polar do centro do texto.
    :param texto_phi: Ângulo azimutal do centro do texto.
    :param texto_extensao: Semi-extensão ``(theta, phi)`` do patch de texto.
    :param texto_rotacao_uv: Se ``True``, rotaciona a textura em 90°.
    :returns: :class:`DadosBola` com faixas, costuras e patch de texto.
    """
    faixas = _gera_faixas_esfera(spec.raio, spec.resolucao)

    r_costura = spec.raio * 1.005  # ligeiramente acima da superfície
    costuras = [
        _grande_circulo(r_costura, "equador"),
        _grande_circulo(r_costura, "meridiano"),
        _elipse_lateral(r_costura, offset_phi=np.pi / 2),
        _elipse_lateral(r_costura, offset_phi=-np.pi / 2),
    ]

    patch = _gera_patch_esfera(
        spec.raio * 1.008,
        spec.texto_theta,
        spec.texto_phi,
        spec.texto_extensao[0],
        spec.texto_extensao[1],
    )
    patch.rotacao_uv = spec.texto_rotacao_uv

    return DadosBola(
        raio=spec.raio,
        faixas=faixas,
        costuras=costuras,
        patch_texto=patch,
    )


def _desenha_patch_textura(
    patch: PatchEsfera,
    textura: "py5.Py5Graphics",
) -> None:
    """Renderiza um patch curvo com textura mapeada via QUAD_STRIP.

    :param patch: Malha pré-calculada sobre a esfera.
    :param textura: Py5Graphics com o conteúdo a mapear.
    """
    py5.no_stroke()
    py5.texture_mode(py5.NORMAL)
    py5.blend_mode(py5.BLEND)
    py5.hint(py5.ENABLE_DEPTH_SORT)
    for i in range(patch.linhas):
        py5.begin_shape(py5.QUAD_STRIP)
        py5.texture(textura)
        py5.tint(255, 255)
        for j in range(patch.colunas + 1):
            for di in (0, 1):
                if patch.rotacao_uv:
                    u = 1.0 - (i + di) / patch.linhas
                    v = j / patch.colunas
                else:
                    u = j / patch.colunas
                    v = (i + di) / patch.linhas
                vt = patch.vertices[i + di, j]
                n = patch.normais[i + di, j]
                py5.normal(n[0], n[1], n[2])
                py5.vertex(vt[0], vt[1], vt[2], u, v)
        py5.end_shape()
    py5.hint(py5.DISABLE_DEPTH_SORT)
    py5.no_tint()


def desenha_bola_basquete(
    dados: DadosBola,
    cor_bola: int | None = None,
    cor_costura: int | None = None,
    espessura_costura: float = 2.5,
    textura_texto: "py5.Py5Graphics | None" = None,
) -> None:
    """Renderiza a bola de basquete usando dados pré-calculados.

    Deve ser chamada dentro de um bloco ``with py5.push()`` com translação
    e rotação já aplicadas.

    :param dados: Geometria pré-calculada via :func:`calcula_bola_basquete`.
    :param cor_bola: Cor da superfície (padrão: laranja basquete).
    :param cor_costura: Cor das costuras (padrão: preto).
    :param espessura_costura: Espessura do traço das costuras.
    :param textura_texto: Py5Graphics com o texto renderizado.
    """
    if cor_bola is None:
        cor_bola = py5.color(17, 70, 95)  # HSB: laranja basquete
    if cor_costura is None:
        cor_costura = py5.color(0, 0, 15)  # HSB: quase preto

    # Esfera
    py5.fill(cor_bola)
    py5.no_stroke()
    for faixa in dados.faixas:
        py5.begin_shape(py5.QUAD_STRIP)
        for v in faixa:
            nx, ny, nz = v / dados.raio
            py5.normal(nx, ny, nz)
            py5.vertex(v[0], v[1], v[2])
        py5.end_shape()

    # Texto texturizado sobre a esfera
    if textura_texto is not None and dados.patch_texto is not None:
        _desenha_patch_textura(dados.patch_texto, textura_texto)

    # Costuras
    py5.no_fill()
    py5.stroke(cor_costura)
    py5.stroke_weight(espessura_costura)
    for costura in dados.costuras:
        py5.begin_shape()
        for v in costura:
            py5.vertex(v[0], v[1], v[2])
        py5.end_shape()
