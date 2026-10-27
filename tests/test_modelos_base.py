import json
from datetime import datetime, timedelta

import pytest
from pytest import approx

from models.carrinho import Carrinho
from models.cliente import Cliente
from models.cupom import Cupom
from models.endereco import Endereco
from models.frete import Frete
from models.pagamento import Pagamento
from models.pedido import Pedido
from models.produto import Produto
from models.item_pedido import ItemPedido


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


@pytest.fixture
def pedido_valido(cliente_valido, endereco_valido):
    return Pedido(
        id="PED-001",
        cliente=cliente_valido,
        endereco_entrega=endereco_valido,
    )


@pytest.fixture
def carrinho_com_item(cliente_valido, produto_valido):
    carrinho = Carrinho(cliente_valido)
    carrinho.adicionar_item(produto_valido, quantidade=1)
    return carrinho


@pytest.fixture
def frete_configurado(tmp_path):
    configuracao = {
        "frete": {
            "por_uf": {
                "CE": {
                    "valor": 15.00,
                    "prazo_dias": 5,
                }
            },
            "padrao": {
                "valor": 30.00,
                "prazo_dias": 12,
            },
        }
    }

    caminho = tmp_path / "settings.json"
    caminho.write_text(json.dumps(configuracao), encoding="utf-8")

    return Frete(caminho_configuracao=caminho)


def criar_cupom(
    codigo="DESCONTO",
    tipo="VALOR",
    valor=5.00,
    categorias=None,
):
    return Cupom(
        codigo=codigo,
        tipo=tipo,
        valor_margem=valor,
        data_validade=datetime.now() + timedelta(days=10),
        uso_maximo=3,
        categorias_elegiveis=categorias or [],
    )


def criar_endereco(uf):
    return Endereco(
        logradouro="Rua das Flores",
        numero="123",
        bairro="Centro",
        cidade="Crato",
        uf=uf,
        cep="63100-000",
    )


def pagar_pedido(pedido, produto):
    """Registra um pagamento integral e passa a lista de produtos ao pedido."""
    pagamento = Pagamento(
        data=datetime.now(),
        forma="PIX",
        valor=pedido.calcular_total_pedido(),
    )
    return pedido.registrar_pagamento(
        pagamento,
        produtos=[produto],
    )


# Produto, cliente e endereço


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


def test_cliente_rejeita_cpf_com_quantidade_errada_de_digitos(
    endereco_valido,
):
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


# Fechamento do pedido


def test_fechar_pedido_com_carrinho(
    pedido_valido,
    cliente_valido,
    produto_valido,
    frete_configurado,
):
    carrinho = Carrinho(cliente_valido)
    carrinho.adicionar_item(produto_valido, quantidade=2)
    cupom = criar_cupom(valor=5.00)

    pedido_valido.fechar_pedido_com_carrinho(
        carrinho=carrinho,
        frete=frete_configurado,
        cupom=cupom,
    )

    assert len(pedido_valido.itens) == 1
    assert pedido_valido.itens[0].sku == "MOUSE-123"
    assert pedido_valido.itens[0].quantidade == 2
    assert pedido_valido.itens[0].preco_unitario == approx(50.00)
    assert pedido_valido.valor_frete == approx(15.00)
    assert pedido_valido.valor_desconto == approx(5.00)
    assert pedido_valido.calcular_total_pedido() == approx(110.00)
    assert carrinho.esta_vazio


def test_pedido_sem_cupom_fica_com_desconto_zero(
    pedido_valido,
    carrinho_com_item,
    frete_configurado,
):
    pedido_valido.fechar_pedido_com_carrinho(
        carrinho=carrinho_com_item,
        frete=frete_configurado,
    )

    assert pedido_valido.valor_desconto == 0.0
    assert pedido_valido.valor_frete == approx(15.00)
    assert pedido_valido.calcular_total_pedido() == approx(65.00)


