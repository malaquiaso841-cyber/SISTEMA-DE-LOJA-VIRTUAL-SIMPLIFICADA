class Produto:
    def __init__(self, sku, nome, categoria, preco_unitario, estoque=0, ativo = True ):
        self.sku = sku
        self.nome = nome
        self.categoria = categoria
        self.preco_unitario = preco_unitario
        self.estoque = estoque
        self.ativo = ativo

    @property
    def sku(self):
        return self._sku

    @sku.setter
    def sku(self, valor):
        sku_limpo = str(valor).strip().upper() if valor is not None else ""
        if not sku_limpo:
            raise ValueError("O sku não pode ser vazio")

        # 3. Remove hífens e underlines temporariamente para validar se o resto é alfanumérico
        sku_sem_separadores = sku_limpo.replace("-", "").replace("_", "")

        # 4. Garante que contém apenas letras/números (sem caracteres especiais ou espaços internos) e tem tamanho mínimo
        if not sku_sem_separadores.isalnum() or len(sku_limpo) < 3:
            raise ValueError("O SKU deve conter pelo menos 3 caracteres e apenas letras, números, hífens ou traços.")

        self._sku = sku_limpo

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, valor):
        nome_limpo = str(valor).strip() if valor is not None else ""
        if not nome_limpo:
            raise ValueError("O nome do produto não pode ser vazio")
        if len(nome_limpo) < 3:
            raise ValueError("O nome do produto deve ter pelo menos 3 caracteres.")
        self._nome = nome_limpo

    @property
    def categoria(self):
        return self._categoria

    @categoria.setter
    def categoria(self, valor):
        categoria_limpa = str(valor).strip().title() if valor is not None else ""
        if not categoria_limpa:
            raise ValueError("A categoria não pode ser vazia")
        if len(categoria_limpa) < 3:
            raise ValueError("A categoria deve ter pelo menos 3 caracteres.")
        self._categoria = categoria_limpa

    @property
    def preco_unitario(self):
        return self._preco_unitario

    @preco_unitario.setter
    def preco_unitario(self, valor):
        try:
             valor_float = float(valor)
        except (TypeError, ValueError):
             raise ValueError("O preço unitário deve ser um número válido.")
        if valor_float <= 0:
             raise ValueError("O preço unitário deve ser maior que zero.")
        self._preco_unitario = valor_float

    @property
    def estoque(self):
        return self._estoque

    @estoque.setter
    def estoque(self, valor):
        try:
            valor_int = int(valor)
        except (TypeError, ValueError):
             raise ValueError("O valor do estoque deve ser um número inteiro.")
        if valor_int < 0:
             raise ValueError("O valor do estoque não pode ser negativo")
        self._estoque = valor_int

    @property
    def ativo(self):
        return self._ativo

    @ativo.setter
    def ativo(self, valor):
        if not isinstance(valor, bool):
            raise ValueError("O status 'ativo' deve ser um valor booleano (True ou False).")
        self._ativo = valor


    # Metodo de atualização do estoque

    def atualizar_estoque(self, quantidade: int) -> None:
        try:
            qtd_int = int(quantidade)
        except (TypeError, ValueError):
            raise ValueError("A quantidade para atualização do estoque deve ser um número inteiro.")
        novo_estoque = self.estoque + qtd_int
        if novo_estoque < 0:
            raise ValueError(
            f"Estoque insuficiente para o produto '{self.nome}'. "
            f"Disponível: {self.estoque}, Solicitado para baixa: {abs(qtd_int)}."
        )
        self.estoque = novo_estoque

    def to_dict(self):
        return{
            "sku": self.sku,
            "nome": self.nome,
            "categoria": self.categoria,
            "preco_unitario": self.preco_unitario,
            "estoque": self.estoque,
            "ativo": self.ativo
        }

    def __str__(self) -> str:
        status = "Ativo" if self.ativo else "Inativo"
        return (
            f"{self.nome} (SKU: {self.sku}) - "
            f"R$ {self.preco_unitario:.2f} | Estoque: {self.estoque} | Status: {status}"
        )

    def __repr__(self) -> str:
        return (
            f"Produto(sku={self.sku!r}, nome={self.nome!r}, categoria={self.categoria!r}, "
            f"preco_unitario={self.preco_unitario}, estoque={self.estoque}, ativo={self.ativo})"
        )

    def __eq__(self, outro: object) -> bool:
        if not isinstance(outro, Produto):
            return False
        return self.sku == outro.sku

    def __lt__(self, outro: "Produto") -> bool:
        if not isinstance(outro, Produto):
            return NotImplemented
        return self.preco_unitario < outro.preco_unitario