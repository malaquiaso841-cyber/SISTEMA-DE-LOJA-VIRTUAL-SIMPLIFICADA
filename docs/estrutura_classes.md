# Estrutura Planejada de Classes

Detalhamento de todas as entidades e modelos orientados a objetos do sistema.

---

### 1. `Produto` (Classe Base)
- **Propósito:** Representa os itens do catálogo de produtos.
- **Atributos:** `sku` (único), `nome`, `categoria`, `preco_unitario` (> 0), `estoque` (≥ 0), `ativo`.
- **Encapsulamento e Validações:** `@property` para preço e estoque.
- **Métodos Especiais:** `__str__`, `__repr__`, `__eq__` (compara por SKU) e `__lt__` (ordenação por preço/nome).
- **Subclasses Opcionais:**
  - `ProdutoDigital`: Produtos sem cobrança de frete.
  - `ProdutoFisico`: Produtos com peso para frete.

---

### 2. `Cliente`
- **Propósito:** Gerencia os dados do comprador.
- **Atributos:** `id`, `nome`, `email`, `cpf`, `enderecos` (lista de `Endereco`).
- **Encapsulamento e Validações:** `@property` para CPF e e-mail válidos.
- **Métodos Especiais:** `__eq__` para impedir duplicidade por CPF ou e-mail.

---

### 3. `Endereco`
- **Propósito:** Representa o endereço físico para entregas e cadastro.
- **Atributos:** `logradouro`, `numero`, `complemento`, `bairro`, `cep`, `cidade`, `uf`.

---

### 4. `ItemCarrinho`
- **Propósito:** Associa um `Produto` a uma quantidade solicitada.
- **Atributos:** `produto` (instância de `Produto`), `quantidade` (≥ 1).
- **Métodos:** Cálculo de subtotal do item (`preco_unitario * quantidade`).

---

### 5. `Carrinho`
- **Propósito:** Agrupa os itens selecionados pelo cliente.
- **Atributos:** `itens` (lista de `ItemCarrinho`).
- **Métodos Especiais:** `__len__` para retornar o total de itens acumulados.
- **Operações:** Adicionar, remover e alterar quantidade de itens, calcular subtotal acumulado.

---

### 6. `Cupom`
- **Propósito:** Gerencia cupons de desconto.
- **Atributos:** `codigo`, `tipo` (`VALOR` ou `PERCENTUAL`), `valor_margem`, `data_validade`, `uso_maximo`, `categorias_elegiveis`.
- **Métodos:** Validação de regras e cálculo de desconto.

---

### 7. `Frete`
- **Propósito:** Regras e cálculo de entregas.
- **Métodos:** Cálculo de valor e prazo estimado com base em `settings.json`.

---

### 8. `ItemPedido`
- **Propósito:** Registra o item comprado com o valor unitário congelado na data do pedido.
- **Atributos:** `sku`, `quantidade`, `preco_unitario`.

---

### 9. `Pagamento`
- **Propósito:** Gerencia a transação financeira vinculada a um pedido.
- **Atributos:** `data`, `forma` (`PIX`, `CREDITO`, `DEBITO`, `BOLETO`), `valor`.

---

### 10. `Pedido`
- **Propósito:** Controla o ciclo de vida da compra e máquina de estados.
- **Atributos:** `id`, `cliente`, `endereco_entrega`, `itens`, `valor_frete`, `valor_desconto`, `status` (`CRIADO`, `PAGO`, `ENVIADO`, `ENTREGUE`, `CANCELADO`), `codigo_rastreio`, `pagamentos`.
- **Métodos:** Cálculo de total final, transição de estados, cancelamento com estorno de estoque, emissão de nota/resumo e `__str__`/`__repr__`.