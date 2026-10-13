from models.cliente import Cliente
from models.produto import Produto
from models.endereco import Endereco
from services.dados import (
    carregar_clientes,
    carregar_produtos,
    salvar_clientes,
    salvar_produtos,
)

def adicionar_produto(produto: Produto) -> Produto:
    if not isinstance(produto, Produto):
        raise TypeError("O produto deve ser uma instância da classe Produto")

    produtos = carregar_produtos()

    if any(item.sku == produto.sku for item in produtos):
        raise ValueError(f"Já existe um produto cadastrado com o SKU {produto.sku}")

    produtos.append(produto)
    salvar_produtos(produtos)

    return produto

def adicionar_cliente(cliente: Cliente) -> Cliente:
    if not isinstance(cliente, Cliente):
        raise TypeError("O cliente deve ser uma instância da classe Cliente")

    clientes = carregar_clientes()

    for existente in clientes:
        if existente.email.casefold() == cliente.email.casefold():
            raise ValueError("Já existe um cliente cadastrado com esse e-mail")

        if existente.cpf == cliente.cpf:
            raise ValueError("Já existe um cliente cadastrado com esse CPF")

    clientes.append(cliente)
    salvar_clientes(clientes)

    return cliente

def _buscar_produto(sku: str, produtos: list[Produto]) -> Produto:
    if not isinstance(sku, str) or not sku.strip():
        raise ValueError("O SKU não pode ser vazio")

    sku_normalizado = sku.strip().upper()

    produto = next(
        (item for item in produtos if item.sku == sku_normalizado),
        None,
    )

    if produto is None:
        raise ValueError(f"Produto com SKU {sku_normalizado} não encontrado")

    return produto

def atualizar_produto(
    sku: str,
    *,
    nome: str | None = None,
    categoria: str | None = None,
    preco_unitario: float | None = None,
    estoque: int | None = None,
) -> Produto:
    produtos = carregar_produtos()
    produto = _buscar_produto(sku, produtos)

    if nome is not None:
        produto.nome = nome

    if categoria is not None:
        produto.categoria = categoria

    if preco_unitario is not None:
        produto.preco_unitario = preco_unitario

    if estoque is not None:
        produto.estoque = estoque

    salvar_produtos(produtos)
    return produto

def alterar_status_produto(sku: str, ativo: bool) -> Produto:
    if not isinstance(ativo, bool):
        raise TypeError("O status do produto deve ser True ou False")

    produtos = carregar_produtos()
    produto = _buscar_produto(sku, produtos)
    produto.ativo = ativo

    salvar_produtos(produtos)
    return produto

def remover_produto(sku: str) -> Produto:
    produtos = carregar_produtos()
    produto = _buscar_produto(sku, produtos)

    if produto.ativo:
        raise ValueError("Inative o produto antes de removê-lo")

    produtos.remove(produto)
    salvar_produtos(produtos)

    return produto

def _buscar_cliente(
    id_cliente: str,
    clientes: list[Cliente],
) -> Cliente:
    if not isinstance(id_cliente, str) or not id_cliente.strip():
        raise ValueError("O ID do cliente não pode ser vazio")

    id_normalizado = id_cliente.strip()

    cliente = next(
        (item for item in clientes if item.id_cliente == id_normalizado),
        None,
    )

    if cliente is None:
        raise ValueError(f"Cliente com ID {id_normalizado} não encontrado")

    return cliente

def atualizar_cliente(
    id_cliente: str,
    *,
    nome: str | None = None,
    email: str | None = None,
    cpf: str | None = None,
    enderecos: list[Endereco] | None = None,
) -> Cliente:
    clientes = carregar_clientes()
    cliente = _buscar_cliente(id_cliente, clientes)

    novo_email = cliente.email
    if email is not None:
        if not isinstance(email, str):
            raise TypeError("O e-mail deve ser um texto")
        novo_email = email.strip().lower()

    novo_cpf = cliente.cpf
    if cpf is not None:
        novo_cpf = "".join(
            caractere for caractere in str(cpf)
            if caractere.isdigit()
        )

    for existente in clientes:
        if existente.id_cliente == cliente.id_cliente:
            continue

        if existente.email == novo_email:
            raise ValueError("Já existe outro cliente cadastrado com esse e-mail")

        if existente.cpf == novo_cpf:
            raise ValueError("Já existe outro cliente cadastrado com esse CPF")

    if nome is not None:
        cliente.nome = nome

    if email is not None:
        cliente.email = email

    if cpf is not None:
        cliente.cpf = cpf

    if enderecos is not None:
        cliente.enderecos = enderecos

    salvar_clientes(clientes)
    return cliente

def remover_cliente(id_cliente: str) -> Cliente:
    clientes = carregar_clientes()
    cliente = _buscar_cliente(id_cliente, clientes)

    clientes.remove(cliente)
    salvar_clientes(clientes)

    return cliente