import math
from datetime import datetime
from typing import List, Optional


class Cupom:
    TIPOS_PERMITIDOS = {"VALOR", "PERCENTUAL"}

    def __init__(
        self,
        codigo: str,
        tipo: str,
        valor_margem: float,
        data_validade: datetime,
        uso_maximo: int,
        categorias_elegiveis: Optional[List[str]] = None,
    ):
        self.codigo = codigo
        self.tipo = tipo
        self.valor_margem = valor_margem
        self.data_validade = data_validade
        self.uso_maximo = uso_maximo
        self.categorias_elegiveis = (
            categorias_elegiveis if categorias_elegiveis is not None else []
        )
        self._usos_realizados = 0

    @property
    def codigo(self) -> str:
        return self._codigo

    @codigo.setter
    def codigo(self, valor: str) -> None:
        if not isinstance(valor, str):
            raise TypeError("O código do cupom deve ser um texto")

        codigo_limpo = valor.strip().upper()

        if not codigo_limpo:
            raise ValueError("O código não pode ser vazio")

        self._codigo = codigo_limpo

    @property
    def tipo(self) -> str:
        return self._tipo

    @tipo.setter
    def tipo(self, valor: str) -> None:
        if not isinstance(valor, str):
            raise TypeError("O tipo do cupom deve ser um texto")

        tipo_limpo = valor.strip().upper()

        if tipo_limpo not in self.TIPOS_PERMITIDOS:
            raise ValueError("O tipo deve ser VALOR ou PERCENTUAL")

        if (
            tipo_limpo == "PERCENTUAL"
            and hasattr(self, "_valor_margem")
            and self._valor_margem > 100
        ):
            raise ValueError("Um desconto percentual não pode ultrapassar 100%")

        self._tipo = tipo_limpo

    @property
    def valor_margem(self) -> float:
        return self._valor_margem

    @valor_margem.setter
    def valor_margem(self, valor: float) -> None:
        if valor is None or isinstance(valor, (str, bool)):
            raise TypeError("O valor do desconto deve ser numérico")

        try:
            valor_numerico = float(valor)
        except (TypeError, ValueError):
            raise TypeError("O valor do desconto deve ser numérico")

        if not math.isfinite(valor_numerico):
            raise ValueError("O valor do desconto deve ser finito")

        if valor_numerico <= 0:
            raise ValueError("O valor do desconto deve ser maior que zero")

        if self.tipo == "PERCENTUAL" and valor_numerico > 100:
            raise ValueError("Um desconto percentual não pode ultrapassar 100%")

        self._valor_margem = valor_numerico

    @property
    def data_validade(self) -> datetime:
        return self._data_validade

    @data_validade.setter
    def data_validade(self, valor: datetime) -> None:
        if not isinstance(valor, datetime):
            raise TypeError("A validade deve ser um objeto datetime")

        self._data_validade = valor

    @property
    def uso_maximo(self) -> int:
        return self._uso_maximo

    @uso_maximo.setter
    def uso_maximo(self, valor: int) -> None:
        if isinstance(valor, bool) or not isinstance(valor, int):
            raise TypeError("O uso máximo deve ser um número inteiro")

        if valor < 1:
            raise ValueError("O uso máximo deve ser maior que zero")

        if hasattr(self, "_usos_realizados") and valor < self._usos_realizados:
            raise ValueError(
                "O uso máximo não pode ser menor que os usos já realizados"
            )

        self._uso_maximo = valor

    @property
    def categorias_elegiveis(self) -> List[str]:
        return self._categorias_elegiveis.copy()

    @categorias_elegiveis.setter
    def categorias_elegiveis(self, valores: List[str]) -> None:
        if not isinstance(valores, list):
            raise TypeError("As categorias elegíveis devem estar em uma lista")

        categorias_limpa = []

        for categoria in valores:
            if not isinstance(categoria, str):
                raise TypeError("Cada categoria deve ser um texto")

            categoria_limpa = categoria.strip().title()

            if not categoria_limpa:
                raise ValueError("As categorias não podem ser vazias")

            categorias_limpa.append(categoria_limpa)

        self._categorias_elegiveis = categorias_limpa

    @property
    def usos_realizados(self) -> int:
        return self._usos_realizados

    def validar(self, categoria: Optional[str] = None) -> bool:
        agora = datetime.now(self.data_validade.tzinfo)

        if agora >= self.data_validade:
            return False

        if self.usos_realizados >= self.uso_maximo:
            return False

        categorias = self.categorias_elegiveis

        if categorias:
            if not isinstance(categoria, str):
                return False

            if categoria.strip().title() not in categorias:
                return False

        return True

    def calcular_desconto(
        self,
        subtotal: float,
        categoria: Optional[str] = None,
    ) -> float:
        if subtotal is None or isinstance(subtotal, (str, bool)):
            raise TypeError("O subtotal deve ser numérico")

        try:
            subtotal_numerico = float(subtotal)
        except (TypeError, ValueError):
            raise TypeError("O subtotal deve ser numérico")

        if not math.isfinite(subtotal_numerico):
            raise ValueError("O subtotal deve ser finito")

        if subtotal_numerico < 0:
            raise ValueError("O subtotal não pode ser negativo")

        if not self.validar(categoria):
            raise ValueError("O cupom está vencido, esgotado ou não é elegível")

        if self.tipo == "PERCENTUAL":
            desconto = subtotal_numerico * (self.valor_margem / 100)
        else:
            desconto = self.valor_margem

        return round(min(desconto, subtotal_numerico), 2)

    def registrar_uso(self, categoria: Optional[str] = None) -> None:
        if not self.validar(categoria):
            raise ValueError("O cupom está vencido, esgotado ou não é elegível")

        self._usos_realizados += 1

    def to_dict(self) -> dict:
        return {
            "codigo": self.codigo,
            "tipo": self.tipo,
            "valor_margem": self.valor_margem,
            "data_validade": self.data_validade.isoformat(),
            "uso_maximo": self.uso_maximo,
            "categorias_elegiveis": self.categorias_elegiveis,
            "usos_realizados": self.usos_realizados,
        }

    @classmethod
    def from_dict(cls, dados: dict) -> "Cupom":
        cupom = cls(
            codigo=dados["codigo"],
            tipo=dados["tipo"],
            valor_margem=dados["valor_margem"],
            data_validade=datetime.fromisoformat(dados["data_validade"]),
            uso_maximo=dados["uso_maximo"],
            categorias_elegiveis=dados.get("categorias_elegiveis", []),
        )

        usos_realizados = dados.get("usos_realizados", 0)

        if isinstance(usos_realizados, bool) or not isinstance(usos_realizados, int):
            raise TypeError("Os usos realizados devem ser um número inteiro")

        if usos_realizados < 0 or usos_realizados > cupom.uso_maximo:
            raise ValueError("A quantidade de usos realizados é inválida")

        cupom._usos_realizados = usos_realizados
        return cupom

    def __repr__(self) -> str:
        return (
            f"Cupom(codigo={self.codigo!r}, "
            f"tipo={self.tipo!r}, "
            f"valor_margem={self.valor_margem}, "
            f"usos={self.usos_realizados}/{self.uso_maximo})"
        )