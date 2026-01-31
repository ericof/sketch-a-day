from .formas import criar_mascara_furo
from dataclasses import dataclass
from sketches.utils.data import SketchInfo

import py5


@dataclass
class TextBoxStyle:
    """Style for the date box."""

    color: str = "#FFF"
    background_color: str | None = "#000"
    stroke: str | None = "#000"
    stroke_weight: int = 2
    font: str = "ArialNarrow-Bold"
    font_size: int = 16


STYLES: dict[str, TextBoxStyle] = {
    "default": TextBoxStyle(),
    "dark": TextBoxStyle(color="#FFF", background_color="#000", stroke="#FFF"),
    "light": TextBoxStyle(color="#000", background_color="#FFF", stroke="#000"),
    "transparent": TextBoxStyle(color="#000", background_color=None, stroke=None),
    "transparent_white": TextBoxStyle(color="#FFF", background_color=None, stroke=None),
    "large_transparent_white": TextBoxStyle(
        color="#FFF", background_color=None, stroke=None, font_size=24
    ),
    "numero": TextBoxStyle(
        color="#FFF", background_color=None, stroke=None, font_size=48
    ),
}


def draw_text_box(
    text: str,
    style_name: str = "default",
    x: float = 0.0,
    y: float = 0.0,
    align: int = py5.CENTER,
    font: str | None = None,
    font_size: int | None = None,
):
    """Draw a text box with the given text and style."""
    style = STYLES.get(style_name, STYLES["default"])
    font = font or style.font
    font_size = font_size or style.font_size
    color = py5.color(style.color)
    bg_color = py5.color(style.background_color) if style.background_color else None
    stroke = py5.color(style.stroke) if style.stroke else None
    text_lines = text.split("\n")
    with py5.push_style():
        py5.rect_mode(py5.CENTER)
        font = py5.create_font(font, font_size, True)
        py5.text_font(font)
        py5.text_size(font_size)

        width = max(py5.text_width(text) * 1.3 for text in text_lines)
        height = font_size * len(text_lines) * 1.2

        # Frame
        if bg_color:
            py5.fill(bg_color)
        else:
            py5.no_fill()

        if stroke:
            py5.stroke(stroke)
            py5.stroke_weight(style.stroke_weight)
        else:
            py5.no_stroke()

        py5.rect(x, y, width, height)

        # Text
        py5.fill(color)
        py5.text_align(align, py5.CENTER)
        py5.text(text, x, y)


def date_box(sketch: SketchInfo, style_name: str = "default"):
    largura, altura = sketch.size.external
    altura_int = sketch.size.internal[0]
    x = largura // 2
    y = (altura - altura_int) // 4
    draw_text_box(sketch.title, style_name, x, y)


def date_description_box(sketch: SketchInfo, style_name: str = "default"):
    largura, altura = sketch.size.external
    altura_int = sketch.size.internal[0]
    x = largura // 2
    y = (altura - altura_int) // 3
    text = f"{sketch.title}\n{sketch.description}"
    draw_text_box(text, style_name, x, y)


def credits_box(sketch: SketchInfo, style_name: str = "default"):
    largura, altura = sketch.size.external
    largura_int, altura_int = sketch.size.internal
    x = largura - ((largura - largura_int) * 0.1)
    y = altura - ((altura - altura_int) * 0.25)
    text = sketch.other_credits
    if text.strip():
        draw_text_box(text, style_name, x, y, align=py5.RIGHT)


def sketch_frame(
    sketch: SketchInfo,
    cor_fundo: int = py5.color("#FFF"),
    date_style: str = "default",
    credits_style: str = "transparent",
    version: int = 1,
    z: int = 1,
):
    """Draw the sketch frame with date and credits."""
    with py5.push():
        py5.rect_mode(py5.CORNER)
        py5.shape_mode(py5.CORNER)
        py5.translate(0, 0, z)
        with py5.push():
            py5.rect_mode(py5.CORNER)
            py5.fill(cor_fundo)
            buraco = py5.create_shape(
                py5.RECT, *sketch.size.pos_interno, *sketch.size.internal
            )
            frame = criar_mascara_furo(buraco, 0, 0, *sketch.size.external)
            frame.set_fill(cor_fundo)
            py5.shape(frame)
        with py5.push():
            match version:
                case 1:
                    date_box(sketch, date_style)
                case 2:
                    date_description_box(sketch, date_style)
        with py5.push():
            credits_box(sketch, credits_style)


def save_sketch_image(sketch: SketchInfo):
    img_path = sketch.path / f"{sketch.day}.{sketch.format}"
    img = py5.get_pixels()
    img.save(img_path)