def test_pedido_rejeita_carrinho_vazio(
    pedido_valido,
    cliente_valido,
    frete_configurado,
):
    carrinho = Carrinho(cliente_valido)

    with pytest.raises(ValueError, match="carrinho vazio"):
        pedido_valido.fechar_pedido_com_carrinho(
            carrinho=carrinho,
            frete=frete_configurado,
        )


def test_pedido_rejeita_carrinho_de_outro_cliente(
    pedido_valido,
    produto_valido,
    endereco_valido,
    frete_configurado,
):
    outro_cliente = Cliente(
        id_cliente="CLI002",
        nome="João Silva",
        email="joao@email.com",
        cpf="987.654.321-00",
        enderecos=[endereco_valido],
    )

    carrinho = Carrinho(outro_cliente)
    carrinho.adicionar_item(produto_valido)

    with pytest.raises(ValueError, match="outro cliente"):
        pedido_valido.fechar_pedido_com_carrinho(
            carrinho=carrinho,
            frete=frete_configurado,
        )


def test_pedido_rejeita_cupom_de_categoria_nao_elegivel(
    pedido_valido,
    carrinho_com_item,
    frete_configurado,
):
    cupom = criar_cupom(
        codigo="ROUPAS10",
        tipo="PERCENTUAL",
        valor=10,
        categorias=["Roupas"],
    )

    with pytest.raises(ValueError):
        pedido_valido.fechar_pedido_com_carrinho(
            carrinho=carrinho_com_item,
            frete=frete_configurado,
            cupom=cupom,
        )


# Pagamentos


def test_pagamento_total_muda_status_do_pedido_para_pago(
    pedido_valido,
    carrinho_com_item,
    frete_configurado,
    produto_valido,
):
    pedido_valido.fechar_pedido_com_carrinho(
        carrinho_com_item,
        frete=frete_configurado,
    )

    estoque_inicial = produto_valido.estoque
    pagamento = Pagamento(
        data=datetime.now(),
        forma="PIX",
        valor=pedido_valido.calcular_total_pedido(),
    )

    resultado = pedido_valido.registrar_pagamento(
        pagamento,
        produtos=[produto_valido],
    )

    assert resultado is True
    assert pagamento in pedido_valido.pagamentos
    assert pedido_valido.status == "pago"
    assert produto_valido.estoque == estoque_inicial - 1


def test_pagamentos_parciais_completam_o_total(
    pedido_valido,
    carrinho_com_item,
    frete_configurado,
    produto_valido,
):
    pedido_valido.fechar_pedido_com_carrinho(
        carrinho_com_item,
        frete=frete_configurado,
    )

    estoque_inicial = produto_valido.estoque
    primeiro = Pagamento(datetime.now(), "PIX", 20.00)
    segundo = Pagamento(datetime.now(), "DEBITO", 45.00)

    assert pedido_valido.registrar_pagamento(
        primeiro,
        produtos=[produto_valido],
    ) is True
    assert pedido_valido.status == "aguardando_pagamento"
    assert produto_valido.estoque == estoque_inicial

    assert pedido_valido.registrar_pagamento(
        segundo,
        produtos=[produto_valido],
    ) is True
    assert pedido_valido.status == "pago"
    assert len(pedido_valido.pagamentos) == 2
    assert produto_valido.estoque == estoque_inicial - 1


def test_pagamento_acima_do_total_e_rejeitado(
    pedido_valido,
    carrinho_com_item,
    frete_configurado,
    produto_valido,
):
    pedido_valido.fechar_pedido_com_carrinho(
        carrinho_com_item,
        frete=frete_configurado,
    )
    pagamento = Pagamento(datetime.now(), "PIX", 66.00)

    with pytest.raises(ValueError, match="ultrapassa"):
        pedido_valido.registrar_pagamento(
            pagamento,
            produtos=[produto_valido],
        )

    assert pedido_valido.pagamentos == []
    assert pedido_valido.status == "aguardando_pagamento"


