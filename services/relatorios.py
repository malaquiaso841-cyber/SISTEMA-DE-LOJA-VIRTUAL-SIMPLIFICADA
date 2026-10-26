from datetime import datetime
from collections import Counter
from services.configuracao import carregar_configuracoes

from services.dados import (
    carregar_pedidos,
    carregar_produtos,
)


def gerar_relatorio_estoque() -> str:
    produtos = carregar_produtos()

    if not produtos:
        return "Nenhum produto cadastrado."

    linhas = [
        "RELATÓRIO DE ESTOQUE",
        f"Gerado em: {datetime.now():%d/%m/%Y %H:%M}",
        "",
    ]

    valor_total_estoque = 0.0
    quantidade_total = 0

    for produto in produtos:
        valor_produtos = produto.preco_unitario * produto.estoque
        valor_total_estoque += valor_produtos
        quantidade_total += produto.estoque

        status = "Ativo" if produto.ativo else "Inativo"

        linhas.append(
            f"SKU: {produto.sku} | "
            f"Produto: {produto.nome} | "
            f"Estoque: {produto.estoque} | "
            f"Preço: R$ {produto.preco_unitario:.2f} | "
            f"Status: {status}"
        )

    linhas.extend([
        "",
        f"Unidades em estoque: {quantidade_total}",
        f"Valor estimado do estoque: R$ {valor_total_estoque:.2f}",
    ])

    return "\n".join(linhas)


def gerar_relatorio_pedidos() -> str:
    pedidos = carregar_pedidos()

    if not pedidos:
        return "Nenhum pedido cadastrado."

    linhas = [
        "RELATÓRIO DE PEDIDOS",
        f"Gerado em: {datetime.now():%d/%m/%Y %H:%M}",
        "",
    ]

    for pedido in pedidos:
        linhas.append(
            f"Pedido: {pedido.id} | "
            f"Cliente: {pedido.cliente.nome} | "
            f"Status: {pedido.status} | "
            f"Data: {pedido.data_criacao:%d/%m/%Y %H:%M} | "
            f"Total: R$ {pedido.calcular_total_pedido():.2f}"
        )

    return "\n".join(linhas)


def gerar_relatorio_vendas() -> str:
    pedidos = carregar_pedidos()

    # Pedidos aguardando pagamento e cancelados não contam como vendas concluídas.
    pedidos_concluidos = [
        pedido
        for pedido in pedidos
        if pedido.status in {"pago", "enviado", "entregue"}
    ]

    if not pedidos_concluidos:
        return "Nenhuma venda concluída."

    valor_total_vendas = sum(
        pedido.calcular_total_pedido()
        for pedido in pedidos_concluidos
    )

    linhas = [
        "RELATÓRIO DE VENDAS",
        f"Gerado em: {datetime.now():%d/%m/%Y %H:%M}",
        "",
        f"Vendas concluídas: {len(pedidos_concluidos)}",
        f"Valor total vendido: R$ {valor_total_vendas:.2f}",
        "",
        "Pedidos:",
    ]

    for pedido in pedidos_concluidos:
        linhas.append(
            f"Pedido: {pedido.id} | "
            f"Cliente: {pedido.cliente.nome} | "
            f"Status: {pedido.status} | "
            f"Total: R$ {pedido.calcular_total_pedido():.2f}"
        )
        
    return "\n".join(linhas)

def gerar_relatorio_pedidos_por_status() -> str:
    pedidos = carregar_pedidos()

    if not pedidos:
        return "Nenhum pedido cadastrado."

    status_disponiveis = [
        "aguardando_pagamento",
        "pago",
        "enviado",
        "entregue",
        "cancelado",
    ]
    total_pedidos = len(pedidos)

    linhas = [
        "RELATÓRIO DE PEDIDOS POR STATUS",
        f"Total de pedidos: {total_pedidos}",
        "",
    ]

    for status in status_disponiveis:
        quantidade = sum(
            1 for pedido in pedidos
            if pedido.status == status
        )
        percentual = quantidade / total_pedidos * 100
        nome_status = status.replace("_", " ").title()

        linhas.append(
            f"{nome_status}: {quantidade} "
            f"({percentual:.1f}%)"
        )
        
    return "\n".join(linhas)

def gerar_relatorio_faturamento_por_periodo(
    data_inicio: datetime,
    data_fim: datetime,
) -> str:
    if not isinstance(data_inicio, datetime):
        raise TypeError("A data inicial deve ser um objeto datetime")

    if not isinstance(data_fim, datetime):
        raise TypeError("A data final deve ser um objeto datetime")

    if data_inicio > data_fim:
        raise ValueError("A data inicial não pode ser posterior à data final")

    pedidos = carregar_pedidos()
    status_faturados = {"pago", "enviado", "entregue"}

    pagamentos_no_periodo = []
    pedidos_no_periodo = set()

    for pedido in pedidos:
        if pedido.status not in status_faturados:
            continue

        for pagamento in pedido.pagamentos:
            if data_inicio <= pagamento.data <= data_fim:
                pagamentos_no_periodo.append(pagamento)
                pedidos_no_periodo.add(pedido.id)

    faturamento = sum(pagamento.valor for pagamento in pagamentos_no_periodo)

    return "\n".join([
        "RELATÓRIO DE FATURAMENTO POR PERÍODO",
        f"De: {data_inicio:%d/%m/%Y %H:%M}",
        f"Até: {data_fim:%d/%m/%Y %H:%M}",
        f"Pedidos faturados no período: {len(pedidos_no_periodo)}",
        f"Pagamentos registrados no período: {len(pagamentos_no_periodo)}",
        f"Faturamento total: R$ {faturamento:.2f}",
    ])

