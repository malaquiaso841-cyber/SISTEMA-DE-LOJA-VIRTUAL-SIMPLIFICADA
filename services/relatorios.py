from datetime import datetime

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