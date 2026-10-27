from models.pagamento import Pagamento
from models.pedido import Pedido
from services.configuracao import carregar_configuracoes
from services.dados import (
    carregar_pedidos,
    carregar_produtos,
    salvar_pedidos,
    salvar_produtos,
)


def _buscar_pedido(pedido_id: str, pedidos: list[Pedido]) -> Pedido:
    if not isinstance(pedido_id, str) or not pedido_id.strip():
        raise ValueError("O ID do pedido não pode ser vazio")

    id_normalizado = pedido_id.strip().upper()

    pedido = next(
        (item for item in pedidos if item.id == id_normalizado),
        None,
    )

    if pedido is None:
        raise ValueError(f"Pedido {id_normalizado} não encontrado")

    return pedido


def registrar_pagamento_pedido(
    pedido_id: str,
    pagamento: Pagamento,
) -> bool:
    pedidos = carregar_pedidos()
    produtos = carregar_produtos()
    pedido = _buscar_pedido(pedido_id, pedidos)

    registrado = pedido.registrar_pagamento(
        pagamento,
        produtos=produtos,
    )

    if registrado:
        salvar_produtos(produtos)
        salvar_pedidos(pedidos)

    return registrado


def cancelar_pedido(
    pedido_id: str,
    janela_horas: int | None = None,
) -> bool:
    if janela_horas is None:
        configuracoes = carregar_configuracoes()
        janela_horas = configuracoes["politica_cancelamento"]["janela_horas"]

    pedidos = carregar_pedidos()
    produtos = carregar_produtos()
    pedido = _buscar_pedido(pedido_id, pedidos)

    cancelado = pedido.cancelar_pedido(
        janela_horas=janela_horas,
        produtos=produtos,
    )

    if cancelado:
        salvar_produtos(produtos)
        salvar_pedidos(pedidos)

    return cancelado

def alterar_status_pedido(
    pedido_id: str,
    novo_status: str,
) -> Pedido:
    pedidos = carregar_pedidos()
    pedido = _buscar_pedido(pedido_id, pedidos)

    pedido.alterar_status(novo_status)
    salvar_pedidos(pedidos)

    return pedido
