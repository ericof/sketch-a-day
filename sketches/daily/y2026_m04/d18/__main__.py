"""2026-04-18
Oscar Schmidt
Uma singela homenagem a um ídolo que se foi cedo demais.
ericof.com
png
Sketch,py5,CreativeCoding
"""

from dataclasses import dataclass
from sketches.utils.draw import canvas
from sketches.utils.draw.basquete import BolaSpec
from sketches.utils.draw.basquete import calcula_bola_basquete
from sketches.utils.draw.basquete import DadosBola
from sketches.utils.draw.basquete import desenha_bola_basquete
from sketches.utils.helpers import images
from sketches.utils.helpers import sketches as helpers

import py5


sketch = helpers.info_for_sketch(__file__, __doc__)

cor_fundo = py5.color(0)
cor_fundo_interna = py5.color(47, 42, 65)  # fundo da imagem (RGB)

raio_bola = 350
resolucao = 50


@dataclass
class Rotacao:
    x: float = -102
    y: float = -69
    z: float = 0
    dist_z: float = -380


espec_bola = BolaSpec(
    raio=raio_bola,
    resolucao=resolucao,
    texto_extensao=(0.15, 0.12),
    texto_theta=1.75,  # abaixo do equador
    texto_phi=-0.16,  # longitude
    texto_rotacao_uv=True,  # corrige rotação 90°
    texto="#14",
    texto_dim=(200, 200),
    texto_fonte=80,
)


backdrop_pos = [-500.0, -500.0]  # x, y do backdrop
backdrop_tam = (0, 0)  # calculado no setup com base na imagem
backdrop_crop = 0.35  # fração central da largura a exibir (0.2 = 20%)

rotacao = Rotacao()
dados_bola: DadosBola | None = None
textura_numero: py5.Py5Graphics | None = None
imagem = None


def _cria_textura_numero(spec: BolaSpec) -> py5.Py5Graphics:
    """Renderiza '#14' em uma textura com fundo transparente."""
    centro = tuple(dim / 2 for dim in spec.texto_dim)
    # Usar JAVA2D para alpha confiável, depois copiar para P3D
    pg = py5.create_graphics(*spec.texto_dim)
    with pg.begin_draw():
        pg.background(0, 0)  # transparente
        pg.fill(30)  # quase preto
        pg.no_stroke()
        pg.text_align(py5.CENTER, py5.CENTER)
        pg.text_size(spec.texto_fonte)
        pg.text(spec.texto, *centro)
    return pg


def desenha_fundo():
    tam = max(helpers.DIMENSOES.internal) * 2
    meio = tam / 2
    with py5.push():
        py5.translate(0, 0, -raio_bola * 1.4)
        py5.no_stroke()
        py5.fill(cor_fundo_interna)
        with py5.begin_shape(py5.QUADS):
            py5.normal(0, 0, 1)
            py5.vertex(-meio, -meio, 0)
            py5.vertex(meio, -meio, 0)
            py5.vertex(meio, meio, 0)
            py5.vertex(-meio, meio, 0)


def desenha_backdrop(escala: float = 1.0):
    if imagem is None:
        return
    # Dimensões da região visível, escaladas
    vis_w = backdrop_tam[0] * backdrop_crop * escala
    vis_h = backdrop_tam[1] * escala
    # Canto inferior direito da área interna
    # internal = (800, 800), centrado em (500, 500) → dir-inf = (900, 900)
    _, (iw, ih) = helpers.DIMENSOES.external, helpers.DIMENSOES.internal
    cx, cy = helpers.DIMENSOES.centro
    # Borda direita/inferior da área interna
    dir_x = cx + iw / 2
    inf_y = cy + ih / 2
    # Posicionar o quad com canto inferior direito nesse ponto
    x1 = dir_x
    y1 = inf_y
    x0 = x1 - vis_w
    y0 = y1 - vis_h
    # UV centralizado
    u0 = 0.5 - backdrop_crop / 2
    u1 = 0.5 + backdrop_crop / 2

    with py5.push():
        py5.translate(0, 0, -1)
        py5.texture_mode(py5.NORMAL)
        py5.no_stroke()
        py5.no_lights()
        with py5.begin_shape(py5.QUADS):
            py5.texture(imagem)
            py5.vertex(x0, y0, 0, u0, 0)
            py5.vertex(x1, y0, 0, u1, 0)
            py5.vertex(x1, y1, 0, u1, 1)
            py5.vertex(x0, y1, 0, u0, 1)


def aplica_rotacao_iluminacao():
    py5.rotate_y(py5.radians(rotacao.y))
    py5.rotate_x(py5.radians(rotacao.x))
    py5.rotate_z(py5.radians(rotacao.z))

    # Iluminação
    py5.point_light(360, 0, 100, 400, -300, 400)
    py5.point_light(360, 0, 60, -300, 200, -200)
    py5.ambient_light(0, 0, 30)


def setup():
    global dados_bola, textura_numero, imagem, backdrop_tam
    py5.size(*helpers.DIMENSOES.external, py5.P3D)
    py5.color_mode(py5.HSB, 360, 100, 100)
    dados_bola = calcula_bola_basquete(spec=espec_bola)
    textura_numero = _cria_textura_numero(spec=espec_bola)
    img_array = images.resource_image_as_array("oscar.jpg")
    # Adicionar canal alpha (255 = opaco) se a imagem for RGB
    if img_array.shape[2] == 3:
        import numpy as np

        alpha = np.full((*img_array.shape[:2], 1), 255, dtype=img_array.dtype)
        img_array = np.concatenate([alpha, img_array], axis=2)
    backdrop_tam = (img_array.shape[1], img_array.shape[0])  # (largura, altura)
    imagem = py5.create_image_from_numpy(img_array)


def draw():
    py5.background(cor_fundo)

    # Backdrop atrás da bola
    desenha_backdrop(escala=0.5)

    # Fundo com iluminação mas sem rotação
    with py5.push():
        py5.translate(*helpers.DIMENSOES.centro, rotacao.dist_z)
        py5.point_light(360, 0, 100, 400, -300, 400)
        py5.point_light(360, 0, 60, -300, 200, -200)
        py5.ambient_light(0, 0, 30)
        desenha_fundo()

    # Resetar luzes do fundo antes da bola
    py5.no_lights()

    # Bola com rotação e iluminação
    with py5.push():
        py5.translate(*helpers.DIMENSOES.centro, rotacao.dist_z)
        aplica_rotacao_iluminacao()
        if dados_bola:
            desenha_bola_basquete(
                dados_bola,
                espessura_costura=5.5,
                textura_texto=textura_numero,
            )

    msg = (
        f"R: ({rotacao.x:.1f}, {rotacao.y:.1f}, "
        f"{rotacao.z:.1f}) | "
        f"Z: {rotacao.dist_z:.1f}"
    )
    py5.window_title(msg)
    py5.no_lights()
    canvas.sketch_frame(
        sketch,
        cor_fundo,
        "large_transparent_white",
        "transparent_white",
        version=2,
        msg=msg,
    )


def key_pressed():
    match py5.key:
        case " ":
            save_and_close()
        case "-":
            rotacao.dist_z -= 20
        case "+":
            rotacao.dist_z += 20
    match py5.key_code:
        case py5.UP:
            rotacao.x += 3
        case py5.DOWN:
            rotacao.x -= 3
        case py5.LEFT:
            rotacao.y += 3
        case py5.RIGHT:
            rotacao.y -= 3


def save_and_close():
    py5.no_loop()
    canvas.save_sketch_image(sketch)
    py5.exit_sketch()


if __name__ == "__main__":
    py5.run_sketch()
