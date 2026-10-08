import json
import math
from pathlib import Path

from models.endereco import Endereco


class Frete:
    def __init__(self, caminho_configuracao=None):
        if caminho_configuracao is None:
            caminho_configuracao = (
                Path(__file__).resolve().parent.parent / "settings.json"
            )

        self._caminho_configuracao = Path(caminho_configuracao)
        self._configuracao = self._carregar_configuracao()

    def _carregar_configuracao(self) -> dict:
        if not self._caminho_configuracao.exists():
            raise FileNotFoundError(
                f"Arquivo de configuração não encontrado: "
                f"{self._caminho_configuracao}"
            )

        try:
            with self._caminho_configuracao.open(
                "r",
                encoding="utf-8",
            ) as arquivo:
                configuracao = json.load(arquivo)
        except json.JSONDecodeError as erro:
            raise ValueError(
                "O arquivo settings.json contém JSON inválido"
            ) from erro

        if not isinstance(configuracao, dict) or "frete" not in configuracao:
            raise ValueError(
                "O settings.json deve conter a configuração 'frete'"
            )

        return configuracao["frete"]

    def _obter_regra(self, endereco: Endereco) -> dict:
        if not isinstance(endereco, Endereco):
            raise TypeError(
                "O endereço deve ser uma instância da classe Endereco"
            )

        regras_por_uf = self._configuracao.get("por_uf", {})
        regra = regras_por_uf.get(endereco.uf)

        if regra is None:
            regra = self._configuracao.get("padrao")

        if not isinstance(regra, dict):
            raise ValueError(
                f"Não há regra de frete configurada para a UF {endereco.uf}"
            )

        valor = regra.get("valor")
        prazo_dias = regra.get("prazo_dias")

        if isinstance(valor, bool) or not isinstance(valor, (int, float)):
            raise ValueError("O valor do frete configurado deve ser numérico")

        if not math.isfinite(valor) or valor < 0:
            raise ValueError(
                "O valor do frete deve ser finito e não negativo"
            )

        if isinstance(prazo_dias, bool) or not isinstance(prazo_dias, int):
            raise ValueError("O prazo do frete deve ser um número inteiro de dias")

        if prazo_dias < 1:
            raise ValueError("O prazo do frete deve ser de pelo menos um dia")

        return regra

    def calcular_valor(self, endereco: Endereco) -> float:
        regra = self._obter_regra(endereco)
        return float(regra["valor"])

    def calcular_prazo(self, endereco: Endereco) -> int:
        regra = self._obter_regra(endereco)
        return regra["prazo_dias"]

    def calcular(self, endereco: Endereco) -> dict:
        regra = self._obter_regra(endereco)

        return {
            "valor": float(regra["valor"]),
            "prazo_dias": regra["prazo_dias"],
        }

    def __repr__(self) -> str:
        return f"Frete(caminho_configuracao={str(self._caminho_configuracao)!r})"