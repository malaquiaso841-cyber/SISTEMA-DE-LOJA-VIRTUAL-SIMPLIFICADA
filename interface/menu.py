from datetime import datetime
import os

from models.carrinho import Carrinho
from models.cliente import Cliente
from models.cupom import Cupom
from models.endereco import Endereco
from models.frete import Frete
from models.pagamento import Pagamento
from models.pedido import Pedido
from models.produto import Produto
from services.cadastros import (
    adicionar_cliente,
    adicionar_produto,
    alterar_status_produto,
    atualizar_cliente,
    atualizar_produto,
    remover_cliente,
    remover_produto,
)
from services.dados import (
    carregar_clientes,
    carregar_cupons,
    carregar_pedidos,
    carregar_produtos,
    salvar_cupons,
    salvar_pedidos,
)
from services.operacoes_pedido import (
    alterar_status_pedido,
    cancelar_pedido as cancelar_pedido_servico,
    registrar_pagamento_pedido,
)
from services.relatorios import (
    gerar_relatorio_estoque,
    gerar_relatorio_faturamento_por_periodo,
    gerar_relatorio_pedidos,
    gerar_relatorio_pedidos_por_status,
    gerar_relatorio_top_produtos_e_ticket_medio,
    gerar_relatorio_vendas_por_categoria,
    gerar_relatorio_vendas_por_uf,
)


JANELA_CANCELAMENTO_HORAS = 24


def limpar_tela() -> None:
    """Limpa o terminal no Windows ou em outros sistemas."""
    os.system("cls" if os.name == "nt" else "clear")


def pausar() -> None:
    input("\nPressione Enter para continuar...")


def ler_float(mensagem: str) -> float:
    """Lê um decimal e repete somente este campo quando a entrada for inválida."""
    while True:
        texto = input(mensagem).strip().replace(",", ".")
        try:
            return float(texto)
        except ValueError:
            print("Entrada inválida. Digite um número, por exemplo: 29,90.")


def ler_int(mensagem: str) -> int:
    """Lê um inteiro e repete somente este campo quando a entrada for inválida."""
    while True:
        texto = input(mensagem).strip()
        try:
            return int(texto)
        except ValueError:
            print("Entrada inválida. Digite um número inteiro, por exemplo: 3.")


def perguntar_se_e_digital() -> bool:
    while True:
        resposta = input("O produto é digital? (s/n): ").strip().lower()

        if resposta in ("s", "sim"):
            return True

        if resposta in ("n", "não", "nao"):
            return False

        print("Resposta inválida. Digite 's' ou 'n'.")

# Produtos

def cadastrar_produto() -> None:
    print("\n=== Cadastro de produto ===")

    try:
        produto = Produto(
            sku=input("SKU: ").strip(),
            nome=input("Nome: ").strip(),
            categoria=input("Categoria: ").strip(),
            preco_unitario=ler_float("Preço unitário: R$ "),
            estoque=ler_int("Quantidade em estoque: "),
            digital=perguntar_se_e_digital(),
        )

        adicionar_produto(produto)
        print(f"Produto '{produto.nome}' cadastrado.")

    except (TypeError, ValueError) as erro:
        print(f"Não foi possível cadastrar o produto: {erro}")


def listar_produtos() -> None:
    produtos = carregar_produtos()

    print("\n=== Produtos cadastrados ===")

    if not produtos:
        print("Nenhum produto cadastrado.")
        return

    for produto in produtos:
        tipo = "Digital" if produto.digital else "Físico"
        status = "Ativo" if produto.ativo else "Inativo"
        print(
            f"{produto} | Tipo: {tipo} | "
            f"Categoria: {produto.categoria} | Status: {status}"
        )


def editar_produto() -> None:
    print("\n=== Atualizar produto ===")
    sku = input("SKU do produto: ").strip()

    print("Deixe um campo vazio para manter o valor atual.")
    nome = input("Novo nome: ").strip()
    categoria = input("Nova categoria: ").strip()
    preco_texto = input("Novo preço: R$ ").strip()
    estoque_texto = input("Novo estoque: ").strip()

    try:
        produto = atualizar_produto(
            sku,
            nome=nome or None,
            categoria=categoria or None,
            preco_unitario=(
                float(preco_texto.replace(",", "."))
                if preco_texto
                else None
            ),
            estoque=int(estoque_texto) if estoque_texto else None,
        )
        print(f"Produto '{produto.nome}' atualizado.")

    except (TypeError, ValueError) as erro:
        print(f"Não foi possível atualizar o produto: {erro}")


