import pytest
from models.cliente import Cliente
from models.endereco import Endereco
from models.produto import Produto
from models.carrinho import Carrinho


# --- FIXTURES COMPATÍVEIS COM AS REGRAS DAS SUAS CLASSES ---

@pytest.fixture
def cliente_valido():
    endereco = Endereco(
        logradouro="Rua das Flores",
        numero="123",
        bairro="Centro",
        cidade="Juazeiro do Norte",
        uf="CE",
        cep="63000-000",
        complemento="Apto 101"
    )
    return Cliente(
        id_cliente="CLI001",
        nome="Maria Silva",
        email="maria@email.com",
        cpf="123.456.789-00",
        enderecos=[endereco]
    )


@pytest.fixture
def produto_mouse():
    return Produto(
        sku="MOUSE-123",
        nome="Mouse Sem Fio",
        categoria="Perifericos",
        preco_unitario=50.00,
        estoque=10
    )


@pytest.fixture
def produto_teclado():
    return Produto(
        sku="TECLADO-456",
        nome="Teclado Mecanico",
        categoria="Perifericos",
        preco_unitario=150.00,
        estoque=5
    )


@pytest.fixture
def carrinho(cliente_valido):
    return Carrinho(cliente=cliente_valido)


# --- SUÍTE COMPLETA DE TESTES ---

def test_inicializacao_carrinho_vazio(carrinho, cliente_valido):
    """Valida estado inicial do carrinho recém-criado."""
    assert carrinho.cliente == cliente_valido
    assert carrinho.esta_vazio is True
    assert len(carrinho) == 0
    assert carrinho.subtotal == 0.0
    assert carrinho.quantidade_total_itens == 0


def test_adicionar_item_novo(carrinho, produto_mouse):
    """Valida adição de produto no carrinho e atualização dos totais."""
    carrinho.adicionar_item(produto_mouse, quantidade=2)

    assert carrinho.esta_vazio is False
    assert len(carrinho) == 1
    assert carrinho.quantidade_total_itens == 2
    assert carrinho.subtotal == 100.00


def test_adicionar_produto_duplicado_acumula_quantidade(carrinho, produto_mouse):
    """Valida se adicionar o mesmo SKU apenas incrementa a quantidade."""
    carrinho.adicionar_item(produto_mouse, quantidade=2)
    carrinho.adicionar_item(produto_mouse, quantidade=3)

    assert len(carrinho) == 1
    assert carrinho.quantidade_total_itens == 5
    assert carrinho.subtotal == 250.00


def test_remover_item_por_objeto_e_por_sku(carrinho, produto_mouse, produto_teclado):
    """Valida remoção por instância de Produto e por string SKU."""
    carrinho.adicionar_item(produto_mouse, quantidade=1)
    carrinho.adicionar_item(produto_teclado, quantidade=1)

    carrinho.remover_item(produto_mouse)
    assert len(carrinho) == 1

    carrinho.remover_item("TECLADO-456")
    assert carrinho.esta_vazio is True


def test_remover_item_inexistente_gera_erro(carrinho, produto_mouse):
    """Valida exceção ao tentar remover produto que não está na lista."""
    with pytest.raises(ValueError):
        carrinho.remover_item(produto_mouse)


def test_atualizar_quantidade(carrinho, produto_mouse):
    """Valida alteração manual da quantidade do item."""
    carrinho.adicionar_item(produto_mouse, quantidade=2)
    carrinho.atualizar_quantidade(produto_mouse, nova_quantidade=5)

    assert carrinho.quantidade_total_itens == 5
    assert carrinho.subtotal == 250.00


def test_atualizar_quantidade_para_zero_remove_item(carrinho, produto_mouse):
    """Valida se definir quantidade 0 dispara a remoção automática do produto."""
    carrinho.adicionar_item(produto_mouse, quantidade=2)
    carrinho.atualizar_quantidade(produto_mouse, nova_quantidade=0)

    assert carrinho.esta_vazio is True


def test_adicionar_item_tipo_invalido_gera_erro(carrinho):
    """Valida exceção ao tentar passar tipo incorreto no parâmetro do produto."""
    with pytest.raises(TypeError):
        carrinho.adicionar_item("objeto_invalido", quantidade=1)


def test_limpar_carrinho(carrinho, produto_mouse, produto_teclado):
    """Valida o método de esvaziar o carrinho."""
    carrinho.adicionar_item(produto_mouse, quantidade=1)
    carrinho.adicionar_item(produto_teclado, quantidade=1)

    carrinho.limpar()

    assert carrinho.esta_vazio is True
    assert len(carrinho) == 0
    assert carrinho.subtotal == 0.0


def test_serializacao_json(carrinho, produto_mouse):
    """Valida conversão para dicionário (to_dict) e reconstrução (from_dict)."""
    carrinho.adicionar_item(produto_mouse, quantidade=2)

    dados_dict = carrinho.to_dict()
    assert isinstance(dados_dict, dict)
    assert dados_dict["cliente"]["email"] == "maria@email.com"
    assert len(dados_dict["itens"]) == 1

    carrinho_reconstruido = Carrinho.from_dict(dados_dict)
    assert carrinho_reconstruido.cliente.nome == "Maria Silva"
    assert len(carrinho_reconstruido) == 1
    assert carrinho_reconstruido.subtotal == 100.00