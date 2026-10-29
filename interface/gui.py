from datetime import datetime
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

from models.carrinho import Carrinho
from models.cliente import Cliente
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
    cancelar_pedido,
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


class LojaGUI:
    def __init__(self, raiz: tk.Tk):
        self.raiz = raiz
        self.raiz.title("Loja Virtual Simplificada")
        self.raiz.geometry("1050x680")
        self.raiz.minsize(850, 560)

        estilo = ttk.Style()
        try:
            estilo.theme_use("clam")
        except tk.TclError:
            pass

        topo = ttk.Frame(raiz, padding=(18, 14))
        topo.pack(fill="x")
        ttk.Label(
            topo,
            text="Loja Virtual Simplificada",
            font=("Segoe UI", 19, "bold"),
        ).pack(side="left")
        ttk.Button(topo, text="Atualizar dados", command=self.atualizar_tudo).pack(side="right")

        self.abas = ttk.Notebook(raiz)
        self.abas.pack(fill="both", expand=True, padx=14, pady=(0, 14))

        self.aba_produtos = ttk.Frame(self.abas, padding=12)
        self.aba_clientes = ttk.Frame(self.abas, padding=12)
        self.aba_pedidos = ttk.Frame(self.abas, padding=12)
        self.aba_relatorios = ttk.Frame(self.abas, padding=12)

        self.abas.add(self.aba_produtos, text="Produtos")
        self.abas.add(self.aba_clientes, text="Clientes")
        self.abas.add(self.aba_pedidos, text="Pedidos")
        self.abas.add(self.aba_relatorios, text="Relatórios")

        self._montar_aba_produtos()
        self._montar_aba_clientes()
        self._montar_aba_pedidos()
        self._montar_aba_relatorios()
        self.atualizar_tudo()

    def _proteger(self, acao):
        try:
            resultado = acao()
            self.atualizar_tudo()
            return resultado
        except (TypeError, ValueError, OSError, KeyError) as erro:
            messagebox.showerror("Não foi possível concluir", str(erro), parent=self.raiz)
            return None

    def _arvore(self, pai, colunas, larguras):
        moldura = ttk.Frame(pai)
        moldura.pack(fill="both", expand=True, pady=8)
        arvore = ttk.Treeview(moldura, columns=colunas, show="headings", height=16)
        for coluna, largura in zip(colunas, larguras):
            arvore.heading(coluna, text=coluna.replace("_", " ").title())
            arvore.column(coluna, width=largura, anchor="w")
        barra = ttk.Scrollbar(moldura, orient="vertical", command=arvore.yview)
        arvore.configure(yscrollcommand=barra.set)
        arvore.pack(side="left", fill="both", expand=True)
        barra.pack(side="right", fill="y")
        return arvore

    def _selecionado(self, arvore):
        selecao = arvore.selection()
        if not selecao:
            messagebox.showinfo("Selecione um registro", "Selecione uma linha na tabela.", parent=self.raiz)
            return None
        return arvore.item(selecao[0], "values")

    def _formulario(self, titulo, campos, valores=None):
        valores = valores or {}
        janela = tk.Toplevel(self.raiz)
        janela.title(titulo)
        janela.transient(self.raiz)
        janela.grab_set()
        janela.resizable(False, False)
        entradas = {}

        for linha, (chave, rotulo, escolhas) in enumerate(campos):
            ttk.Label(janela, text=rotulo).grid(row=linha, column=0, sticky="w", padx=12, pady=6)
            if escolhas:
                entrada = ttk.Combobox(janela, values=escolhas, state="readonly", width=34)
                entrada.set(str(valores.get(chave, escolhas[0])))
            else:
                entrada = ttk.Entry(janela, width=37)
                entrada.insert(0, str(valores.get(chave, "")))
            entrada.grid(row=linha, column=1, sticky="ew", padx=12, pady=6)
            entradas[chave] = entrada

        resultado = {"dados": None}

        def confirmar():
            resultado["dados"] = {chave: campo.get().strip() for chave, campo in entradas.items()}
            janela.destroy()

        botoes = ttk.Frame(janela, padding=10)
        botoes.grid(row=len(campos), column=0, columnspan=2, sticky="e")
        ttk.Button(botoes, text="Cancelar", command=janela.destroy).pack(side="right", padx=5)
        ttk.Button(botoes, text="Salvar", command=confirmar).pack(side="right", padx=5)
        janela.wait_window()
        return resultado["dados"]

    # Produtos
    def _montar_aba_produtos(self):
        ttk.Label(self.aba_produtos, text="Catálogo de produtos", font=("Segoe UI", 14, "bold")).pack(anchor="w")
        self.tabela_produtos = self._arvore(
            self.aba_produtos,
            ("sku", "nome", "categoria", "preco", "estoque", "tipo", "status"),
            (110, 210, 130, 100, 80, 90, 90),
        )
        botoes = ttk.Frame(self.aba_produtos)
        botoes.pack(fill="x")
        for texto, comando in (
            ("Cadastrar", self.cadastrar_produto),
            ("Editar", self.editar_produto),
            ("Ativar/Inativar", self.alternar_produto),
            ("Remover", self.excluir_produto),
        ):
            ttk.Button(botoes, text=texto, command=comando).pack(side="left", padx=4)

    def atualizar_produtos(self):
        self.tabela_produtos.delete(*self.tabela_produtos.get_children())
        for p in carregar_produtos():
            self.tabela_produtos.insert("", "end", values=(
                p.sku, p.nome, p.categoria, f"R$ {p.preco_unitario:.2f}",
                p.estoque, "Digital" if p.digital else "Físico",
                "Ativo" if p.ativo else "Inativo",
            ))

    def cadastrar_produto(self):
        dados = self._formulario("Cadastrar produto", [
            ("sku", "SKU", None), ("nome", "Nome", None),
            ("categoria", "Categoria", None), ("preco", "Preço unitário", None),
            ("estoque", "Estoque", None), ("tipo", "Tipo", ["Físico", "Digital"]),
        ])
        if not dados:
            return
        def salvar():
            produto = Produto(
                sku=dados["sku"], nome=dados["nome"], categoria=dados["categoria"],
                preco_unitario=float(dados["preco"].replace(",", ".")),
                estoque=int(dados["estoque"]), digital=dados["tipo"] == "Digital",
            )
            adicionar_produto(produto)
            messagebox.showinfo("Produto", "Produto cadastrado.", parent=self.raiz)
        self._proteger(salvar)

    def editar_produto(self):
        valores = self._selecionado(self.tabela_produtos)
        if not valores:
            return
        p = next((x for x in carregar_produtos() if x.sku == valores[0]), None)
        if p is None:
            return
        dados = self._formulario("Atualizar produto", [
            ("nome", "Nome", None), ("categoria", "Categoria", None),
            ("preco", "Preço unitário", None), ("estoque", "Estoque", None),
        ], {"nome": p.nome, "categoria": p.categoria, "preco": p.preco_unitario, "estoque": p.estoque})
        if not dados:
            return
        def salvar():
            atualizar_produto(
                p.sku, nome=dados["nome"], categoria=dados["categoria"],
                preco_unitario=float(dados["preco"].replace(",", ".")),
                estoque=int(dados["estoque"]),
            )
            messagebox.showinfo("Produto", "Produto atualizado.", parent=self.raiz)
        self._proteger(salvar)

    def alternar_produto(self):
        valores = self._selecionado(self.tabela_produtos)
        if not valores:
            return
        p = next((x for x in carregar_produtos() if x.sku == valores[0]), None)
        if p is None:
            return
        self._proteger(lambda: alterar_status_produto(p.sku, not p.ativo))

    def excluir_produto(self):
        valores = self._selecionado(self.tabela_produtos)
        if not valores:
            return
        if not messagebox.askyesno("Remover produto", "Remover o produto selecionado?", parent=self.raiz):
            return
        self._proteger(lambda: remover_produto(valores[0]))

    # Clientes
    def _montar_aba_clientes(self):
        ttk.Label(self.aba_clientes, text="Cadastro de clientes", font=("Segoe UI", 14, "bold")).pack(anchor="w")
        self.tabela_clientes = self._arvore(
            self.aba_clientes, ("id", "nome", "email", "cpf", "enderecos"),
            (110, 190, 220, 130, 260),
        )
        botoes = ttk.Frame(self.aba_clientes)
        botoes.pack(fill="x")
        for texto, comando in (
            ("Cadastrar", self.cadastrar_cliente),
            ("Editar", self.editar_cliente),
            ("Remover", self.excluir_cliente),
        ):
            ttk.Button(botoes, text=texto, command=comando).pack(side="left", padx=4)

    def atualizar_clientes(self):
        self.tabela_clientes.delete(*self.tabela_clientes.get_children())
        for c in carregar_clientes():
            self.tabela_clientes.insert("", "end", values=(
                c.id_cliente, c.nome, c.email, c.cpf,
                f"{len(c.enderecos)} endereço(s)",
            ))

    def cadastrar_cliente(self):
        campos = [
            ("id", "ID", None), ("nome", "Nome", None),
            ("email", "E-mail", None), ("cpf", "CPF", None),
            ("logradouro", "Logradouro", None), ("numero", "Número", None),
            ("complemento", "Complemento", None), ("bairro", "Bairro", None),
            ("cidade", "Cidade", None), ("uf", "UF", None), ("cep", "CEP", None),
        ]
        dados = self._formulario("Cadastrar cliente e endereço", campos)
        if not dados:
            return
        def salvar():
            endereco = Endereco(
                logradouro=dados["logradouro"], numero=dados["numero"],
                complemento=dados["complemento"], bairro=dados["bairro"],
                cidade=dados["cidade"], uf=dados["uf"], cep=dados["cep"],
            )
            cliente = Cliente(
                id_cliente=dados["id"], nome=dados["nome"], email=dados["email"],
                cpf=dados["cpf"], enderecos=[endereco],
            )
            adicionar_cliente(cliente)
            messagebox.showinfo("Cliente", "Cliente cadastrado.", parent=self.raiz)
        self._proteger(salvar)

    def editar_cliente(self):
        valores = self._selecionado(self.tabela_clientes)
        if not valores:
            return
        c = next((x for x in carregar_clientes() if x.id_cliente == valores[0]), None)
        if c is None:
            return
        dados = self._formulario("Atualizar cliente", [
            ("nome", "Nome", None), ("email", "E-mail", None), ("cpf", "CPF", None),
        ], {"nome": c.nome, "email": c.email, "cpf": c.cpf})
        if not dados:
            return
        self._proteger(lambda: atualizar_cliente(
            c.id_cliente, nome=dados["nome"], email=dados["email"], cpf=dados["cpf"],
        ))

    def excluir_cliente(self):
        valores = self._selecionado(self.tabela_clientes)
        if not valores:
            return
        if messagebox.askyesno("Remover cliente", "Remover o cliente selecionado?", parent=self.raiz):
            self._proteger(lambda: remover_cliente(valores[0]))

    # Pedidos
    def _montar_aba_pedidos(self):
        ttk.Label(self.aba_pedidos, text="Pedidos e pagamentos", font=("Segoe UI", 14, "bold")).pack(anchor="w")
        self.tabela_pedidos = self._arvore(
            self.aba_pedidos, ("id", "cliente", "status", "data", "total", "pago"),
            (130, 190, 150, 160, 120, 120),
        )
        botoes = ttk.Frame(self.aba_pedidos)
        botoes.pack(fill="x")
        for texto, comando in (
            ("Criar pedido", self.criar_pedido),
            ("Registrar pagamento", self.registrar_pagamento),
            ("Avançar status", self.avancar_status),
            ("Cancelar pedido", self.cancelar_pedido),
            ("Ver resumo", self.ver_resumo_pedido),
        ):
            ttk.Button(botoes, text=texto, command=comando).pack(side="left", padx=3)

    def atualizar_pedidos(self):
        self.tabela_pedidos.delete(*self.tabela_pedidos.get_children())
        for p in carregar_pedidos():
            pago = sum(x.valor for x in p.pagamentos)
            self.tabela_pedidos.insert("", "end", values=(
                p.id, p.cliente.nome, p.status,
                p.data_criacao.strftime("%d/%m/%Y %H:%M"),
                f"R$ {p.calcular_total_pedido():.2f}", f"R$ {pago:.2f}",
            ))

    def _pedido_selecionado(self):
        valores = self._selecionado(self.tabela_pedidos)
        if not valores:
            return None
        return next((p for p in carregar_pedidos() if p.id == valores[0]), None)

    def criar_pedido(self):
        clientes = carregar_clientes()
        produtos = [p for p in carregar_produtos() if p.ativo]
        cupons = carregar_cupons()
        pedidos = carregar_pedidos()
        if not clientes or not produtos:
            messagebox.showinfo("Pedido", "Cadastre pelo menos um cliente e um produto ativo.", parent=self.raiz)
            return

        janela = tk.Toplevel(self.raiz)
        janela.title("Criar pedido")
        janela.transient(self.raiz)
        janela.grab_set()
        janela.geometry("760x560")

        ttk.Label(janela, text="Cliente").grid(row=0, column=0, padx=10, pady=8, sticky="w")
        cliente_var = tk.StringVar()
        combo_cliente = ttk.Combobox(
            janela, textvariable=cliente_var, state="readonly", width=55,
            values=[f"{c.id_cliente} — {c.nome}" for c in clientes],
        )
        combo_cliente.grid(row=0, column=1, padx=10, pady=8, sticky="ew")
        combo_cliente.current(0)

        ttk.Label(janela, text="Endereço").grid(row=1, column=0, padx=10, pady=8, sticky="w")
        endereco_var = tk.StringVar()
        combo_endereco = ttk.Combobox(janela, textvariable=endereco_var, state="readonly", width=55)
        combo_endereco.grid(row=1, column=1, padx=10, pady=8, sticky="ew")

        def atualizar_enderecos(_evento=None):
            cliente = clientes[combo_cliente.current()]
            enderecos = [str(e) for e in cliente.enderecos]
            combo_endereco["values"] = enderecos
            combo_endereco.current(0 if enderecos else -1)
        combo_cliente.bind("<<ComboboxSelected>>", atualizar_enderecos)
        atualizar_enderecos()

        ttk.Label(janela, text="Produto").grid(row=2, column=0, padx=10, pady=8, sticky="w")
        produto_var = tk.StringVar()
        combo_produto = ttk.Combobox(
            janela, textvariable=produto_var, state="readonly", width=55,
            values=[f"{p.sku} — {p.nome} (estoque {p.estoque})" for p in produtos],
        )
        combo_produto.grid(row=2, column=1, padx=10, pady=8, sticky="ew")
        combo_produto.current(0)

        ttk.Label(janela, text="Quantidade").grid(row=3, column=0, padx=10, pady=8, sticky="w")
        qtd_var = tk.StringVar(value="1")
        ttk.Entry(janela, textvariable=qtd_var, width=12).grid(row=3, column=1, padx=10, pady=8, sticky="w")

        tabela = ttk.Treeview(janela, columns=("sku", "produto", "qtd", "subtotal"), show="headings", height=9)
        for col, width in (("sku", 100), ("produto", 260), ("qtd", 80), ("subtotal", 120)):
            tabela.heading(col, text=col.title())
            tabela.column(col, width=width)
        tabela.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        cupom_var = tk.StringVar()
        ttk.Label(janela, text="Cupom (opcional)").grid(row=5, column=0, padx=10, pady=8, sticky="w")
        ttk.Entry(janela, textvariable=cupom_var, width=30).grid(row=5, column=1, padx=10, pady=8, sticky="w")

        carrinho = Carrinho(clientes[0])
        subtotal_var = tk.StringVar(value="Subtotal: R$ 0,00")
        ttk.Label(janela, textvariable=subtotal_var, font=("Segoe UI", 11, "bold")).grid(row=6, column=0, padx=10, pady=8, sticky="w")

        def adicionar_item():
            try:
                idx = combo_produto.current()
                if idx < 0:
                    raise ValueError("Selecione um produto.")
                produto = produtos[idx]
                carrinho.adicionar_item(produto, int(qtd_var.get()))
                tabela.delete(*tabela.get_children())
                for item in carrinho:
                    tabela.insert("", "end", values=(
                        item.produto.sku, item.produto.nome, item.quantidade,
                        f"R$ {item.subtotal:.2f}",
                    ))
                subtotal_var.set(f"Subtotal: R$ {carrinho.subtotal:.2f}")
            except (TypeError, ValueError) as erro:
                messagebox.showerror("Carrinho", str(erro), parent=janela)

        ttk.Button(janela, text="Adicionar produto", command=adicionar_item).grid(row=3, column=1, padx=150, pady=8, sticky="w")

        def salvar_pedido():
            if carrinho.esta_vazio:
                messagebox.showerror("Pedido", "Adicione pelo menos um produto.", parent=janela)
                return
            cliente = clientes[combo_cliente.current()]
            if not cliente.enderecos:
                messagebox.showerror("Pedido", "O cliente não possui endereço cadastrado.", parent=janela)
                return
            endereco = cliente.enderecos[combo_endereco.current()]
            carrinho.cliente = cliente
            codigo = cupom_var.get().strip().upper()
            cupom = next((c for c in cupons if c.codigo == codigo), None) if codigo else None
            if codigo and cupom is None:
                messagebox.showerror("Cupom", "Cupom não encontrado.", parent=janela)
                return

            try:
                pedido = Pedido(
                    id=self._gerar_id_pedido(pedidos),
                    cliente=cliente,
                    endereco_entrega=endereco,
                )
                pedido.fechar_pedido_com_carrinho(
                    carrinho=carrinho, frete=Frete(), cupom=cupom,
                )
                pedidos.append(pedido)
                salvar_pedidos(pedidos)
                if cupom is not None:
                    salvar_cupons(cupons)
                messagebox.showinfo("Pedido criado", pedido.gerar_resumo_nota(), parent=janela)
                janela.destroy()
                self.atualizar_tudo()
            except (TypeError, ValueError, OSError, KeyError) as erro:
                messagebox.showerror("Pedido", str(erro), parent=janela)

        botoes = ttk.Frame(janela)
        botoes.grid(row=7, column=0, columnspan=2, sticky="e", padx=10, pady=12)
        ttk.Button(botoes, text="Fechar pedido", command=salvar_pedido).pack(side="right", padx=5)
        ttk.Button(botoes, text="Voltar", command=janela.destroy).pack(side="right", padx=5)
        janela.columnconfigure(1, weight=1)
        janela.rowconfigure(4, weight=1)

    def _gerar_id_pedido(self, pedidos):
        numeros = []
        for pedido in pedidos:
            final = pedido.id.split("-")[-1]
            if final.isdigit():
                numeros.append(int(final))
        return f"PED-{max(numeros, default=0) + 1:04d}"

    def registrar_pagamento(self):
        pedido = self._pedido_selecionado()
        if pedido is None:
            return
        if pedido.status != "aguardando_pagamento":
            messagebox.showinfo("Pagamento", "O pedido não está aguardando pagamento.", parent=self.raiz)
            return
        forma = simpledialog.askstring(
            "Pagamento", "Forma (PIX, CREDITO, DEBITO ou BOLETO):", parent=self.raiz,
        )
        if forma is None:
            return
        valor = simpledialog.askfloat("Pagamento", "Valor recebido:", minvalue=0.01, parent=self.raiz)
        if valor is None:
            return
        self._proteger(lambda: registrar_pagamento_pedido(
            pedido.id, Pagamento(datetime.now(), forma, valor),
        ))

    def avancar_status(self):
        pedido = self._pedido_selecionado()
        if pedido is None:
            return
        opcoes = sorted(pedido.TRANSICOES_PERMITIDAS[pedido.status] - {"cancelado"})
        if not opcoes:
            messagebox.showinfo("Status", "Este pedido não pode avançar de status.", parent=self.raiz)
            return
        proximo = simpledialog.askstring(
            "Avançar status",
            "Próximo status permitido: " + ", ".join(opcoes),
            parent=self.raiz,
        )
        if proximo is None:
            return
        self._proteger(lambda: alterar_status_pedido(pedido.id, proximo.strip().lower()))

    def cancelar_pedido(self):
        pedido = self._pedido_selecionado()
        if pedido is None:
            return
        if not messagebox.askyesno("Cancelar pedido", f"Cancelar {pedido.id}?", parent=self.raiz):
            return
        cancelado = self._proteger(lambda: cancelar_pedido(pedido.id))
        if cancelado:
            messagebox.showinfo("Pedido", "Pedido cancelado.", parent=self.raiz)

    def ver_resumo_pedido(self):
        pedido = self._pedido_selecionado()
        if pedido:
            messagebox.showinfo(f"Pedido {pedido.id}", pedido.gerar_resumo_nota(), parent=self.raiz)

    # Relatórios
    def _montar_aba_relatorios(self):
        ttk.Label(self.aba_relatorios, text="Relatórios", font=("Segoe UI", 14, "bold")).pack(anchor="w")
        barra = ttk.Frame(self.aba_relatorios)
        barra.pack(fill="x", pady=8)
        ttk.Label(barra, text="Relatório:").pack(side="left", padx=(0, 8))
        self.tipo_relatorio = tk.StringVar()
        self.combo_relatorios = ttk.Combobox(
            barra, textvariable=self.tipo_relatorio, state="readonly", width=42,
            values=[
                "Estoque", "Pedidos", "Pedidos por status",
                "Faturamento por período", "Mais vendidos e ticket médio",
                "Vendas por UF", "Vendas por categoria",
            ],
        )
        self.combo_relatorios.pack(side="left")
        self.combo_relatorios.current(0)
        ttk.Button(barra, text="Gerar", command=self.gerar_relatorio).pack(side="left", padx=8)
        self.saida_relatorio = tk.Text(self.aba_relatorios, wrap="word", height=22)
        self.saida_relatorio.pack(fill="both", expand=True)
        self.saida_relatorio.configure(state="disabled")

    def gerar_relatorio(self):
        nome = self.tipo_relatorio.get()
        try:
            if nome == "Estoque":
                texto = gerar_relatorio_estoque()
            elif nome == "Pedidos":
                texto = gerar_relatorio_pedidos()
            elif nome == "Pedidos por status":
                texto = gerar_relatorio_pedidos_por_status()
            elif nome == "Faturamento por período":
                inicio_txt = simpledialog.askstring("Período", "Data inicial (DD/MM/AAAA):", parent=self.raiz)
                fim_txt = simpledialog.askstring("Período", "Data final (DD/MM/AAAA):", parent=self.raiz)
                if not inicio_txt or not fim_txt:
                    return
                inicio = datetime.strptime(inicio_txt, "%d/%m/%Y")
                fim = datetime.strptime(fim_txt, "%d/%m/%Y").replace(hour=23, minute=59, second=59)
                texto = gerar_relatorio_faturamento_por_periodo(inicio, fim)
            elif nome == "Mais vendidos e ticket médio":
                limite_txt = simpledialog.askstring(
                    "Ranking", "Limite (deixe vazio para usar settings.json):", parent=self.raiz,
                )
                if limite_txt is None:
                    return
                limite = int(limite_txt) if limite_txt.strip() else None
                texto = gerar_relatorio_top_produtos_e_ticket_medio(limite)
            elif nome == "Vendas por UF":
                texto = gerar_relatorio_vendas_por_uf()
            else:
                texto = gerar_relatorio_vendas_por_categoria()

            self.saida_relatorio.configure(state="normal")
            self.saida_relatorio.delete("1.0", "end")
            self.saida_relatorio.insert("1.0", texto)
            self.saida_relatorio.configure(state="disabled")
        except (TypeError, ValueError, OSError, KeyError) as erro:
            messagebox.showerror("Relatório", str(erro), parent=self.raiz)

    def atualizar_tudo(self):
        self.atualizar_produtos()
        self.atualizar_clientes()
        self.atualizar_pedidos()


def iniciar_interface():
    raiz = tk.Tk()
    LojaGUI(raiz)
    raiz.mainloop()


if __name__ == "__main__":
    iniciar_interface()

