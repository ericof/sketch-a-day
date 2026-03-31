from pathlib import Path
from sketches import DAILY_DIR
from sketches.utils.helpers.dates import format_day
from sketches.utils.helpers.dates import format_year_month


def sketch_path_for_day(day: str) -> Path:
    """Retorna o caminho do diretório de um sketch para um dia específico.

    :param day: Data em formato ISO ou relativa.
    :returns: Caminho do diretório do sketch.
    """
    formatted_year_month = format_year_month(day)
    formatted_day = format_day(day)
    dst = DAILY_DIR / formatted_year_month / formatted_day
    return dst
