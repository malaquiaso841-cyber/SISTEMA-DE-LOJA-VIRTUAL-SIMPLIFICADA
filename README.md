# Sistema de Loja Virtual Simplificada

Projeto acadêmico em Python para aplicar conceitos de Programação Orientada a Objetos (POO) na modelagem das operações essenciais de uma loja virtual.

## Informações acadêmicas

| Campo | Informação |
|---|---|
| Instituição | Universidade Federal do Cariri (UFCA) |
| Curso | Engenharia de Software |
| Disciplina | POO — Programação Orientada a Objetos |
| Professor | Jayr Alencar Pereira |
| Integrante | Malaquias de Oliveira do Nascimento |

## Sobre o projeto

O sistema será desenvolvido para uso por interface de linha de comando (CLI), com possibilidade de uma API mínima em Python. O objetivo é simular o fluxo de compra de uma loja virtual, desde o cadastro de produtos e clientes até o pagamento, a expedição e a entrega dos pedidos.

A implementação dará ênfase à orientação a objetos: encapsulamento e validações com `@property`, herança, composição, métodos especiais e regras de negócio. Os dados poderão ser persistidos em JSON ou SQLite, sem uso de ORM.

## Objetivos

### Objetivo geral

Desenvolver um sistema orientado a objetos em Python que simule as operações essenciais de uma loja virtual.

### Objetivos específicos

- Aplicar encapsulamento e validações com propriedades (`@property`);
- Usar herança e composição na modelagem das classes, como produtos físicos e digitais, itens do pedido e carrinho;
- Implementar métodos especiais, incluindo `__str__`, `__repr__`, `__eq__`, `__len__` e `__lt__`;
- Criar regras de negócio para frete, cupons, pagamentos e estorno de estoque;
- Controlar os estados dos pedidos: `CRIADO`, `PAGO`, `ENVIADO`, `ENTREGUE` e `CANCELADO`;
- Implementar persistência simples em JSON ou SQLite e uma rotina de carga inicial (*seed*);
- Criar testes automatizados com `pytest`.

## Funcionalidades previstas

### Produtos e clientes

- Cadastro, consulta, atualização e remoção de produtos (CRUD);
- Validação de SKU único, preço unitário maior que zero e estoque não negativo;
- Ativação e inativação de produtos;
- Cadastro e manutenção de clientes;
- Validação de dados e prevenção de duplicidade de e-mail ou CPF.

### Carrinho, cupons e frete

- Adição, remoção e alteração da quantidade de itens no carrinho;
- Verificação de disponibilidade em estoque e cálculo do subtotal;
- Cupons de valor fixo ou percentual, com código, validade, limite de usos e categorias elegíveis;
- Cálculo de frete parametrizado por UF ou CEP, com prazo de entrega;
- Isenção de frete para produtos digitais.

### Pedidos, pagamentos e expedição

- Fechamento do pedido a partir do carrinho e geração de resumo textual;
- Controle dos estados do pedido;
- Registro de pagamentos por PIX, cartão de crédito, cartão de débito ou boleto;
- Transição para `PAGO` após a quitação do valor total;
- Geração de código fictício de rastreamento e registro da entrega.

### Cancelamentos e relatórios

- Cancelamento dentro da janela permitida e estorno automático do estoque;
- Relatórios de faturamento por período, produtos mais vendidos, ticket médio e vendas por categoria ou UF.

## Tecnologias

- **Python 3.10 ou superior:** linguagem de implementação;
- **pytest:** testes unitários e de integração;
- **JSON ou SQLite3:** persistência simples;
- **Markdown:** documentação técnica;
- **Git e GitHub:** controle de versão e hospedagem do repositório.

## Arquitetura

O projeto será dividido em três camadas:

1. **Interface (CLI):** comandos de terminal disponibilizados em `main.py`;
2. **Serviços e persistência:** regras de negócio, relatórios e leitura e escrita de dados;
3. **Modelos de domínio:** classes que representam as entidades do e-commerce, organizadas em `models/`.

```text
Interface CLI (main.py)
        |
        v
Serviços e regras de negócio <--> Modelos OO (models/)
        |
        v
Persistência (services/dados.py / JSON ou SQLite)
```

## Estrutura de diretórios

```text
SISTEMA-DE-LOJA-VIRTUAL-SIMPLIFICADA/
├── docs/
│   ├── estrutura_classes.md
│   └── uml.txt
├── models/
│   ├── __init__.py
│   ├── produto.py
│   ├── cliente.py
│   ├── endereco.py
│   ├── carrinho.py
│   ├── cupom.py
│   ├── frete.py
│   ├── pedido.py
│   └── pagamento.py
├── services/
│   ├── __init__.py
│   ├── dados.py
│   └── relatorios.py
├── tests/
│   ├── __init__.py
│   ├── test_modelos_base.py
│   └── test_regras_negocio.py
├── main.py
├── settings.json
├── requirements.txt
├── README.md
└── .gitignore
```

## Documentação da modelagem

A descrição detalhada das classes, seus atributos, métodos e relacionamentos será mantida na pasta `docs/`:

- [`docs/estrutura_classes.md`](docs/estrutura_classes.md): responsabilidades, propriedades e métodos das entidades;
- [`docs/uml.txt`](docs/uml.txt): diagrama textual UML, com herança, composição, agregação e assinaturas de métodos.

## Requisitos para execução

- Python 3.10 ou superior;
- `pip`.

Verifique as instalações com:

```bash
python --version
pip --version
```

## Instalação

Clone o repositório e entre na pasta do projeto:

```bash
git clone https://github.com/malaquiaso841-cyber/SISTEMA-DE-LOJA-VIRTUAL-SIMPLIFICADA.git
cd SISTEMA-DE-LOJA-VIRTUAL-SIMPLIFICADA
```

Crie e ative um ambiente virtual e instale as dependências:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Exemplos de uso

Os exemplos abaixo ilustram os comandos previstos para a CLI:

```bash
# Cadastrar um produto
python main.py cadastrar-produto --sku "PROD01" --nome "Notebook" --preco 3500.00 --estoque 10

# Cadastrar um cliente
python main.py cadastrar-cliente --nome "Maria Silva" --email "maria@email.com" --cpf "12345678900"

# Adicionar itens ao carrinho, fechar e pagar um pedido
python main.py add-carrinho --sku "PROD01" --qtd 2
python main.py fechar-pedido --cliente-id 1
python main.py pagar --pedido-id 1 --forma "PIX"

# Consultar relatórios
python main.py relatorio faturamento
python main.py relatorio top
```

## Testes

Com as dependências instaladas, execute a suíte de testes com:

```bash
pytest
```

Os testes devem cobrir, entre outros cenários:

- Validação de preço maior que zero e estoque não negativo;
- Formato de e-mail e unicidade de CPF;
- Tentativa de adicionar ao carrinho mais itens do que há em estoque;
- Aplicação e rejeição de cupons expirados ou inválidos;
- Cálculo de frete e isenção para produtos digitais;
- Transições de estado do pedido e estorno de estoque após cancelamento.

## Licença e finalidade

Este projeto tem finalidade estritamente acadêmica e foi proposto para a disciplina de Programação Orientada a Objetos da Universidade Federal do Cariri (UFCA).
