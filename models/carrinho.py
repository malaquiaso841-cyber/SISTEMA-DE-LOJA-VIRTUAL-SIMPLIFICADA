from models.item_carrinho import ItemCarrinho
from models.produto import Produto
from models.cliente import Cliente

class Carrinho:
    def __init__(self, cliente: Cliente):
        self.cliente = cliente
        self._itens = []

    @property
    def cliente(self) -> Cliente:
        return self._cliente

    @cliente.setter
    def cliente(self, valor: Cliente):
        if not isinstance(valor, Cliente):
            raise TypeError("O cliente deve ser uma instância válida da classe Cliente.")
        self._cliente = valor

    @property
    def itens(self) -> list[ItemCarrinho]:
        # Retorna uma cópia da lista para impedir alterações diretas (.append, .pop) fora da classe
        return self._itens.copy()

    @property
    def esta_vazio(self) -> bool:
        return len(self._itens) == 0

    # Métodos de Manipulação de Itens

    def adicionar_item(self, produto: Produto, quantidade: int = 1) -> None:
        if not isinstance(produto, Produto):
            raise TypeError("O produto deve ser uma instância da classe Produto.")

        if not produto.ativo:
            raise ValueError(f"O produto '{produto.nome}' está inativo.")

        item_existente = next(
            (item for item in self._itens if item.produto.sku == produto.sku),
            None
        )

        if item_existente:
            item_existente.quantidade += quantidade
        else:
            novo_item = ItemCarrinho(produto=produto, quantidade=quantidade)
            self._itens.append(novo_item)

    def remover_item(self, produto_ou_sku: Produto | str):
        if isinstance(produto_ou_sku, Produto):
            sku_alvo = produto_ou_sku.sku
        elif isinstance(produto_ou_sku, str):
            sku_alvo = produto_ou_sku
        else:
            raise TypeError("O parâmetro deve ser uma instância de Produto ou uma string contendo o SKU.")

        item_encontrado = None
        for item in self._itens:
            if item.produto.sku == sku_alvo:
                item_encontrado = item
                break

        if item_encontrado:
            self._itens.remove(item_encontrado)
        else:
            raise ValueError(f"O produto com SKU '{sku_alvo}' não está no carrinho.")

    def atualizar_quantidade(self, produto_ou_sku: Produto | str, nova_quantidade: int):
        if not isinstance(nova_quantidade, int):
            raise TypeError("A quantidade deve ser um número inteiro.")
        if nova_quantidade < 0:
            raise ValueError("A quantidade não pode ser um valor negativo.")
        if nova_quantidade == 0:
            self.remover_item(produto_ou_sku)
            return

        if isinstance(produto_ou_sku, Produto):
            sku_alvo = produto_ou_sku.sku
        elif isinstance(produto_ou_sku, str):
            sku_alvo = produto_ou_sku
        else:
            raise TypeError("O parâmetro deve ser uma instância de Produto ou uma string contendo o SKU.")

        item_encontrado = None
        for item in self._itens:
            if item.produto.sku == sku_alvo:
                item_encontrado = item
                break

        if item_encontrado:
            item_encontrado.quantidade = nova_quantidade
        else:
            raise ValueError(f"O produto com SKU '{sku_alvo}' não está no carrinho.")

    def limpar(self):
        self._itens.clear()

    # Propriedades Calculadas

    @property
    def quantidade_total_itens(self) -> int:
        """Soma a quantidade de todas as unidades contidas no carrinho."""
        return sum(item.quantidade for item in self._itens)

    @property
    def subtotal(self) -> float:
        """Calcula a soma do subtotal de todos os itens do carrinho."""
        return sum(item.subtotal for item in self._itens)

    @property
    def total(self) -> float:
        """
        Retorna o valor total a ser pago pelo carrinho.
        Pode ser expandido futuramente para aplicar cupons ou frete.
        """
        return self.subtotal

    # Métodos Especiais (Dunder Methods)

    def __len__(self) -> int:
        """Retorna o número total de itens/unidades presentes no carrinho quando usado len(carrinho)."""
        return self.quantidade_total_itens
    
    def __iter__(self):
        """Permite iterar sobre os itens do carrinho em loops (ex: for item in carrinho:)."""
        return iter(self._itens)

    def __repr__(self) -> str:
        """Retorna a representação técnica do carrinho para depuração, exibições em testes e logs."""
        return (
            f"Carrinho(cliente='{self.cliente.nome}', "
            f"itens={len(self._itens)}, total=R${self.total:.2f})"
        )

    # Serialização / Persistência (JSON)

    def to_dict(self) -> dict:
        """Converte a instância do Carrinho em um dicionário compatível com JSON."""
        return {
            "cliente": self.cliente.to_dict(),
            "itens": [item.to_dict() for item in self._itens],
            "subtotal": self.subtotal,
            "total": self.total
        }

    @classmethod
    def from_dict(cls, dados: dict) -> "Carrinho":
        """Reconstrói um objeto Carrinho a partir de um dicionário."""
        cliente = Cliente.from_dict(dados["cliente"])
        carrinho = cls(cliente=cliente)
        
        for item_dict in dados.get("itens", []):
            item = ItemCarrinho.from_dict(item_dict)
            carrinho._itens.append(item)
            
        return carrinho
    




                    



                
        
            
     
        
        
            


            

        




    