def test_pagamento_integral_e_rejeitado_se_estoque_for_insuficiente(
    pedido_valido,
    carrinho_com_item,
    frete_configurado,
    produto_valido,
):
    pedido_valido.fechar_pedido_com_carrinho(
        carrinho_com_item,
        frete=frete_configurado,
    )

    produto_valido.estoque = 0
    pagamento = Pagamento(
        datetime.now(),
        "PIX",
        pedido_valido.calcular_total_pedido(),
    )

    with pytest.raises(ValueError, match="Estoque insuficiente"):
        pedido_valido.registrar_pagamento(
            pagamento,
            produtos=[produto_valido],
        )

    assert pedido_valido.pagamentos == []
    assert pedido_valido.status == "aguardando_pagamento"
    assert produto_valido.estoque == 0


def test_mesmo_pagamento_nao_e_registrado_duas_vezes(
    pedido_valido,
    carrinho_com_item,
    frete_configurado,
    produto_valido,
):
    pedido_valido.fechar_pedido_com_carrinho(
        carrinho_com_item,
        frete=frete_configurado,
    )
    pagamento = Pagamento(datetime.now(), "PIX", 20.00)

    assert pedido_valido.registrar_pagamento(
        pagamento,
        produtos=[produto_valido],
    ) is True
    assert pedido_valido.registrar_pagamento(
        pagamento,
        produtos=[produto_valido],
    ) is False
    assert len(pedido_valido.pagamentos) == 1


def test_registrar_objeto_que_nao_e_pagamento_gera_erro(
    pedido_valido,
    carrinho_com_item,
    frete_configurado,
    produto_valido,
):
    pedido_valido.fechar_pedido_com_carrinho(
        carrinho_com_item,
        frete=frete_configurado,
    )

    with pytest.raises(TypeError, match="Pagamento"):
        pedido_valido.registrar_pagamento(
            "PIX",
            produtos=[produto_valido],
        )


# Status, cancelamento e representação do pedido


def test_pedido_permite_transicao_ate_entregue(
    pedido_valido,
    carrinho_com_item,
    frete_configurado,
    produto_valido,
):
    pedido_valido.fechar_pedido_com_carrinho(
        carrinho_com_item,
        frete=frete_configurado,
    )
    pagar_pedido(pedido_valido, produto_valido)

    pedido_valido.alterar_status("enviado")
    pedido_valido.alterar_status("entregue")

    assert pedido_valido.status == "entregue"
    assert pedido_valido.data_entrega is not None


def test_pedido_rejeita_transicao_invalida(pedido_valido):
    with pytest.raises(ValueError, match="Não é permitido"):
        pedido_valido.alterar_status("entregue")


def test_pedido_pode_ser_cancelado_dentro_da_janela(pedido_valido):
    resultado = pedido_valido.cancelar_pedido(janela_horas=2)

    assert resultado is True
    assert pedido_valido.status == "cancelado"


def test_pedido_nao_pode_ser_cancelado_fora_da_janela(pedido_valido):
    pedido_valido.data_criacao = datetime.now() - timedelta(hours=3)

    resultado = pedido_valido.cancelar_pedido(janela_horas=2)

    assert resultado is False
    assert pedido_valido.status == "aguardando_pagamento"


def test_pedido_enviado_nao_pode_ser_cancelado(
    pedido_valido,
    carrinho_com_item,
    frete_configurado,
    produto_valido,
):
    pedido_valido.fechar_pedido_com_carrinho(
        carrinho_com_item,
        frete=frete_configurado,
    )
    pagar_pedido(pedido_valido, produto_valido)
    pedido_valido.alterar_status("enviado")

    resultado = pedido_valido.cancelar_pedido(
        janela_horas=2,
        produtos=[produto_valido],
    )

    assert resultado is False
    assert pedido_valido.status == "enviado"


