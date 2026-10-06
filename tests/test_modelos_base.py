import pytest

from models.cliente import Cliente
from models.endereco import Endereco
from models.produto import Produto


@pytest.fixture
def endereco_valido():
    return Endereco(
        logradouro="Rua das Flores",
        numero="123",
        bairro="Centro",
        cidade="Juazeiro do Norte",
        uf="CE",
        cep="63000-000",
        complemento="Apto 101",
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
        cpf="123.456.789-00",
        enderecos=[endereco_valido],
    )


def test_produto_criado_com_dados_validos(produto_valido):
    assert produto_valido.sku == "MOUSE-123"
    assert produto_valido.preco_unitario == 50.00
    assert produto_valido.estoque == 10
    assert produto_valido.ativo is True


@pytest.mark.parametrize("preco", [0, -1])
def test_produto_rejeita_preco_zero_ou_negativo(preco):
    with pytest.raises(ValueError):
        Produto(
            sku="MOUSE-123",
            nome="Mouse sem fio",
            categoria="Perifericos",
            preco_unitario=preco,
            estoque=10,
        )


def test_produto_rejeita_estoque_negativo():
    with pytest.raises(ValueError):
        Produto(
            sku="MOUSE-123",
            nome="Mouse sem fio",
            categoria="Perifericos",
            preco_unitario=50.00,
            estoque=-1,
        )


def test_produto_rejeita_baixa_maior_que_estoque(produto_valido):
    with pytest.raises(ValueError):
        produto_valido.atualizar_estoque(-11)


def test_produtos_com_mesmo_sku_sao_iguais(produto_valido):
    outro = Produto(
        sku="MOUSE-123",
        nome="Outro nome",
        categoria="Acessorios",
        preco_unitario=75.00,
        estoque=2,
    )

    assert produto_valido == outro


def test_cliente_criado_com_dados_validos(cliente_valido):
    assert cliente_valido.nome == "Maria Silva"
    assert cliente_valido.email == "maria@email.com"
    assert cliente_valido.cpf == "12345678900"
    assert len(cliente_valido.enderecos) == 1


@pytest.mark.parametrize("email", ["", "email-invalido", "usuario@"])
def test_cliente_rejeita_email_invalido(email, endereco_valido):
    with pytest.raises(ValueError):
        Cliente(
            id_cliente="CLI001",
            nome="Maria Silva",
            email=email,
            cpf="12345678900",
            enderecos=[endereco_valido],
        )


def test_cliente_rejeita_cpf_com_quantidade_errada_de_digitos(endereco_valido):
    with pytest.raises(ValueError):
        Cliente(
            id_cliente="CLI001",
            nome="Maria Silva",
            email="maria@email.com",
            cpf="12345",
            enderecos=[endereco_valido],
        )


def test_endereco_criado_com_dados_validos(endereco_valido):
    assert endereco_valido.uf == "CE"
    assert endereco_valido.cep == "63000000"
    assert endereco_valido.cep_formatado() == "63000-000"


def test_endereco_rejeita_uf_invalida():
    with pytest.raises(ValueError):
        Endereco(
            logradouro="Rua das Flores",
            numero="123",
            bairro="Centro",
            cidade="Juazeiro do Norte",
            uf="Ceará",
            cep="63000-000",
        )


def test_endereco_rejeita_cep_invalido():
    with pytest.raises(ValueError):
        Endereco(
            logradouro="Rua das Flores",
            numero="123",
            bairro="Centro",
            cidade="Juazeiro do Norte",
            uf="CE",
            cep="123",
        )