def alterar_status_de_produto() -> None:
    print("\n=== Ativar ou inativar produto ===")
    sku = input("SKU do produto: ").strip()
    resposta = input("Ativar o produto? (s/n): ").strip().lower()

    if resposta not in ("s", "sim", "n", "não", "nao"):
        print("Resposta inválida.")
        return

    ativo = resposta in ("s", "sim")

    try:
        produto = alterar_status_produto(sku, ativo)
        status = "ativado" if produto.ativo else "inativado"
        print(f"Produto '{produto.nome}' {status}.")

    except (TypeError, ValueError) as erro:
        print(f"Não foi possível alterar o produto: {erro}")


def excluir_produto() -> None:
    print("\n=== Remover produto ===")
    sku = input("SKU do produto: ").strip()

    try:
        produto = remover_produto(sku)
        print(f"Produto '{produto.nome}' removido.")

    except (TypeError, ValueError) as erro:
        print(f"Não foi possível remover o produto: {erro}")
        print("Produtos ativos precisam ser inativados antes da remoção.")

# Clientes

def cadastrar_cliente() -> None:
    print("\n=== Cadastro de cliente ===")

    try:
        id_cliente = input("ID do cliente: ").strip()
        clientes = carregar_clientes()

        if any(
            cliente.id_cliente.casefold() == id_cliente.casefold()
            for cliente in clientes
        ):
            print("Já existe um cliente com esse ID.")
            return

        endereco = Endereco(
            logradouro=input("Logradouro: ").strip(),
            numero=input("Número: ").strip(),
            complemento=input("Complemento (opcional): ").strip(),
            bairro=input("Bairro: ").strip(),
            cidade=input("Cidade: ").strip(),
            uf=input("UF: ").strip(),
            cep=input("CEP: ").strip(),
        )

        cliente = Cliente(
            id_cliente=id_cliente,
            nome=input("Nome: ").strip(),
            email=input("E-mail: ").strip(),
            cpf=input("CPF: ").strip(),
            enderecos=[endereco],
        )

        adicionar_cliente(cliente)
        print(f"Cliente '{cliente.nome}' cadastrado.")

    except (TypeError, ValueError) as erro:
        print(f"Não foi possível cadastrar o cliente: {erro}")


def listar_clientes() -> None:
    clientes = carregar_clientes()

    print("\n=== Clientes cadastrados ===")

    if not clientes:
        print("Nenhum cliente cadastrado.")
        return

    for cliente in clientes:
        print(f"{cliente.id_cliente} | {cliente.nome} | {cliente.email}")
        print(f"CPF: {cliente.cpf}")

        if cliente.enderecos:
            for endereco in cliente.enderecos:
                print(f"  Endereço: {endereco}")
        else:
            print("  Cliente sem endereço cadastrado.")


def editar_cliente() -> None:
    print("\n=== Atualizar cliente ===")
    id_cliente = input("ID do cliente: ").strip()

    print("Deixe um campo vazio para manter o valor atual.")
    nome = input("Novo nome: ").strip()
    email = input("Novo e-mail: ").strip()
    cpf = input("Novo CPF: ").strip()

    try:
        cliente = atualizar_cliente(
            id_cliente,
            nome=nome or None,
            email=email or None,
            cpf=cpf or None,
        )
        print(f"Cadastro de '{cliente.nome}' atualizado.")

    except (TypeError, ValueError) as erro:
        print(f"Não foi possível atualizar o cliente: {erro}")


def excluir_cliente() -> None:
    print("\n=== Remover cliente ===")
    id_cliente = input("ID do cliente: ").strip()

    try:
        cliente = remover_cliente(id_cliente)
        print(f"Cliente '{cliente.nome}' removido.")

    except (TypeError, ValueError) as erro:
        print(f"Não foi possível remover o cliente: {erro}")

# Pedidos

def escolher_cliente(clientes: list[Cliente]) -> Cliente | None:
    if not clientes:
        print("Cadastre um cliente antes de criar um pedido.")
        return None

    print("\n=== Escolha o cliente ===")
    for indice, cliente in enumerate(clientes, start=1):
        print(f"{indice}. {cliente.nome} — {cliente.email}")

    try:
        escolha = ler_int("Número do cliente: ")
        if 1 <= escolha <= len(clientes):
            return clientes[escolha - 1]
    except ValueError:
        pass

    print("Escolha inválida.")
    return None


