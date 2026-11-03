# Regras de negócio adotadas

Este documento registra duas decisões de negócio implementadas no sistema da loja virtual.

## Uso de cupons

O uso do cupom é contabilizado quando o pedido é fechado, antes da confirmação do pagamento. Assim, pedidos fechados que depois não forem pagos também consomem um uso do limite do cupom. Essa regra foi adotada pelo projeto; o documento do trabalho não determina em qual etapa o uso deve ser contabilizado.

## Estoque de produtos digitais

Produtos digitais também possuem quantidade de estoque controlada pelo sistema. O estoque de todos os itens do pedido, inclusive digitais, é baixado quando o pagamento total é confirmado. Se um pedido pago for cancelado dentro das condições permitidas, o estoque dos itens é estornado. O documento do trabalho determina que produtos digitais não geram cobrança de frete, mas não exige que sejam excluídos do controle de estoque.

## Correspondência com a implementação

- `Pedido.fechar_pedido_com_carrinho()` registra o uso do cupom ao fechar o pedido.
- `Pedido.registrar_pagamento()` chama a baixa de estoque quando o pagamento quita o pedido.
- `Pedido._baixar_estoque()` processa os itens do pedido sem excluir os digitais.
- `Pedido._estornar_estoque()` repõe as quantidades dos itens quando há cancelamento com estoque previamente baixado.

Essas regras descrevem o comportamento atual da implementação e podem ser revistas se os requisitos do projeto mudarem.
