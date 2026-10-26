import json
from pathlib import Path

CAMINHO_CONFIGURACOES = (
    Path(__file__).resolve().parent.parent / "settings.json"
)


def carregar_configuracoes() -> dict:
    with CAMINHO_CONFIGURACOES.open("r", encoding="utf-8") as arquivo:
        return json.load(arquivo)