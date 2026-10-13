import json
from pathlib import Path

from models.cliente import Cliente
from models.cupom import Cupom
from models.pedido import Pedido
from models.produto import Produto


PASTA_DADOS = Path(__file__).resolve().parent.parent / "data"


def _salvar_lista(nome_arquivo: str, objetos: list) -> None:
    PASTA_DADOS.mkdir(parents=True, exist_ok=True)
    caminho = PASTA_DADOS / nome_arquivo

    dados = []

    for objeto in objetos:
        if not hasattr(objeto, "to_dict"):
            raise TypeError(
                f"{type(objeto).__name__} precisa ter o método to_dict()"
            )

        dados.append(objeto.to_dict())

    with caminho.open("w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, ensure_ascii=False, indent=4)


def _carregar_lista(nome_arquivo: str, classe) -> list:
    caminho = PASTA_DADOS / nome_arquivo

    if not caminho.exists():
        return []

    try:
        with caminho.open("r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
    except json.JSONDecodeError as erro:
        raise ValueError(
            f"O arquivo {nome_arquivo} contém JSON inválido"
        ) from erro

    if not isinstance(dados, list):
        raise ValueError(
            f"O conteúdo de {nome_arquivo} deve ser uma lista JSON"
        )

    return [classe.from_dict(item) for item in dados]


def salvar_produtos(produtos: list[Produto]) -> None:
    _salvar_lista("produtos.json", produtos)


def carregar_produtos() -> list[Produto]:
    return _carregar_lista("produtos.json", Produto)


def salvar_clientes(clientes: list[Cliente]) -> None:
    _salvar_lista("clientes.json", clientes)


def carregar_clientes() -> list[Cliente]:
    return _carregar_lista("clientes.json", Cliente)


def salvar_pedidos(pedidos: list[Pedido]) -> None:
    _salvar_lista("pedidos.json", pedidos)


def carregar_pedidos() -> list[Pedido]:
    return _carregar_lista("pedidos.json", Pedido)


def salvar_cupons(cupons: list[Cupom]) -> None:
    _salvar_lista("cupons.json", cupons)


def carregar_cupons() -> list[Cupom]:
    return _carregar_lista("cupons.json", Cupom)