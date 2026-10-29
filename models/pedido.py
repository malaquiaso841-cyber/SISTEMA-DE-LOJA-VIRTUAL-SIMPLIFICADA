import math
from datetime import datetime
from typing import List, Optional
from models.cliente import Cliente
from models.endereco import Endereco
from models.pagamento import Pagamento
from models.item_pedido import ItemPedido
from models.carrinho import Carrinho
from models.frete import Frete
from models.cupom import Cupom
from models.produto import Produto
from services.configuracao import carregar_configuracoes
from uuid import uuid4

class Pedido:
    STATUS_PERMITIDOS = {
        "aguardando_pagamento",
        "pago",
        "enviado",
        "entregue",
        "cancelado",
    }

    TRANSICOES_PERMITIDAS = {
        "aguardando_pagamento": {"pago", "cancelado"},
        "pago": {"enviado", "cancelado"},
        "enviado": {"entregue"},
        "entregue": set(),
        "cancelado": set(),
    }

    def __init__(self, id: str, cliente: Cliente, endereco_entrega: Endereco,
    ):
        self.id = id
        self.cliente = cliente
        self.endereco_entrega = endereco_entrega
        self.itens: List["ItemPedido"] = []
        self.valor_frete = 0.0
        self.valor_desconto = 0.0
        self.status = "aguardando_pagamento"
        self.codigo_rastreio: Optional[str] = None
        self.data_criacao = datetime.now()
        self.data_entrega: Optional[datetime] = None
        self._estoque_baixado = False
        self.pagamentos: List["Pagamento"] = []
        self.prazo_entrega_dias: Optional[int] = None

    @property
    def id(self) -> str:
        return self._id

    @id.setter
    def id(self, valor: str) -> None:
        id_normalizado = str(valor).strip().upper() if valor is not None else ""

        if not id_normalizado:
            raise ValueError("O id do pedido não pode ser vazio")

        self._id = id_normalizado

    @property
    def cliente(self) -> Cliente:
        return self._cliente

    @cliente.setter
    def cliente(self, valor: Cliente) -> None:
        if not isinstance(valor, Cliente):
            raise TypeError(
                "O cliente deve ser uma instância válida da classe Cliente"
            )

        self._cliente = valor

    @property
    def endereco_entrega(self) -> Endereco:
        return self._endereco_entrega

    @endereco_entrega.setter
    def endereco_entrega(self, valor: Endereco) -> None:
        if not isinstance(valor, Endereco):
            raise TypeError(
                "O endereço de entrega deve ser uma instância válida "
                "da classe Endereco"
            )

        self._endereco_entrega = valor

    @property
    def valor_frete(self) -> float:
        return self._valor_frete

    @valor_frete.setter
    def valor_frete(self, valor) -> None:
        if valor is None or isinstance(valor, (str, bool)):
            raise TypeError("O valor do frete deve ser numérico")

        try:
            frete = float(valor)
        except (TypeError, ValueError):
            raise TypeError("O valor do frete deve ser numérico")

        if not math.isfinite(frete):
            raise ValueError("O valor do frete deve ser finito")

        if frete < 0:
            raise ValueError("O valor do frete não pode ser negativo")

        self._valor_frete = frete

    @property
    def valor_desconto(self) -> float:
        return self._valor_desconto

    @valor_desconto.setter
    def valor_desconto(self, valor) -> None:
        if valor is None or isinstance(valor, (str, bool)):
            raise TypeError("O valor do desconto deve ser numérico")

        try:
            desconto = float(valor)
        except (TypeError, ValueError):
            raise TypeError("O valor do desconto deve ser numérico")

        if not math.isfinite(desconto):
            raise ValueError("O valor do desconto deve ser finito")

        if desconto < 0:
            raise ValueError("O valor do desconto não pode ser negativo")

        self._valor_desconto = desconto

    @property
    def status(self) -> str:
        return self._status

    @status.setter
    def status(self, valor: str) -> None:
        if not isinstance(valor, str):
            raise TypeError("O status deve ser um texto")

        status_normalizado = valor.strip().lower()

        if status_normalizado not in self.STATUS_PERMITIDOS:
            raise ValueError("Status inválido")

        self._status = status_normalizado

    def calcular_total_pedido(self) -> float:
        subtotal = sum(
            item.preco_unitario * item.quantidade
            for item in self.itens
        )

        if self.valor_desconto > subtotal:
            raise ValueError(
                "O desconto não pode ultrapassar o subtotal dos itens"
            )

        return subtotal + self.valor_frete - self.valor_desconto

    def registrar_pagamento(
    self,
    pagamento: Pagamento,
    produtos: List[Produto],
) -> bool:
        if not isinstance(pagamento, Pagamento):
            raise TypeError(
                "O pagamento deve ser uma instância da classe Pagamento"
            )

        if self.status != "aguardando_pagamento":
            return False

        if pagamento in self.pagamentos:
            return False

        total_pedido = round(self.calcular_total_pedido(), 2)
        total_pago_atual = round(
            sum(item.valor for item in self.pagamentos),
            2,
        )
        novo_total_pago = round(total_pago_atual + pagamento.valor, 2)

        if novo_total_pago > total_pedido:
            raise ValueError("O pagamento ultrapassa o total do pedido")

        pagamento_quita_pedido = novo_total_pago >= total_pedido

        if pagamento_quita_pedido:
            if self._estoque_baixado:
                raise ValueError("O estoque deste pedido já foi baixado")

            # Se não houver estoque, o pagamento não é registrado.
            self._baixar_estoque(produtos)
            self._estoque_baixado = True

        self.pagamentos.append(pagamento)

        if pagamento_quita_pedido:
            self.status = "pago"

        return True

    def alterar_status(self, novo_status: str) -> None:
        if not isinstance(novo_status, str):
            raise TypeError("O status deve ser um texto")

        novo_status = novo_status.strip().lower()

        if novo_status not in self.STATUS_PERMITIDOS:
            raise ValueError("Status inválido")

        if novo_status == "pago":
            raise ValueError(
                "O pedido só pode ficar pago após registrar o pagamento completo"
            )

        if novo_status == "cancelado":
            raise ValueError(
                "Use cancelar_pedido() para cancelar e estornar o estoque"
            )

        transicoes = self.TRANSICOES_PERMITIDAS[self.status]

        if novo_status not in transicoes:
            raise ValueError(
                f"Não é permitido mudar de '{self.status}' para '{novo_status}'"
            )

        if novo_status == "enviado":
            self.codigo_rastreio = f"BR{uuid4().hex[:12].upper()}"

        self.status = novo_status

        if novo_status == "entregue":
            self.data_entrega = datetime.now()

    def fechar_pedido_com_carrinho(
        self,
        carrinho: Carrinho,
        frete: Frete,
        cupom: Optional[Cupom] = None,
    ) -> None:
        if not isinstance(carrinho, Carrinho):
            raise TypeError("O carrinho deve ser uma instância da classe Carrinho")

        if not isinstance(frete, Frete):
            raise TypeError("O frete deve ser uma instância da classe Frete")

        if carrinho.cliente != self.cliente:
            raise ValueError("O carrinho pertence a outro cliente")

        if carrinho.esta_vazio:
            raise ValueError("Não é possível fechar um pedido com carrinho vazio")

        if self.itens:
            raise ValueError("Este pedido já possui itens")

        for item in carrinho:
            if not item.produto.ativo:
                raise ValueError(
                    f"O produto '{item.produto.nome}' está inativo."
                )

            if item.quantidade > item.produto.estoque:
                raise ValueError(
                    f"Estoque insuficiente para '{item.produto.nome}'. "
                    f"Disponível: {item.produto.estoque}; "
                    f"solicitado: {item.quantidade}."
                )

        novos_itens = [
            ItemPedido(
                sku=item.produto.sku,
                quantidade=item.quantidade,
                preco_unitario=item.preco_unitario,
                digital=item.produto.digital,
                categoria=item.produto.categoria,
            )
            for item in carrinho
        ]
        
        subtotal = sum(item.subtotal for item in novos_itens)

        desconto = 0.0
        categoria_validada = None

        if cupom is not None:
            if not isinstance(cupom, Cupom):
                raise TypeError("O cupom deve ser uma instância da classe Cupom")

            categorias = cupom.categorias_elegiveis

            if categorias:
                itens_elegiveis = [
                    item
                    for item in carrinho
                    if item.produto.categoria.strip().title() in categorias
                ]

                if not itens_elegiveis:
                    raise ValueError(
                        "Nenhum item do carrinho é elegível para este cupom"
                    )

                subtotal_elegivel = sum(item.subtotal for item in itens_elegiveis)
                categoria_validada = itens_elegiveis[0].produto.categoria
            else:
                subtotal_elegivel = subtotal

            if not cupom.validar(categoria_validada):
                raise ValueError("O cupom está vencido ou esgotado")

            desconto = cupom.calcular_desconto(
                subtotal_elegivel,
                categoria=categoria_validada,
            )

        tem_produto_fisico = any(
            not item.produto.digital
            for item in carrinho
        )

        if tem_produto_fisico:
            dados_frete = frete.calcular(self.endereco_entrega)
            valor_frete = dados_frete["valor"]
            prazo_entrega_dias = dados_frete["prazo_dias"]
        else:
            valor_frete = 0.0
            prazo_entrega_dias = None

        self.itens = novos_itens
        self.valor_frete = valor_frete
        self.valor_desconto = desconto
        self.data_criacao = datetime.now()
        self.valor_frete = valor_frete
        self.prazo_entrega_dias = prazo_entrega_dias

        if cupom is not None:
            cupom.registrar_uso(categoria_validada)

        carrinho.limpar()

    def _obter_produtos_do_pedido(
        self,
        produtos: List[Produto],
    ) -> List[tuple[Produto, int]]:
        if not isinstance(produtos, list):
            raise TypeError("Os produtos devem ser informados em uma lista")

        produtos_por_sku = {}

        for produto in produtos:
            if not isinstance(produto, Produto):
                raise TypeError("A lista deve conter apenas objetos Produto")

            if produto.sku in produtos_por_sku:
                raise ValueError(f"Há mais de um produto com o SKU {produto.sku}")

            produtos_por_sku[produto.sku] = produto

        quantidades_por_sku = {}

        for item in self.itens:
            quantidades_por_sku[item.sku] = (
                quantidades_por_sku.get(item.sku, 0) + item.quantidade
            )

        ajustes = []

        for sku, quantidade in quantidades_por_sku.items():
            produto = produtos_por_sku.get(sku)

            if produto is None:
                raise ValueError(f"Produto com SKU {sku} não foi encontrado")

            ajustes.append((produto, quantidade))

        return ajustes

    def cancelar_pedido(
        self,
        janela_horas: int,
        produtos: Optional[List[Produto]] = None,
    ) -> bool:
        if isinstance(janela_horas, bool) or not isinstance(janela_horas, int):
            raise TypeError(
                "A janela de cancelamento deve ser um número inteiro de horas"
            )

        if janela_horas < 0:
            raise ValueError("A janela de cancelamento não pode ser negativa")

        horas_desde_a_criacao = (
            datetime.now() - self.data_criacao
        ).total_seconds() / 3600

        if horas_desde_a_criacao > janela_horas:
            return False

        if self.status not in {"aguardando_pagamento", "pago"}:
            return False

        if self._estoque_baixado:
            if produtos is None:
                raise ValueError(
                    "Informe a lista de produtos para estornar o estoque"
                )

            self._estornar_estoque(produtos)
            self._estoque_baixado = False

        self.status = "cancelado"
        return True

    def _baixar_estoque(self, produtos: List[Produto]) -> None:
        ajustes = self._obter_produtos_do_pedido(produtos)

        # Confere todos os produtos antes de alterar qualquer estoque.
        for produto, quantidade in ajustes:
            if produto.estoque < quantidade:
                raise ValueError(
                    f"Estoque insuficiente para {produto.nome}. "
                    f"Disponível: {produto.estoque}; solicitado: {quantidade}."
                )

        for produto, quantidade in ajustes:
            produto.atualizar_estoque(-quantidade)


    def _estornar_estoque(self, produtos: List[Produto]) -> None:
        ajustes = self._obter_produtos_do_pedido(produtos)

        for produto, quantidade in ajustes:
            produto.atualizar_estoque(quantidade)
    
    def gerar_resumo_nota(self) -> str:
        formas_pagamento = sorted({
            pagamento.forma
            for pagamento in self.pagamentos
        })
        texto_formas_pagamento = (
            ", ".join(formas_pagamento)
            if formas_pagamento
            else "Nenhum pagamento registrado"
        )

        linhas = [
            f"Pedido: {self.id}",
            f"Cliente: {self.cliente.nome}",
            f"Status: {self.status}",
            f"Endereço de entrega: {self.endereco_entrega}",
            f"Formas de pagamento: {texto_formas_pagamento}",
            "Itens:",
        ]

        for item in self.itens:
            linhas.append(
                f"- {item.sku} | "
                f"Quantidade: {item.quantidade} | "
                f"Preço unitário: R$ {item.preco_unitario:.2f} | "
                f"Subtotal: R$ {item.subtotal:.2f}"
            )

        linhas.extend([
            f"Frete: R$ {self.valor_frete:.2f}",
            f"Desconto: R$ {self.valor_desconto:.2f}",
            f"Total: R$ {self.calcular_total_pedido():.2f}",
        ])

        if self.codigo_rastreio:
            linhas.append(f"Código de rastreio: {self.codigo_rastreio}")

        if self.prazo_entrega_dias is not None:
            linhas.append(
                f"Prazo estimado de entrega: "
                f"{self.prazo_entrega_dias} dias úteis"
            )

        return "\n".join(linhas)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "cliente": self.cliente.to_dict(),
            "endereco_entrega": self.endereco_entrega.to_dict(),
            "itens": [item.to_dict() for item in self.itens],
            "valor_frete": self.valor_frete,
            "valor_desconto": self.valor_desconto,
            "status": self.status,
            "codigo_rastreio": self.codigo_rastreio,
            "data_criacao": self.data_criacao.isoformat(),
            "prazo_entrega_dias": self.prazo_entrega_dias,
            "data_entrega": (
                self.data_entrega.isoformat()
                if self.data_entrega is not None
                else None
            ),
            "estoque_baixado": self._estoque_baixado,
            "pagamentos": [
                pagamento.to_dict()
                for pagamento in self.pagamentos
            ],
        }

    @classmethod
    def from_dict(cls, dados: dict) -> "Pedido":
        pedido = cls(
            id=dados["id"],
            cliente=Cliente.from_dict(dados["cliente"]),
            endereco_entrega=Endereco.from_dict(dados["endereco_entrega"]),
        )

        pedido.itens = [
            ItemPedido.from_dict(item)
            for item in dados.get("itens", [])
        ]
        pedido.pagamentos = [
            Pagamento.from_dict(pagamento)
            for pagamento in dados.get("pagamentos", [])
        ]

        pedido.valor_frete = dados.get("valor_frete", 0.0)
        pedido.valor_desconto = dados.get("valor_desconto", 0.0)
        pedido.status = dados.get("status", "aguardando_pagamento")
        pedido.codigo_rastreio = dados.get("codigo_rastreio")
        pedido._estoque_baixado = dados.get("estoque_baixado", False)
        pedido.prazo_entrega_dias = dados.get("prazo_entrega_dias")

        if dados.get("data_criacao"):
            pedido.data_criacao = datetime.fromisoformat(dados["data_criacao"])

        if dados.get("data_entrega"):
            pedido.data_entrega = datetime.fromisoformat(dados["data_entrega"])

        return pedido

    def __repr__(self) -> str:
        return (
            f"Pedido(id='{self.id}', "
            f"cliente='{self.cliente.nome}', "
            f"status='{self.status}', "
            f"itens={len(self.itens)}, "
            f"total=R$ {self.calcular_total_pedido():.2f})"
        )




    













        


    

    

    