def test_resumo_da_nota_contem_dados_do_pedido(
    pedido_valido,
    carrinho_com_item,
    frete_configurado,
    produto_valido,
):
    cupom = criar_cupom(valor=5.00)

    pedido_valido.fechar_pedido_com_carrinho(
        carrinho_com_item,
        frete=frete_configurado,
        cupom=cupom,
    )

    pagamento = Pagamento(
        data=datetime.now(),
        forma="PIX",
        valor=pedido_valido.calcular_total_pedido(),
    )
    pedido_valido.registrar_pagamento(
        pagamento,
        produtos=[produto_valido],
    )

    resumo = pedido_valido.gerar_resumo_nota()

    assert "MOUSE-123" in resumo
    assert "Subtotal: R$ 50.00" in resumo
    assert "Endereço de entrega: Rua das Flores" in resumo
    assert "Formas de pagamento: PIX" in resumo
    assert "Total: R$ 60.00" in resumo


def test_repr_do_pedido_contem_id_e_status(pedido_valido):
    representacao = repr(pedido_valido)

    assert "PED-001" in representacao
    assert "aguardando_pagamento" in representacao


def test_pedido_rejeita_frete_negativo(pedido_valido):
    with pytest.raises(ValueError, match="negativo"):
        pedido_valido.valor_frete = -1.00


def test_pedido_rejeita_desconto_negativo(pedido_valido):
    with pytest.raises(ValueError, match="negativo"):
        pedido_valido.valor_desconto = -1.00


def test_pedido_rejeita_status_invalido(pedido_valido):
    with pytest.raises(ValueError, match="Status inválido"):
        pedido_valido.status = "em preparação"


def test_pedido_preserva_dados_ao_serializar_e_reconstruir(
    pedido_valido,
    carrinho_com_item,
    frete_configurado,
    produto_valido,
):
    pedido_valido.fechar_pedido_com_carrinho(
        carrinho_com_item,
        frete=frete_configurado,
    )
    pedido_valido.registrar_pagamento(
        Pagamento(datetime.now(), "PIX", 20.00),
        produtos=[produto_valido],
    )

    dados = pedido_valido.to_dict()
    pedido_reconstruido = Pedido.from_dict(dados)

    assert pedido_reconstruido.to_dict() == dados


def test_alterar_status_nao_pode_marcar_pedido_como_pago(pedido_valido):
    with pytest.raises(ValueError, match="pagamento completo"):
        pedido_valido.alterar_status("pago")


def test_alterar_status_nao_pode_cancelar_pedido_diretamente(pedido_valido):
    with pytest.raises(ValueError, match="cancelar_pedido"):
        pedido_valido.alterar_status("cancelado")


# Cupom


@pytest.fixture
def cupom_percentual():
    return criar_cupom(
        codigo="DESCONTO10",
        tipo="PERCENTUAL",
        valor=10,
    )


def test_cupom_percentual_calcula_desconto(cupom_percentual):
    desconto = cupom_percentual.calcular_desconto(100.00)

    assert desconto == approx(10.00)


def test_cupom_valor_nao_ultrapassa_subtotal():
    cupom = criar_cupom(
        codigo="DESCONTO200",
        tipo="VALOR",
        valor=200.00,
    )

    desconto = cupom.calcular_desconto(100.00)

    assert desconto == approx(100.00)


def test_cupom_verifica_categoria_elegivel():
    cupom = criar_cupom(
        codigo="ROUPA10",
        tipo="PERCENTUAL",
        valor=10,
        categorias=["Roupas"],
    )

    assert cupom.validar(categoria="Roupas") is True
    assert cupom.validar(categoria="Eletrônicos") is False


def test_cupom_rejeita_categoria_nao_elegivel():
    cupom = criar_cupom(
        codigo="ROUPA10",
        tipo="PERCENTUAL",
        valor=10,
        categorias=["Roupas"],
    )

    with pytest.raises(ValueError):
        cupom.calcular_desconto(100.00, categoria="Eletrônicos")


def test_cupom_expirado_e_invalido():
    cupom = Cupom(
        codigo="VENCIDO",
        tipo="VALOR",
        valor_margem=10.00,
        data_validade=datetime.now() - timedelta(days=1),
        uso_maximo=3,
    )

    assert cupom.validar() is False