def escolher_endereco(cliente: Cliente) -> Endereco | None:
    if not cliente.enderecos:
        print("Este cliente não possui endereço cadastrado.")
        return None

    print("\n=== Escolha o endereço de entrega ===")
    for indice, endereco in enumerate(cliente.enderecos, start=1):
        print(f"{indice}. {endereco}")

    try:
        escolha = ler_int("Número do endereço: ")
        if 1 <= escolha <= len(cliente.enderecos):
            return cliente.enderecos[escolha - 1]
    except ValueError:
        pass

    print("Escolha inválida.")
    return None


def gerar_id_pedido(pedidos: list[Pedido]) -> str:
    numeros = []

    for pedido in pedidos:
        parte_final = pedido.id.split("-")[-1]
        if parte_final.isdigit():
            numeros.append(int(parte_final))

    proximo_numero = max(numeros, default=0) + 1
    return f"PED-{proximo_numero:04d}"


def criar_pedido() -> None:
    clientes = carregar_clientes()
    produtos = carregar_produtos()
    cupons = carregar_cupons()
    pedidos = carregar_pedidos()

    cliente = escolher_cliente(clientes)
    if cliente is None:
        return

    endereco = escolher_endereco(cliente)
    if endereco is None:
        return

    produtos_ativos = [produto for produto in produtos if produto.ativo]
    if not produtos_ativos:
        print("Não há produtos ativos para adicionar ao pedido.")
        return

    carrinho = Carrinho(cliente)

    while True:
        print("\n=== Carrinho ===")
        print("1. Adicionar produto")
        print("2. Remover produto")
        print("3. Alterar quantidade")
        print("4. Ver carrinho")
        print("0. Finalizar pedido")

        opcao = input("Escolha uma opção: ").strip()

        try:
            if opcao == "1":
                print("\n=== Produtos disponíveis ===")
                for produto in produtos_ativos:
                    print(
                        f"{produto.sku} | {produto.nome} | "
                        f"R$ {produto.preco_unitario:.2f} | "
                        f"Estoque: {produto.estoque}"
                    )

                sku = input("SKU do produto: ").strip().upper()
                produto = next(
                    (item for item in produtos_ativos if item.sku == sku),
                    None,
                )

                if produto is None:
                    print("Produto não encontrado ou inativo.")
                    continue

                quantidade = ler_int("Quantidade: ")
                carrinho.adicionar_item(produto, quantidade)
                print("Produto adicionado ao carrinho.")

            elif opcao == "2":
                sku = input("SKU do produto a remover: ").strip().upper()
                carrinho.remover_item(sku)
                print("Produto removido.")

            elif opcao == "3":
                sku = input("SKU do produto: ").strip().upper()
                quantidade = ler_int(
                    "Nova quantidade (0 remove o produto): "
                )
                carrinho.atualizar_quantidade(sku, quantidade)
                print("Carrinho atualizado.")

            elif opcao == "4":
                if carrinho.esta_vazio:
                    print("O carrinho está vazio.")
                else:
                    for item in carrinho:
                        print(
                            f"{item.produto.sku} | {item.produto.nome} | "
                            f"Quantidade: {item.quantidade} | "
                            f"Subtotal: R$ {item.subtotal:.2f}"
                        )
                    print(f"Subtotal: R$ {carrinho.subtotal:.2f}")

            elif opcao == "0":
                break

            else:
                print("Opção inválida.")

        except (TypeError, ValueError) as erro:
            print(f"Não foi possível atualizar o carrinho: {erro}")

    if carrinho.esta_vazio:
        print("O carrinho está vazio; o pedido não foi criado.")
        return

    print("\n=== Resumo do carrinho ===")
    for item in carrinho:
        print(
            f"{item.produto.nome} | "
            f"Quantidade: {item.quantidade} | "
            f"Subtotal: R$ {item.subtotal:.2f}"
        )

    print(f"Subtotal: R$ {carrinho.subtotal:.2f}")

    codigo = input(
        "Código do cupom (Enter para pular): "
    ).strip().upper()

    cupom = None

    if codigo:
        cupom = next(
            (item for item in cupons if item.codigo == codigo),
            None,
        )

        if cupom is None:
            print("Cupom não encontrado.")
            return

    try:
        pedido = Pedido(
            id=gerar_id_pedido(pedidos),
            cliente=cliente,
            endereco_entrega=endereco,
        )

        pedido.fechar_pedido_com_carrinho(
            carrinho=carrinho,
            frete=Frete(),
            cupom=cupom,
        )

        # O estoque é baixado quando o pagamento total é confirmado.
        pedidos.append(pedido)
        salvar_pedidos(pedidos)

        if cupom is not None:
            salvar_cupons(cupons)

        print("\nPedido criado:")
        print(pedido.gerar_resumo_nota())

    except (TypeError, ValueError, FileNotFoundError) as erro:
        print(f"Não foi possível criar o pedido: {erro}")

