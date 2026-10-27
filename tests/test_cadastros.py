import pytest
from services.cadastros import atualizar_cliente, remover_cliente
from models.cliente import Cliente
from models.endereco import Endereco
from models.produto import Produto
from services import dados
from services.cadastros import adicionar_cliente, adicionar_produto, atualizar_produto

@pytest.fixture
def endereco_valido():
    return Endereco(
        logradouro="Rua das Flores",
        numero="123",
        bairro="Centro",
        cidade="Juazeiro do Norte",
        uf="CE",
        cep="63000-000",
    )


@pytest.fixture
def produto_valido():
    return Produto(
        sku="MOUSE-123",
        nome="Mouse sem fio",
        categoria="Perifericos",
        preco_unitario=50.00,
        estoque=10,
    )


@pytest.fixture
def cliente_valido(endereco_valido):
    return Cliente(
        id_cliente="CLI001",
        nome="Maria Silva",
        email="maria@email.com",
        cpf="12345678900",
        enderecos=[endereco_valido],
    )


def test_adicionar_produto_salva_produto(
    tmp_path,
    monkeypatch,
    produto_valido,
):
    monkeypatch.setattr(dados, "PASTA_DADOS", tmp_path / "dados")

    adicionar_produto(produto_valido)

    produtos_salvos = dados.carregar_produtos()

    assert len(produtos_salvos) == 1
    assert produtos_salvos[0].sku == "MOUSE-123"


def test_adicionar_produto_rejeita_sku_duplicado(
    tmp_path,
    monkeypatch,
    produto_valido,
):
    monkeypatch.setattr(dados, "PASTA_DADOS", tmp_path / "dados")
    adicionar_produto(produto_valido)

    outro_produto = Produto(
        sku="mouse-123",
        nome="Outro mouse",
        categoria="Acessorios",
        preco_unitario=75.00,
        estoque=5,
    )

    with pytest.raises(ValueError, match="SKU"):
        adicionar_produto(outro_produto)


def test_adicionar_cliente_salva_cliente(
    tmp_path,
    monkeypatch,
    cliente_valido,
):
    monkeypatch.setattr(dados, "PASTA_DADOS", tmp_path / "dados")

    adicionar_cliente(cliente_valido)

    clientes_salvos = dados.carregar_clientes()

    assert len(clientes_salvos) == 1
    assert clientes_salvos[0].email == "maria@email.com"


@pytest.mark.parametrize(
    "email,cpf",
    [
        ("maria@email.com", "98765432100"),
        ("outra@email.com", "12345678900"),
    ],
)
def test_adicionar_cliente_rejeita_email_ou_cpf_duplicado(
    tmp_path,
    monkeypatch,
    endereco_valido,
    email,
    cpf,
):
    monkeypatch.setattr(dados, "PASTA_DADOS", tmp_path / "dados")

    cliente_existente = Cliente(
        id_cliente="CLI001",
        nome="Maria Silva",
        email="maria@email.com",
        cpf="12345678900",
        enderecos=[endereco_valido],
    )
    adicionar_cliente(cliente_existente)

    outro_cliente = Cliente(
        id_cliente="CLI002",
        nome="João Silva",
        email=email,
        cpf=cpf,
        enderecos=[endereco_valido],
    )

    with pytest.raises(ValueError, match="e-mail|CPF"):
        adicionar_cliente(outro_cliente)

def test_atualizar_produto_salva_alteracoes(
    tmp_path,
    monkeypatch,
    produto_valido,
):
    monkeypatch.setattr(dados, "PASTA_DADOS", tmp_path / "dados")
    adicionar_produto(produto_valido)

    atualizado = atualizar_produto(
        "MOUSE-123",
        preco_unitario=60.00,
        estoque=8,
    )

    produto_salvo = dados.carregar_produtos()[0]

    assert atualizado.preco_unitario == 60.00
    assert produto_salvo.estoque == 8

def test_atualizar_cliente_salva_alteracoes(
    tmp_path,
    monkeypatch,
    cliente_valido,
):
    monkeypatch.setattr(dados, "PASTA_DADOS", tmp_path / "dados")
    adicionar_cliente(cliente_valido)

    atualizado = atualizar_cliente(
        "CLI001",
        nome="Maria Oliveira",
        email="maria.oliveira@email.com",
    )

    cliente_salvo = dados.carregar_clientes()[0]

    assert atualizado.nome == "Maria Oliveira"
    assert cliente_salvo.email == "maria.oliveira@email.com"


@pytest.mark.parametrize(
    "email,cpf",
    [
        ("maria@email.com", "98765432100"),
        ("joao@email.com", "12345678900"),
    ],
)
def test_atualizar_cliente_rejeita_email_ou_cpf_duplicado(
    tmp_path,
    monkeypatch,
    endereco_valido,
    cliente_valido,
    email,
    cpf,
):
    monkeypatch.setattr(dados, "PASTA_DADOS", tmp_path / "dados")

    outro_cliente = Cliente(
        id_cliente="CLI002",
        nome="João Silva",
        email="joao@email.com",
        cpf="98765432100",
        enderecos=[endereco_valido],
    )

    adicionar_cliente(cliente_valido)
    adicionar_cliente(outro_cliente)

    with pytest.raises(ValueError, match="e-mail|CPF"):
        atualizar_cliente(
            "CLI002",
            email=email,
            cpf=cpf,
        )


def test_remover_cliente_apaga_do_cadastro(
    tmp_path,
    monkeypatch,
    cliente_valido,
):
    monkeypatch.setattr(dados, "PASTA_DADOS", tmp_path / "dados")
    adicionar_cliente(cliente_valido)

    removido = remover_cliente("CLI001")

    assert removido.id_cliente == "CLI001"
    assert dados.carregar_clientes() == []