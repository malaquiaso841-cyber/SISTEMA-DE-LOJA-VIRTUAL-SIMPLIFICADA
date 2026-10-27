from datetime import datetime, timedelta

from models.cliente import Cliente
from models.cupom import Cupom
from models.endereco import Endereco
from models.produto import Produto
from services.configuracao import carregar_configuracoes
from services.dados import (
    carregar_clientes,
    carregar_cupons,
    carregar_produtos,
    salvar_clientes,
    salvar_cupons,
    salvar_produtos,
)


def executar_seed() -> dict[str, int]:
    produtos = carregar_produtos()
    clientes = carregar_clientes()
    cupons = carregar_cupons()

    produtos_adicionados = 0
    clientes_adicionados = 0
    cupons_adicionados = 0

    produtos_iniciais = [
        Produto(
            sku="MOUSE-SEED-01",
            nome="Mouse sem fio",
            categoria="Perifericos",
            preco_unitario=50.00,
            estoque=20,
        ),
        Produto(
            sku="TECLADO-SEED-01",
            nome="Teclado mecânico",
            categoria="Perifericos",
            preco_unitario=150.00,
            estoque=10,
        ),
         Produto(
            sku="EBOOK-SEED-01",
            nome="E-book de Python",
            categoria="Livros Digitais",
            preco_unitario=39.90,
            estoque=999,
            digital=True,
        ),
    ]

    for produto in produtos_iniciais:
        ja_cadastrado = any(
            existente.sku == produto.sku
            for existente in produtos
        )

        if not ja_cadastrado:
            produtos.append(produto)
            produtos_adicionados += 1

    endereco_inicial = Endereco(
        logradouro="Rua de Exemplo",
        numero="100",
        bairro="Centro",
        cidade="Juazeiro do Norte",
        uf="CE",
        cep="63000-000",
    )

    cliente_inicial = Cliente(
        id_cliente="CLI-SEED-01",
        nome="Cliente Exemplo",
        email="cliente.seed@example.com",
        cpf="12345678901",
        enderecos=[endereco_inicial],
    )

    cliente_ja_cadastrado = any(
        existente.id_cliente == cliente_inicial.id_cliente
        or existente.email == cliente_inicial.email
        or existente.cpf == cliente_inicial.cpf
        for existente in clientes
    )

    if not cliente_ja_cadastrado:
        clientes.append(cliente_inicial)
        clientes_adicionados += 1

    dias_validade = carregar_configuracoes()["cupons"]["validade_padrao_dias"]

    cupons_iniciais = [
        Cupom(
            codigo="SEED10",
            tipo="PERCENTUAL",
            valor_margem=10,
            data_validade=datetime.now() + timedelta(days=dias_validade),
            uso_maximo=100,
            categorias_elegiveis=["Perifericos"],
        ),
        Cupom(
            codigo="SEED5",
            tipo="VALOR",
            valor_margem=5.00,
            data_validade=datetime.now() + timedelta(days=30),
            uso_maximo=50,
            categorias_elegiveis=[],
        ),
    ]

    for cupom in cupons_iniciais:
        ja_cadastrado = any(
            existente.codigo == cupom.codigo
            for existente in cupons
        )

        if not ja_cadastrado:
            cupons.append(cupom)
            cupons_adicionados += 1

    if produtos_adicionados:
        salvar_produtos(produtos)

    if clientes_adicionados:
        salvar_clientes(clientes)

    if cupons_adicionados:
        salvar_cupons(cupons)

    return {
        "produtos_adicionados": produtos_adicionados,
        "clientes_adicionados": clientes_adicionados,
        "cupons_adicionados": cupons_adicionados,
    }


if __name__ == "__main__":
    resultado = executar_seed()

    print("Carga inicial concluída:")
    print(f"Produtos adicionados: {resultado['produtos_adicionados']}")
    print(f"Clientes adicionados: {resultado['clientes_adicionados']}")
    print(f"Cupons adicionados: {resultado['cupons_adicionados']}")