import json
from datetime import datetime
from services.operacoes_pedido import alterar_status_pedido
import pytest
from models.carrinho import Carrinho
from models.cliente import Cliente
from models.endereco import Endereco
from models.frete import Frete
from models.pagamento import Pagamento
from models.pedido import Pedido
from models.produto import Produto
from services import dados
from services.relatorios import gerar_relatorio_pedidos_por_status
from services.relatorios import gerar_relatorio_faturamento_por_periodo
from services.relatorios import gerar_relatorio_top_produtos_e_ticket_medio
from services.relatorios import gerar_relatorio_vendas_por_uf
from services.relatorios import gerar_relatorio_vendas_por_categoria
from services.operacoes_pedido import (
    cancelar_pedido as cancelar_pedido_com_persistencia,
    registrar_pagamento_pedido,
)


@pytest.fixture
def pedido_salvo(tmp_path, monkeypatch):
    # Direciona os arquivos JSON de teste para uma pasta temporária.
    monkeypatch.setattr(dados, "PASTA_DADOS", tmp_path / "dados")

    endereco = Endereco(
        logradouro="Rua das Flores",
        numero="123",
        bairro="Centro",
        cidade="Juazeiro do Norte",
        uf="CE",
        cep="63000-000",
    )

    cliente = Cliente(
        id_cliente="CLI001",
        nome="Maria Silva",
        email="maria@email.com",
        cpf="12345678900",
        enderecos=[endereco],
    )

    produto = Produto(
        sku="MOUSE-123",
        nome="Mouse sem fio",
        categoria="Perifericos",
        preco_unitario=50.00,
        estoque=10,
    )

    caminho_configuracao = tmp_path / "settings.json"
    caminho_configuracao.write_text(
        json.dumps({
            "frete": {
                "por_uf": {
                    "CE": {"valor": 15.00, "prazo_dias": 5}
                },
                "padrao": {"valor": 30.00, "prazo_dias": 12},
            }
        }),
        encoding="utf-8",
    )

    frete = Frete(caminho_configuracao=caminho_configuracao)
    carrinho = Carrinho(cliente)
    carrinho.adicionar_item(produto, quantidade=1)

    pedido = Pedido(
        id="PED-001",
        cliente=cliente,
        endereco_entrega=endereco,
    )
    pedido.fechar_pedido_com_carrinho(
        carrinho=carrinho,
        frete=frete,
    )

    dados.salvar_produtos([produto])
    dados.salvar_pedidos([pedido])

    return pedido


def test_pagamento_salva_baixa_do_estoque(pedido_salvo):
    pagamento = Pagamento(
        data=datetime.now(),
        forma="PIX",
        valor=pedido_salvo.calcular_total_pedido(),
    )

    resultado = registrar_pagamento_pedido(
        pedido_id="PED-001",
        pagamento=pagamento,
    )

    produtos_salvos = dados.carregar_produtos()
    pedidos_salvos = dados.carregar_pedidos()

    assert resultado is True
    assert produtos_salvos[0].estoque == 9
    assert pedidos_salvos[0].status == "pago"
    assert pedidos_salvos[0]._estoque_baixado is True


def test_cancelamento_salva_reposicao_do_estoque(pedido_salvo):
    pagamento = Pagamento(
        data=datetime.now(),
        forma="PIX",
        valor=pedido_salvo.calcular_total_pedido(),
    )

    registrar_pagamento_pedido(
        pedido_id="PED-001",
        pagamento=pagamento,
    )

    resultado = cancelar_pedido_com_persistencia(
        pedido_id="PED-001",
        janela_horas=2,
    )

    produtos_salvos = dados.carregar_produtos()
    pedidos_salvos = dados.carregar_pedidos()

    assert resultado is True
    assert produtos_salvos[0].estoque == 10
    assert pedidos_salvos[0].status == "cancelado"
    assert pedidos_salvos[0]._estoque_baixado is False

def test_envio_salva_status_e_codigo_de_rastreio(pedido_salvo):
    pagamento = Pagamento(
        data=datetime.now(),
        forma="PIX",
        valor=pedido_salvo.calcular_total_pedido(),
    )

    registrar_pagamento_pedido("PED-001", pagamento)
    alterar_status_pedido("PED-001", "enviado")

    pedido_recarregado = dados.carregar_pedidos()[0]

    assert pedido_recarregado.status == "enviado"
    assert pedido_recarregado.codigo_rastreio is not None
    assert pedido_recarregado.codigo_rastreio.startswith("BR")

def test_entrega_salva_data_de_entrega(pedido_salvo):
    pagamento = Pagamento(
        data=datetime.now(),
        forma="PIX",
        valor=pedido_salvo.calcular_total_pedido(),
    )

    registrar_pagamento_pedido("PED-001", pagamento)
    alterar_status_pedido("PED-001", "enviado")
    alterar_status_pedido("PED-001", "entregue")

    pedido_recarregado = dados.carregar_pedidos()[0]

    assert pedido_recarregado.status == "entregue"
    assert pedido_recarregado.data_entrega is not None

def test_relatorio_pedidos_por_status_mostra_quantidade_e_percentual(
    pedido_salvo,
):
    relatorio = gerar_relatorio_pedidos_por_status()

    assert "Total de pedidos: 1" in relatorio
    assert "Aguardando Pagamento: 1 (100.0%)" in relatorio
    assert "Cancelado: 0 (0.0%)" in relatorio

def test_relatorio_pedidos_por_status_mostra_quantidade_e_percentual(
    pedido_salvo,
):
    relatorio = gerar_relatorio_pedidos_por_status()

    assert "Total de pedidos: 1" in relatorio
    assert "Aguardando Pagamento: 1 (100.0%)" in relatorio
    assert "Cancelado: 0 (0.0%)" in relatorio

def test_relatorio_top_produtos_e_ticket_medio(pedido_salvo):
    pagamento = Pagamento(
        data=datetime.now(),
        forma="PIX",
        valor=pedido_salvo.calcular_total_pedido(),
    )
    registrar_pagamento_pedido("PED-001", pagamento)

    relatorio = gerar_relatorio_top_produtos_e_ticket_medio(limite=5)

    assert "Ticket médio: R$ 65.00" in relatorio
    assert "SKU: MOUSE-123 | Unidades vendidas: 1" in relatorio

def test_relatorio_vendas_por_uf(pedido_salvo):
    pagamento = Pagamento(
        data=datetime.now(),
        forma="PIX",
        valor=pedido_salvo.calcular_total_pedido(),
    )
    registrar_pagamento_pedido("PED-001", pagamento)

    relatorio = gerar_relatorio_vendas_por_uf()

    assert "CE: 1 pedido(s)" in relatorio
    assert "Faturamento: R$ 65.00" in relatorio

def test_relatorio_vendas_por_categoria(pedido_salvo):
    pagamento = Pagamento(
        data=datetime.now(),
        forma="PIX",
        valor=pedido_salvo.calcular_total_pedido(),
    )
    registrar_pagamento_pedido("PED-001", pagamento)

    relatorio = gerar_relatorio_vendas_por_categoria()

    assert "Perifericos" in relatorio
    assert "1 unidade(s)" in relatorio
    assert "R$ 50.00" in relatorio

def test_prazo_estimado_frete_no_pedido(pedido_salvo):
    assert pedido_salvo.prazo_entrega_dias == 5
    assert "5 dias úteis" in pedido_salvo.gerar_resumo_nota()

    pedido_recarregado = Pedido.from_dict(pedido_salvo.to_dict())
    assert pedido_recarregado.prazo_entrega_dias == 5