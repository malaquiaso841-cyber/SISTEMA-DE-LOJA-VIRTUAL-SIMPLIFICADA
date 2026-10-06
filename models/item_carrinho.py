from models.produto import Produto

class ItemCarrinho:
    def __init__(self, produto: Produto, quantidade = 1):
        self.produto = produto
        self.quantidade = quantidade
        # Salva o preço no momento em que o item é adicionado
        self._preco_unitario = produto.preco_unitario

    @property
    def produto(self) -> Produto:
        return self._produto

    @produto.setter
    def produto(self, valor: Produto):
        if not isinstance(valor, Produto):
            raise TypeError("O produto deve ser uma instância válida da classe Produto.")
        self._produto = valor

    @property
    def quantidade(self):
        return self._quantidade

    @quantidade.setter
    def quantidade(self, valor: int) -> None:
        if isinstance(valor, bool) or not isinstance(valor, int):
            raise TypeError("A quantidade deve ser um número inteiro.")

        if valor < 1:
            raise ValueError("A quantidade deve ser maior que zero.")

        if valor > self._produto.estoque:
            raise ValueError(
                f"Quantidade solicitada ({valor}) é superior "
                f"ao estoque disponível ({self._produto.estoque})."
            )

        self._quantidade = valor

    @property
    def preco_unitario(self):
        return self._preco_unitario

    @property
    def subtotal(self) -> float:
        """Calcula o valor total deste item específico."""
        return self._preco_unitario * self._quantidade

    def to_dict(self):
        return {
            "produto": self.produto.to_dict(),  # Reaproveita o to_dict da classe Produto
            "quantidade": self.quantidade,
            "preco_unitario": self.preco_unitario,
            "subtotal": self.subtotal
        }

    @classmethod
    def from_dict(cls, dados: dict) -> "ItemCarrinho":
        produto = Produto.from_dict(dados["produto"])
        item = cls(produto=produto, quantidade=dados["quantidade"])
        item._preco_unitario = dados.get("preco_unitario", produto.preco_unitario)
        return item

    # MÉTODOS ESPECIAIS

    def __repr__(self):
            return (
                f"ItemCarrinho(produto='{self.produto.nome}', "
                f"qtd={self.quantidade}, subtotal=R${self.subtotal:.2f})"
            )
    
    def __eq__(self, outro: object) -> bool:
        if not isinstance(outro, ItemCarrinho):
            return False
        return self.produto.sku == outro.produto.sku

        
        


