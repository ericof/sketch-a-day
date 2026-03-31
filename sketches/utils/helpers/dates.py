from datetime import date
from datetime import timedelta


def process_day(day: str) -> str:
    """Converte datas relativas (today, yesterday, tomorrow) para formato ISO.

    :param day: Data em formato ISO (YYYY-MM-DD) ou relativa
        ('today', 'yesterday', 'tomorrow').
    :returns: Data em formato ISO (YYYY-MM-DD).
    """
    day = day.lower()
    today = date.today()
    if day == "today":
        day = f"{today}"
    elif day == "yesterday":
        day = f"{today + timedelta(days=-1)}"
    elif day == "tomorrow":
        day = f"{today + timedelta(days=1)}"
    return day


def format_year_month(day: str) -> str:
    """Formata a data para o padrão de diretório ano/mês (ex: 'y2026_m03').

    :param day: Data em formato ISO ou relativa.
    :returns: String no formato 'yAAAA_mMM'.
    """
    day = process_day(day)
    return f"y{day[:4]}_m{day[5:7]}"


def format_day(day: str) -> str:
    """Formata o dia para o padrão de diretório (ex: 'd31').

    :param day: Data em formato ISO ou relativa.
    :returns: String no formato 'dDD'.
    """
    day = process_day(day)
    return f"d{day[8:10]}"
