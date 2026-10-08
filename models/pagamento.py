from datetime import datetime
import math

class Pagamento:
    FORMAS_PERMITIDAS = {
        "PIX",
        "CREDITO",
        "DEBITO",
        "BOLETO",
    }

    def __init__(
        self,
        data: datetime,
        forma: str,
        valor: float,
    ):
        self.data = data
        self.forma = forma
        self.valor = valor

    @property
    def data(self) -> datetime:
        return self._data

    @data.setter
    def data(self, valor: datetime) -> None:
        if not isinstance(valor, datetime):
            raise TypeError("A data do pagamento deve ser um objeto datetime")

        self._data = valor

    @property
    def forma(self) -> str:
        return self._forma

    @forma.setter
    def forma(self, valor: str) -> None:
        if not isinstance(valor, str):
            raise TypeError("A forma de pagamento deve ser um texto")
        forma_pagamento_limpa = valor.strip().upper()
        if not forma_pagamento_limpa:
            raise ValueError("A forma de pagamento não pode ser vazia")
        if  forma_pagamento_limpa not in self.FORMAS_PERMITIDAS:
            raise ValueError("Forma inválida. Use PIX, CREDITO, DEBITO ou BOLETO")
        self._forma = forma_pagamento_limpa
        
    @property
    def valor(self) -> float:
        return self._valor

    @valor.setter
    def valor(self, valor: float) -> None:
        if valor is None or isinstance(valor, (str, bool)):
            raise TypeError("O valor do pagamento deve ser númerico")
        try:
            valor_numerico = float(valor)
        except(TypeError, ValueError):
            raise TypeError("O valor do pagamento deve ser númerico")
        if not math.isfinite(valor_numerico):
            raise ValueError("O valor do pagamento deve ser um número finito")
        if valor_numerico <= 0:
            raise ValueError("O valor do pagamento deve ser maior que zero")
        self._valor = valor_numerico

    def to_dict(self) -> dict:
        return{
            "data": self.data.isoformat(),
            "forma": self.forma,
            "valor": self.valor
        }
    @classmethod
    def from_dict(cls, dados: dict) -> "Pagamento":
        return cls(
            data=datetime.fromisoformat(dados["data"]),
            forma=dados["forma"],
            valor=dados["valor"],
        )

    def __repr__(self) -> str:
        return (
            f"Pagamento(data={self.data.isoformat()!r}, "
            f"forma={self.forma!r}, "
            f"valor={self.valor:.2f})"
        )
