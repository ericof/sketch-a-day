from collections import defaultdict

import re
import requests


def texto_de_url(url: str) -> str:
    """Obtém o texto presente em uma url."""
    response = requests.get(url, timeout=3)
    response.raise_for_status()
    return response.text


SCRIPT_IGNORAR = [
    (r"^\d.*", "Linhas que comecem com número"),
    (r"^[\t|\ ]+\(.*\)", "Linhas com parenteses"),
    (r"^[\t|\ ]+STAR TREK.*", "Linhas que comecem com STAR TREK"),
    (r"^[\t|\ ]+[A-Z]{2}[A-Z'\.\: ]+", "Linhas indicam fala de personagens"),
]


def processa_script(texto: str) -> str:
    """Processa o texto de um script, removendo linhas indesejadas."""
    linhas = []
    comecou = False
    total = 0
    eliminados = defaultdict(int)
    for linha in texto.splitlines():
        total += 1
        if linha.startswith("1 "):
            comecou = True
        elif not comecou:
            eliminados["Não começou"] += 1
            continue
        valida = True
        for padrao, descricao in SCRIPT_IGNORAR:
            if re.match(padrao, linha):
                eliminados[descricao] += 1
                valida = False
                break
        if valida:
            linhas.append(linha.strip())
    return "\n".join(linhas)
