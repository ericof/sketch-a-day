"""2025-07-09
Mapas: Machu Picchu, Peru
Machu Picchu, Peru
ericof.com|Poly data (c) OpenStreetMap contributors|https://www.openstreetmap.org/copyright
png
Sketch,py5,CreativeCoding
"""

from sketches.utils import mapas
from sketches.utils.draw import canvas
from sketches.utils.draw import formas
from sketches.utils.draw.cores.paletas import gera_paleta
from sketches.utils.helpers import sketches as helpers
from sketches.utils.mapas.estilos import get_paleta_estilos

import py5


sketch = helpers.info_for_sketch(__file__, __doc__)


def camadas_mapa(
    dados: mapas.GeodataEscalado, paleta, cor_base, largura, altura
) -> list[tuple[py5.Py5Shape, int]]:
    estilos_elementos = get_paleta_estilos("simples")
    mapa = mapas.mapa_como_forma(
        dados,
        cor_base,
        camadas=[
            ("caminhos", mapas.processa_caminhos(py5.color("#1a1307"), 1)),
            (
                "elementos",
                mapas.processa_elementos(None, 0.5, estilos=estilos_elementos),
            ),
        ],
    )
    camadas = [(mapa, -1)]
    if camada_limite := [c.gdf for c in dados.camadas if c.nome == "limites"]:
        limites = mapas.dataframe_para_shape(camada_limite[0])
        mascara = formas.criar_mascara_furo(limites, 0, 0, largura, altura)
        mascara.set_fill(py5.color("#000"))
        mascara.set_stroke(py5.color("#CCC"))
        mascara.set_stroke_weight(5)
        # Ocultar o mapa
        for _ in range(2):
            camadas.append((mascara, 0))

    return camadas


def setup():
    py5.size(*helpers.DIMENSOES.external, py5.P3D)
    cor_fundo = py5.color("#000000")
    py5.background(cor_fundo)
    paleta = gera_paleta("mandarin-redux", True)
    cor_base = py5.color("#f5ebd8")
    tags = {"building": True, "natural": True}
    dados: mapas.GeodataEscalado = mapas.escala_dados(
        mapas.obtem_dados(
            "osmid:W157376572", pasta=sketch.path, tags=tags, percentual=20
        ),
    )
    camadas = camadas_mapa(dados, paleta, cor_base, *helpers.DIMENSOES.internal)
    with py5.push_matrix():
        py5.translate(*helpers.DIMENSOES.pos_interno, -1)
        for forma, z in camadas:
            with py5.push_matrix():
                py5.translate(0, 0, z)
                py5.shape(forma, 0, 0)
    # Credits and go
    canvas.sketch_frame(
        sketch,
        cor_fundo,
        date_style="large_transparent_white",
        credits_style="transparent_white",
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