def test_cupom_esgotado_fica_invalido():
    cupom = Cupom(
        codigo="ULTIMOUSO",
        tipo="VALOR",
        valor_margem=10.00,
        data_validade=datetime.now() + timedelta(days=10),
        uso_maximo=1,
    )

    cupom.registrar_uso()

    assert cupom.usos_realizados == 1
    assert cupom.validar() is False


def test_cupom_preserva_dados_na_serializacao(cupom_percentual):
    dados = cupom_percentual.to_dict()
    cupom_reconstruido = Cupom.from_dict(dados)

    assert cupom_reconstruido.to_dict() == dados


# Frete


def test_frete_calcula_valor_e_prazo_por_uf(frete_configurado):
    endereco = criar_endereco("CE")

    assert frete_configurado.calcular_valor(endereco) == approx(15.00)
    assert frete_configurado.calcular_prazo(endereco) == 5


def test_frete_usa_regra_padrao_para_uf_sem_regra(frete_configurado):
    endereco = criar_endereco("SP")

    resultado = frete_configurado.calcular(endereco)

    assert resultado == {
        "valor": 30.00,
        "prazo_dias": 12,
    }


def test_frete_rejeita_objeto_que_nao_e_endereco(frete_configurado):
    with pytest.raises(TypeError):
        frete_configurado.calcular_valor("63100-000")


# Estoque e cancelamento


def test_pagamento_parcial_nao_baixa_estoque(
    pedido_valido,
    carrinho_com_item,
    frete_configurado,
    produto_valido,
):
    pedido_valido.fechar_pedido_com_carrinho(
        carrinho_com_item,
        frete=frete_configurado,
    )
    estoque_inicial = produto_valido.estoque
    pagamento_parcial = Pagamento(datetime.now(), "PIX", 20.00)

    pedido_valido.registrar_pagamento(
        pagamento_parcial,
        produtos=[produto_valido],
    )

    assert produto_valido.estoque == estoque_inicial
    assert pedido_valido.status == "aguardando_pagamento"


def test_pagamento_total_da_baixa_no_estoque(
    pedido_valido,
    carrinho_com_item,
    frete_configurado,
    produto_valido,
):
    pedido_valido.fechar_pedido_com_carrinho(
        carrinho_com_item,
        frete=frete_configurado,
    )
    estoque_inicial = produto_valido.estoque
    total = pedido_valido.calcular_total_pedido()
    pagamento = Pagamento(datetime.now(), "PIX", total)

    pedido_valido.registrar_pagamento(
        pagamento,
        produtos=[produto_valido],
    )

    assert produto_valido.estoque == estoque_inicial - 1
    assert pedido_valido.status == "pago"


def test_cancelar_pedido_pago_repoe_estoque(
    pedido_valido,
    carrinho_com_item,
    frete_configurado,
    produto_valido,
):
    pedido_valido.fechar_pedido_com_carrinho(
        carrinho_com_item,
        frete=frete_configurado,
    )
    estoque_inicial = produto_valido.estoque
    pagamento = Pagamento(
        datetime.now(),
        "PIX",
        pedido_valido.calcular_total_pedido(),
    )
    pedido_valido.registrar_pagamento(
        pagamento,
        produtos=[produto_valido],
    )

    resultado = pedido_valido.cancelar_pedido(
        janela_horas=2,
        produtos=[produto_valido],
    )

    assert resultado is True
    assert pedido_valido.status == "cancelado"
    assert produto_valido.estoque == estoque_inicial


def test_cancelamento_repetido_nao_repoe_estoque_duas_vezes(
    pedido_valido,
    carrinho_com_item,
    frete_configurado,
    produto_valido,
):
    pedido_valido.fechar_pedido_com_carrinho(
        carrinho_com_item,
        frete=frete_configurado,
    )
    pagamento = Pagamento(
        datetime.now(),
        "PIX",
        pedido_valido.calcular_total_pedido(),
    )
    pedido_valido.registrar_pagamento(
        pagamento,
        produtos=[produto_valido],
    )
    pedido_valido.cancelar_pedido(
        janela_horas=2,
        produtos=[produto_valido],
    )
    estoque_apos_cancelamento = produto_valido.estoque

    resultado = pedido_valido.cancelar_pedido(
        janela_horas=2,
        produtos=[produto_valido],
    )

    assert resultado is False
    assert produto_valido.estoque == estoque_apos_cancelamento