def registrar_pagamento() -> None:
    pedidos = carregar_pedidos()
    pedidos_abertos = [
        pedido
        for pedido in pedidos
        if pedido.status == "aguardando_pagamento"
    ]

    if not pedidos_abertos:
        print("Não há pedidos aguardando pagamento.")
        return

    print("\n=== Pedidos aguardando pagamento ===")
    for pedido in pedidos_abertos:
        print(
            f"{pedido.id} — {pedido.cliente.nome} — "
            f"Total: R$ {pedido.calcular_total_pedido():.2f} — "
            f"Pago: R$ {sum(p.valor for p in pedido.pagamentos):.2f}"
        )

    id_pedido = input("\nID do pedido: ").strip().upper()

    pedido = next(
        (item for item in pedidos_abertos if item.id == id_pedido),
        None,
    )

    if pedido is None:
        print("Pedido não encontrado.")
        return

    try:
        forma = input("Forma (PIX, CREDITO, DEBITO, BOLETO): ").strip()
        valor = ler_float("Valor do pagamento: R$ ")

        pagamento = Pagamento(
            data=datetime.now(),
            forma=forma,
            valor=valor,
        )

        registrado = registrar_pagamento_pedido(
            pedido_id=pedido.id,
            pagamento=pagamento,
        )

        if not registrado:
            print("O pagamento não foi registrado.")
            return

        pedido_atualizado = next(
            (
                item for item in carregar_pedidos()
                if item.id == pedido.id
            ),
            None,
        )

        if pedido_atualizado is not None:
            print(
                "Pagamento registrado. "
                f"Status do pedido: {pedido_atualizado.status}"
            )

    except (TypeError, ValueError, FileNotFoundError) as erro:
        print(f"Não foi possível registrar o pagamento: {erro}")


def listar_pedidos() -> None:
    pedidos = carregar_pedidos()

    print("\n=== Pedidos ===")

    if not pedidos:
        print("Nenhum pedido cadastrado.")
        return

    for pedido in pedidos:
        print(pedido.gerar_resumo_nota())
        print("-" * 60)


def atualizar_status_pedido() -> None:
    pedidos = carregar_pedidos()

    if not pedidos:
        print("Nenhum pedido cadastrado.")
        return

    for pedido in pedidos:
        print(
            f"{pedido.id} | {pedido.cliente.nome} | "
            f"Status: {pedido.status}"
        )

    id_pedido = input("\nID do pedido: ").strip().upper()
    pedido = next((item for item in pedidos if item.id == id_pedido), None)

    if pedido is None:
        print("Pedido não encontrado.")
        return

    # O cancelamento tem uma opção própria para garantir o estorno do estoque.
    transicoes = pedido.TRANSICOES_PERMITIDAS[pedido.status] - {"cancelado"}

    if not transicoes:
        print(f"O pedido está em '{pedido.status}' e não pode avançar.")
        return

    opcoes = sorted(transicoes)
    print("\nPróximos status permitidos:")
    for indice, status in enumerate(opcoes, start=1):
        print(f"{indice}. {status}")

    try:
        escolha = ler_int("Escolha o novo status: ")

        if not 1 <= escolha <= len(opcoes):
            print("Escolha inválida.")
            return

        pedido_atualizado = alterar_status_pedido(
            pedido.id,
            opcoes[escolha - 1],
        )
        print(f"Status atualizado para '{pedido_atualizado.status}'.")

        if pedido_atualizado.codigo_rastreio:
            print(f"Código de rastreio: {pedido_atualizado.codigo_rastreio}")

    except (TypeError, ValueError, FileNotFoundError) as erro:
        print(f"Não foi possível atualizar o status: {erro}")


def cancelar_pedido() -> None:
    pedidos = carregar_pedidos()
    pedidos_cancelaveis = [
        pedido
        for pedido in pedidos
        if pedido.status in {"aguardando_pagamento", "pago"}
    ]

    if not pedidos_cancelaveis:
        print("Não há pedidos que possam ser cancelados.")
        return

    print("\n=== Pedidos que podem ser cancelados ===")
    for pedido in pedidos_cancelaveis:
        print(
            f"{pedido.id} | {pedido.cliente.nome} | "
            f"Status: {pedido.status} | "
            f"Total: R$ {pedido.calcular_total_pedido():.2f}"
        )

    id_pedido = input("\nID do pedido: ").strip().upper()

    try:
        cancelado = cancelar_pedido_servico(
           pedido_id=id_pedido,
        )

        if cancelado:
            print("Pedido cancelado. O estoque foi atualizado quando necessário.")
        else:
            print(
                "O pedido não foi cancelado. Ele pode estar fora da janela "
                "permitida ou não estar em um status cancelável."
            )

    except (TypeError, ValueError, FileNotFoundError) as erro:
        print(f"Não foi possível cancelar o pedido: {erro}")

