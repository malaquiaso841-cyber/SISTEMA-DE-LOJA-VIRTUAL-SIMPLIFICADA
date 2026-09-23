# Estrutura Planejada de Classes

Detalhamento de todas as entidades e modelos orientados a objetos do sistema.

---

### 1. `Produto` (Classe Base)
- **Propósito:** Representa os itens do catálogo de produtos[cite: 1].
- **Atributos:** `sku` (único), `nome`, `categoria`, `preco_unitario` (> 0), `estoque` (≥ 0), `ativo`[cite: 1].
- **Encapsulamento e Validações:** `@property` para preço e estoque[cite: 1].
- **Métodos Especiais:** `__str__`, `__repr__`, `__eq__` (compara por SKU) e `__lt__` (ordenação por preço/nome)[cite: 1].
- **Subclasses Opcionais:**
  - `ProdutoDigital`: Produtos sem cobrança de frete[cite: 1].
  - `ProdutoFisico`: Produtos com peso para frete[cite: 1].

---

### 2. `Cliente`
- **Propósito:** Gerencia os dados do comprador[cite: 1].
- **Atributos:** `id`, `nome`, `email`, `cpf`, `enderecos` (lista de `Endereco`)[cite: 1].
- **Encapsulamento e Validações:** `@property` para CPF e e-mail válidos[cite: 1].
- **Métodos Especiais:** `__eq__` para impedir duplicidade por CPF ou e-mail[cite: 1].

---

### 3. `Endereco`
- **Propósito:** Representa o endereço físico para entregas e cadastro[cite: 1].
- **Atributos:** `logradouro`, `numero`, `complemento`, `bairro`, `cep`, `cidade`, `uf`[cite: 1].

---

### 4. `ItemCarrinho`
- **Propósito:** Associa um `Produto` a uma quantidade solicitada[cite: 1].
- **Atributos:** `produto` (instância de `Produto`), `quantidade` (≥ 1)[cite: 1].
- **Métodos:** Cálculo de subtotal do item (`preco_unitario * quantidade`)[cite: 1].

---

### 5. `Carrinho`
- **Propósito:** Agrupa os itens selecionados pelo cliente[cite: 1].
- **Atributos:** `itens` (lista de `ItemCarrinho`)[cite: 1].
- **Métodos Especiais:** `__len__` para retornar o total de itens acumulados[cite: 1].
- **Operações:** Adicionar, remover e alterar quantidade de itens, calcular subtotal acumulado[cite: 1].

---

### 6. `Cupom`
- **Propósito:** Gerencia cupons de desconto[cite: 1].
- **Atributos:** `codigo`, `tipo` (`VALOR` ou `PERCENTUAL`), `valor_margem`, `data_validade`, `uso_maximo`, `categorias_elegiveis`[cite: 1].
- **Métodos:** Validação de regras e cálculo de desconto[cite: 1].

---

### 7. `Frete`
- **Propósito:** Regras e cálculo de entregas[cite: 1].
- **Métodos:** Cálculo de valor e prazo estimado com base em `settings.json`[cite: 1].

---

### 8. `ItemPedido`
- **Propósito:** Registra o item comprado com o valor unitário congelado na data do pedido[cite: 1].
- **Atributos:** `sku`, `quantidade`, `preco_unitario`[cite: 1].

---

### 9. `Pagamento`
- **Propósito:** Gerencia a transação financeira vinculada a um pedido[cite: 1].
- **Atributos:** `data`, `forma` (`PIX`, `CREDITO`, `DEBITO`, `BOLETO`), `valor`[cite: 1].

---

### 10. `Pedido`
- **Propósito:** Controla o ciclo de vida da compra e máquina de estados[cite: 1].
- **Atributos:** `id`, `cliente`, `endereco_entrega`, `itens`, `valor_frete`, `valor_desconto`, `status` (`CRIADO`, `PAGO`, `ENVIADO`, `ENTREGUE`, `CANCELADO`), `codigo_rastreio`, `pagamentos`[cite: 1].
- **Métodos:** Cálculo de total final, transição de estados, cancelamento com estorno de estoque, emissão de nota/resumo e `__str__`/`__repr__`[cite: 1].