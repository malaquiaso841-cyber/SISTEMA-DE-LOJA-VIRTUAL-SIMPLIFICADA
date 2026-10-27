from services import dados
from services.seed import executar_seed


def test_seed_cria_dados_e_nao_duplica(tmp_path, monkeypatch):
    monkeypatch.setattr(dados, "PASTA_DADOS", tmp_path / "dados")

    primeira_execucao = executar_seed()

    assert primeira_execucao == {
        "produtos_adicionados": 3,
        "clientes_adicionados": 1,
        "cupons_adicionados": 2,
    }

    produtos = dados.carregar_produtos()
    produto_digital = next(
        produto
        for produto in produtos
        if produto.sku == "EBOOK-SEED-01"
    )

    assert len(produtos) == 3
    assert produto_digital.digital is True

    segunda_execucao = executar_seed()

    assert segunda_execucao == {
        "produtos_adicionados": 0,
        "clientes_adicionados": 0,
        "cupons_adicionados": 0,
    }

    assert len(dados.carregar_produtos()) == 3
    assert len(dados.carregar_clientes()) == 1
    assert len(dados.carregar_cupons()) == 2