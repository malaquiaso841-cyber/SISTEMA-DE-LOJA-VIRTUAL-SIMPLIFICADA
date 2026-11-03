# Funcionalidades do Sistema

O sistema simula as operações de uma loja virtual. Ele pode ser utilizado pelo menu de terminal ou pela interface gráfica.

## Acessar as interfaces

Na pasta principal do projeto, execute:

```powershell
python main.py --terminal
```

Para abrir a interface gráfica:

```powershell
python main.py --grafica
```

## Produtos

O sistema permite:

- Cadastrar e listar produtos;
- Atualizar nome, categoria, preço e estoque;
- Ativar ou inativar produtos;
- Remover produtos inativos;
- Identificar produtos físicos e digitais;
- Validar SKU, preço e quantidade em estoque.

## Clientes e endereços

O sistema permite:

- Cadastrar e listar clientes;
- Atualizar os dados de um cliente;
- Remover clientes;
- Associar endereços aos clientes;
- Informar nome, e-mail, CPF e endereço para a criação de pedidos;
- Validar os dados e impedir duplicidade de e-mail e CPF.

## Carrinho

Durante a criação de um pedido, é possível:

- Adicionar produtos e quantidades;
- Remover produtos;
- Alterar a quantidade de um item;
- Consultar os itens e o subtotal;
- Verificar a disponibilidade do produto no estoque.

O estoque é validado novamente quando o pedido é fechado, para evitar criar o pedido com uma quantidade superior à disponível.

## Cupons

Os cupons podem ter:

- Código;
- Desconto em valor ou percentual;
- Data de validade;
- Limite de usos;
- Categorias de produtos elegíveis.

O sistema valida as regras antes de aplicar o desconto. O uso do cupom é contabilizado quando o pedido é fechado, antes da confirmação do pagamento.

## Pedidos e pagamentos

O sistema permite:

- Criar pedidos a partir do carrinho;
- Consultar o resumo do pedido;
- Registrar pagamentos parciais ou totais;
- Atualizar o status do pedido;
- Cancelar pedidos conforme o status e a janela configurada;
- Consultar as formas de pagamento registradas.

Os status utilizados pelo sistema são:

- `aguardando_pagamento`;
- `pago`;
- `enviado`;
- `entregue`;
- `cancelado`.

Quando o pagamento total é confirmado, o pedido passa para `pago` e o estoque dos itens é baixado. Se um pedido pago for cancelado dentro das condições permitidas, o estoque é estornado.

## Frete e entrega

O frete é calculado com base nas regras de `settings.json`, considerando a UF do endereço e a regra padrão quando não houver uma específica.

Para pedidos com produtos físicos, o resumo apresenta o valor do frete e o prazo estimado em dias úteis. Produtos digitais não geram cobrança de frete. O estoque dos produtos digitais também é controlado pelo sistema.

Ao atualizar o pedido para `enviado`, o sistema gera um código de rastreio fictício. Ao marcá-lo como `entregue`, registra a data da entrega.

## Relatórios

O sistema oferece relatórios de:

- Estoque;
- Pedidos;
- Pedidos por status, com quantidade e percentual;
- Faturamento por período;
- Produtos mais vendidos e ticket médio;
- Vendas por unidade federativa (UF);
- Vendas por categoria.

Os relatórios de vendas consideram pedidos com status `pago`, `enviado` ou `entregue`.

## Configurações

O arquivo `settings.json` contém:

- Valores e prazos de frete por UF e uma regra padrão;
- Janela de cancelamento em horas;
- Validade padrão dos cupons;
- Quantidade padrão de produtos exibidos no ranking de mais vendidos.

## Persistência e carga inicial

Os dados de produtos, clientes, cupons e pedidos são armazenados em arquivos JSON na pasta `data/`.

Para carregar os registros de exemplo, execute na pasta principal:

```powershell
python -m services.seed
```

A carga inicial pode ser executada novamente sem adicionar duplicatas dos mesmos registros de exemplo.

## Testes

Para executar os testes automatizados na pasta principal:

```powershell
python -m pytest
```

Os testes cobrem modelos, carrinho, cadastros, regras de negócio, operações de pedido, relatórios e carga inicial.

## Documentação relacionada

- [Estrutura das classes](estrutura_classes.md)
- [Diagrama UML](uml.txt)
- [Regras de negócio adotadas](regras_de_negocio.md)