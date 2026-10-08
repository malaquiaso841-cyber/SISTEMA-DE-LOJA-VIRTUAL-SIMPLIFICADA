import math

class ItemPedido:
    def __init__(self, sku: str, quantidade: int, preco_unitario: float):
        self.sku = sku
        self.quantidade = quantidade
        self.preco_unitario = preco_unitario
    
    @property
    def sku(self) -> str:
        return self._sku

    @sku.setter
    def sku(self, valor: str) -> None:
        sku_limpo = str(valor).strip().upper() if valor is not None else ""

        if not sku_limpo:
            raise ValueError("O SKU não pode ser vazio")

        sku_sem_separadores = sku_limpo.replace("-", "").replace("_", "")

        if not sku_sem_separadores.isalnum() or len(sku_limpo) < 3:
            raise ValueError(
                "O SKU deve ter pelo menos 3 caracteres e conter apenas "
                "letras, números, hífens ou underlines."
            )

        self._sku = sku_limpo

    @property
    def quantidade(self) -> int:
        return self._quantidade

    @quantidade.setter
    def quantidade(self, valor: int) -> None:
        if isinstance(valor, bool) or not isinstance(valor, int):
            raise TypeError("A quantidade deve ser um número inteiro")

        if valor < 1:
            raise ValueError("A quantidade deve ser maior que zero")

        self._quantidade = valor


    @property
    def preco_unitario(self) -> float:
        return self._preco_unitario

    @preco_unitario.setter
    def preco_unitario(self, valor: float) -> None:
        if valor is None or isinstance(valor, (str, bool)):
            raise TypeError("O preço unitário deve ser numérico")

        try:
            unitario = float(valor)
        except (TypeError, ValueError):
            raise TypeError("O preço unitário deve ser numérico")

        if not math.isfinite(unitario):
            raise ValueError("O preço unitário deve ser finito")

        if unitario <= 0:
            raise ValueError("O preço unitário deve ser maior que zero")

        self._preco_unitario = unitario


    @property
    def subtotal(self) -> float:
        return self.quantidade * self.preco_unitario
        

    def to_dict(self) -> dict:
        return {
            "sku": self.sku,
            "quantidade": self.quantidade,
            "preco_unitario": self.preco_unitario,
            "subtotal": self.subtotal,
        }

    @classmethod
    def from_dict(cls, dados: dict) -> "ItemPedido":
        return cls(
            sku=dados["sku"],
            quantidade=dados["quantidade"],
            preco_unitario=dados["preco_unitario"],
        )

    def __repr__(self) -> str:
        return (
            f"ItemPedido(sku='{self.sku}', "
            f"quantidade={self.quantidade}, "
            f"preco_unitario={self.preco_unitario:.2f}, "
            f"subtotal={self.subtotal:.2f})"
        )