def test_enviar_pedido_gera_e_preserva_codigo_rastreio(
    pedido_valido,
    carrinho_com_item,
    frete_configurado,
    produto_valido,
):
    pedido_valido.fechar_pedido_com_carrinho(
        carrinho_com_item,
        frete=frete_configurado,
    )

    pagamento = Pagamento(
        data=datetime.now(),
        forma="PIX",
        valor=pedido_valido.calcular_total_pedido(),
    )
    pedido_valido.registrar_pagamento(
        pagamento,
        produtos=[produto_valido],
    )

    pedido_valido.alterar_status("enviado")

    assert pedido_valido.status == "enviado"
    assert pedido_valido.codigo_rastreio is not None
    assert pedido_valido.codigo_rastreio.startswith("BR")
    assert len(pedido_valido.codigo_rastreio) == 14

    dados = pedido_valido.to_dict()
    pedido_reconstruido = Pedido.from_dict(dados)

    assert pedido_reconstruido.codigo_rastreio == pedido_valido.codigo_rastreio

def test_pedido_com_apenas_produto_digital_nao_cobra_frete(
    pedido_valido,
    cliente_valido,
    frete_configurado,
):
    produto_digital = Produto(
        sku="EBOOK-01",
        nome="E-book de Python",
        categoria="Livros Digitais",
        preco_unitario=50.00,
        estoque=10,
        digital=True,
    )
    carrinho = Carrinho(cliente_valido)
    carrinho.adicionar_item(produto_digital, quantidade=1)

    pedido_valido.fechar_pedido_com_carrinho(
        carrinho=carrinho,
        frete=frete_configurado,
    )

    assert pedido_valido.itens[0].digital is True
    assert pedido_valido.valor_frete == approx(0.00)
    assert pedido_valido.calcular_total_pedido() == approx(50.00)


def test_pedido_misto_cobra_frete_pelos_produtos_fisicos(
    pedido_valido,
    cliente_valido,
    produto_valido,
    frete_configurado,
):
    produto_digital = Produto(
        sku="EBOOK-01",
        nome="E-book de Python",
        categoria="Livros Digitais",
        preco_unitario=20.00,
        estoque=10,
        digital=True,
    )
    carrinho = Carrinho(cliente_valido)
    carrinho.adicionar_item(produto_valido, quantidade=1)
    carrinho.adicionar_item(produto_digital, quantidade=1)

    pedido_valido.fechar_pedido_com_carrinho(
        carrinho=carrinho,
        frete=frete_configurado,
    )

    assert pedido_valido.valor_frete == approx(15.00)
    assert pedido_valido.calcular_total_pedido() == approx(85.00)

def test_produto_digital_preserva_campo_na_serializacao():
    produto = Produto(
        sku="EBOOK-01",
        nome="E-book de Python",
        categoria="Livros Digitais",
        preco_unitario=50.00,
        estoque=10,
        digital=True,
    )

    dados = produto.to_dict()
    produto_reconstruido = Produto.from_dict(dados)

    assert dados["digital"] is True
    assert produto_reconstruido.digital is True


def test_item_pedido_digital_preserva_campo_na_serializacao():
    item = ItemPedido(
        sku="EBOOK-01",
        quantidade=1,
        preco_unitario=50.00,
        digital=True,
    )

    dados = item.to_dict()
    item_reconstruido = ItemPedido.from_dict(dados)

    assert dados["digital"] is True
    assert item_reconstruido.digital is True


def test_produto_antigo_sem_campo_digital_e_considerado_fisico():
    dados = {
        "sku": "PROD-01",
        "nome": "Produto físico",
        "categoria": "Acessórios",
        "preco_unitario": 25.00,
        "estoque": 5,
        "ativo": True,
    }

    produto = Produto.from_dict(dados)

    assert produto.digital is False