# Relatórios

def menu_relatorios() -> None:
    while True:
        limpar_tela()
        print("=" * 48)
        print("                 RELATÓRIOS")
        print("=" * 48)
        print("1. Estoque")
        print("2. Pedidos")
        print("3. Pedidos por status")
        print("4. Faturamento por período")
        print("5. Produtos mais vendidos e ticket médio")
        print("6. Vendas por UF")
        print("7. Vendas por categoria")
        print("0. Voltar")
        print("-" * 48)

        opcao = input("Escolha uma opção: ").strip()

        try:
            if opcao == "1":
                print(gerar_relatorio_estoque())
                pausar()

            elif opcao == "2":
                print(gerar_relatorio_pedidos())
                pausar()

            elif opcao == "3":
                print(gerar_relatorio_pedidos_por_status())
                pausar()

            elif opcao == "4":
                inicio_texto = input(
                    "Data inicial (DD/MM/AAAA): "
                ).strip()
                fim_texto = input(
                    "Data final (DD/MM/AAAA): "
                ).strip()

                inicio = datetime.strptime(inicio_texto, "%d/%m/%Y")
                fim = datetime.strptime(fim_texto, "%d/%m/%Y")
                fim = fim.replace(hour=23, minute=59, second=59)

                print(
                    gerar_relatorio_faturamento_por_periodo(
                        inicio,
                        fim,
                    )
                )
                pausar()

            elif opcao == "5":
                limite_texto = input(
                    "Quantidade de produtos no ranking (Enter = configurado): "
                ).strip()

                limite = int(limite_texto) if limite_texto else None

                print(gerar_relatorio_top_produtos_e_ticket_medio(limite))

            elif opcao == "6":
                print(gerar_relatorio_vendas_por_uf())
                pausar()

            elif opcao == "7":
                print(gerar_relatorio_vendas_por_categoria())
                pausar()

            elif opcao == "0":
                return

            else:
                print("Opção inválida.")
                pausar()

        except (TypeError, ValueError) as erro:
            print(f"Não foi possível gerar o relatório: {erro}")
            pausar()

# Menus

def mostrar_menu() -> None:
    print("=" * 52)
    print("                  LOJA VIRTUAL")
    print("=" * 52)
    print("\nPRODUTOS")
    print("  1. Cadastrar produto")
    print("  2. Listar produtos")
    print("  3. Atualizar produto")
    print("  4. Ativar ou inativar produto")
    print("  5. Remover produto")
    print("\nCLIENTES")
    print("  6. Cadastrar cliente")
    print("  7. Listar clientes")
    print("  8. Atualizar cliente")
    print("  9. Remover cliente")
    print("\nPEDIDOS")
    print(" 10. Criar pedido")
    print(" 11. Registrar pagamento")
    print(" 12. Consultar pedidos")
    print(" 13. Atualizar status do pedido")
    print(" 14. Cancelar pedido")
    print("\nRELATÓRIOS")
    print(" 15. Consultar relatórios")
    print("\n  0. Sair")
    print("-" * 52)


def menu() -> None:
    while True:
        limpar_tela()
        mostrar_menu()
        opcao = input("Escolha uma opção: ").strip()

        try:
            if opcao == "1":
                cadastrar_produto()
            elif opcao == "2":
                listar_produtos()
            elif opcao == "3":
                editar_produto()
            elif opcao == "4":
                alterar_status_de_produto()
            elif opcao == "5":
                excluir_produto()
            elif opcao == "6":
                cadastrar_cliente()
            elif opcao == "7":
                listar_clientes()
            elif opcao == "8":
                editar_cliente()
            elif opcao == "9":
                excluir_cliente()
            elif opcao == "10":
                criar_pedido()
            elif opcao == "11":
                registrar_pagamento()
            elif opcao == "12":
                listar_pedidos()
            elif opcao == "13":
                atualizar_status_pedido()
            elif opcao == "14":
                cancelar_pedido()
            elif opcao == "15":
                menu_relatorios()
            elif opcao == "0":
                print("Até logo!")
                return
            else:
                print("Opção inválida. Escolha um número do menu.")

        except (TypeError, ValueError, FileNotFoundError) as erro:
            print(f"Não foi possível concluir a operação: {erro}")

        pausar()


if __name__ == "__main__":
    menu()