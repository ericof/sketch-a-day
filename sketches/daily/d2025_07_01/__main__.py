"""2025-07-01
Mapas: Exílio 01
Mapa do bairro de Pinheiros, São Paulo, SP, Brasil
ericof.com|Poly data (c) OpenStreetMap contributors|https://www.openstreetmap.org/copyright
png
Sketch,py5,CreativeCoding
"""

from sketches.utils import mapas
from sketches.utils.draw import canvas
from sketches.utils.draw import formas
from sketches.utils.draw.cores.paletas import gera_paleta
from sketches.utils.helpers import sketches as helpers

import py5


sketch = helpers.info_for_sketch(__file__, __doc__)


def camadas_mapa(
    dados: mapas.GeodataEscalado, paleta, cor_base, largura, altura
) -> list[tuple[py5.Py5Shape, int]]:
    mapa = mapas.mapa_como_forma(
        dados,
        cor_base,
        camadas=[
            ("caminhos", mapas.processa_caminhos(py5.color("#FFFFFF"), 1)),
            ("elementos", mapas.processa_elementos(paleta, 5.0)),
        ],
    )
    camadas = [(mapa, -1)]
    if camada_limite := [c.gdf for c in dados.camadas if c.nome == "limites"]:
        limites = mapas.dataframe_para_shape(camada_limite[0])
        mascara = formas.criar_mascara_furo(limites, 0, 0, largura, altura)
        mascara.set_fill(py5.color(200, 200, 200, 85))
        mascara.set_stroke(py5.color("#FF9600"))
        mascara.set_stroke_weight(3)
        # Ocultar o mapa
        for _ in range(5):
            camadas.append((mascara, 0))

    return camadas


def setup():
    py5.size(*helpers.DIMENSOES.external, py5.P3D)
    cor_fundo = py5.color(250)
    py5.background(cor_fundo)
    paleta = gera_paleta("tons-azul-01", True)
    cor_base = py5.color("#7EB7FF")
    dados: mapas.GeodataEscalado = mapas.escala_dados(
        mapas.obtem_dados("Pinheiros, São Paulo, São Paulo, Brasil", pasta=sketch.path),
    )
    camadas = camadas_mapa(dados, paleta, cor_base, *helpers.DIMENSOES.internal)
    with py5.push_matrix():
        py5.translate(*helpers.DIMENSOES.pos_interno, -1)
        for forma, z in camadas:
            with py5.push_matrix():
                py5.translate(0, 0, z)
                py5.shape(forma, 0, 0)
    # Credits and go
    canvas.sketch_frame(sketch, cor_fundo, date_style="transparent")


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