def gerar_relatorio_top_produtos_e_ticket_medio(
    limite: int | None = None,
) -> str:
    if limite is None:
        configuracoes = carregar_configuracoes()
        limite = configuracoes["relatorios"]["top_n_produtos"]
        
    if isinstance(limite, bool) or not isinstance(limite, int):
        raise TypeError("O limite deve ser um número inteiro")

    if limite < 1:
        raise ValueError("O limite deve ser maior que zero")

    pedidos = carregar_pedidos()
    pedidos_concluidos = [
        pedido
        for pedido in pedidos
        if pedido.status in {"pago", "enviado", "entregue"}
    ]

    if not pedidos_concluidos:
        return "Não há vendas concluídas para gerar o relatório."

    unidades_por_sku = Counter()

    for pedido in pedidos_concluidos:
        for item in pedido.itens:
            unidades_por_sku[item.sku] += item.quantidade

    faturamento_total = sum(
        pedido.calcular_total_pedido()
        for pedido in pedidos_concluidos
    )
    ticket_medio = faturamento_total / len(pedidos_concluidos)

    produtos_mais_vendidos = sorted(
        unidades_por_sku.items(),
        key=lambda produto: (-produto[1], produto[0]),
    )[:limite]

    linhas = [
        "RELATÓRIO DE PRODUTOS MAIS VENDIDOS E TICKET MÉDIO",
        f"Vendas concluídas: {len(pedidos_concluidos)}",
        f"Ticket médio: R$ {ticket_medio:.2f}",
        "",
        f"Produtos mais vendidos (até {limite}):",
    ]

    for posicao, (sku, quantidade) in enumerate(
        produtos_mais_vendidos,
        start=1,
    ):
        linhas.append(
            f"{posicao}. SKU: {sku} | Unidades vendidas: {quantidade}"
        )

    return "\n".join(linhas)

def gerar_relatorio_vendas_por_uf() -> str:
    pedidos = carregar_pedidos()
    pedidos_concluidos = [
        pedido
        for pedido in pedidos
        if pedido.status in {"pago", "enviado", "entregue"}
    ]

    if not pedidos_concluidos:
        return "Não há vendas concluídas para gerar o relatório."

    vendas_por_uf = {}

    for pedido in pedidos_concluidos:
        uf = pedido.endereco_entrega.uf

        if uf not in vendas_por_uf:
            vendas_por_uf[uf] = {
                "pedidos": 0,
                "faturamento": 0.0,
            }

        vendas_por_uf[uf]["pedidos"] += 1
        vendas_por_uf[uf]["faturamento"] += pedido.calcular_total_pedido()

    linhas = [
        "RELATÓRIO DE VENDAS POR UF",
        f"Vendas concluídas: {len(pedidos_concluidos)}",
        "",
    ]

    for uf, dados_uf in sorted(vendas_por_uf.items()):
        linhas.append(
            f"{uf}: {dados_uf['pedidos']} pedido(s) | "
            f"Faturamento: R$ {dados_uf['faturamento']:.2f}"
        )

    return "\n".join(linhas)

def gerar_relatorio_vendas_por_categoria() -> str:
    pedidos = carregar_pedidos()

    pedidos_concluidos = [
        pedido
        for pedido in pedidos
        if pedido.status in {"pago", "enviado", "entregue"}
    ]

    if not pedidos_concluidos:
        return "Não há vendas concluídas para gerar o relatório."

    vendas_por_categoria = {}

    for pedido in pedidos_concluidos:
        for item in pedido.itens:
            categoria = item.categoria

            if categoria not in vendas_por_categoria:
                vendas_por_categoria[categoria] = {
                    "unidades": 0,
                    "valor_bruto": 0.0,
                }

            vendas_por_categoria[categoria]["unidades"] += item.quantidade
            vendas_por_categoria[categoria]["valor_bruto"] += item.subtotal

    linhas = [
        "RELATÓRIO DE VENDAS POR CATEGORIA",
        "",
    ]

    for categoria, dados in sorted(vendas_por_categoria.items()):
        linhas.append(
            f"{categoria}: "
            f"{dados['unidades']} unidade(s) | "
            f"Valor bruto: R$ {dados['valor_bruto']:.2f}"
        )

    return "\n".join(linhas)