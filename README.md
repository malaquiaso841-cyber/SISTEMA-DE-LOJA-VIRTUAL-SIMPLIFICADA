# Sistema de Loja Virtual Simplificada

## Informações acadêmicas

- **Instituição:** Universidade Federal do Cariri (UFCA)
- **Curso:** Engenharia de Software
- **Disciplina:** POO - Programação Orientada a Objetos
- **Professor:** Jayr Alencar Pereira
- **Integrante:**
  - Malaquias de Oliveira do Nascimento

---

## Descrição do projeto

Este projeto consiste no desenvolvimento de um **Sistema de Loja Virtual Simplificada** via interface de linha de comando (CLI) ou API mínima em Python, focado no domínio de e-commerce e na aplicação rigorosa dos conceitos de Programação Orientada a Objetos (POO).

O sistema simula todo o fluxo de compras de uma loja virtual: cadastro de produtos e clientes, gestão do carrinho, cálculo de fretes, aplicação de cupons de desconto, fechamento de pedidos, registro de pagamentos, controle de estoque e fluxo de expedição.

A persistência de dados é feita de forma simples (JSON ou SQLite sem ORM) e o modelo orientado a objetos enfatiza herança, composição, encapsulamento com validações (`@property`) e uso de métodos especiais em Python.

---

## Objetivos

### Objetivo geral

Desenvolver um sistema orientado a objetos em Python que simule as operações essenciais de uma loja virtual.

### Objetivos específicos

- Aplicar conceitos de **encapsulamento** e validações com propriedades (`@property`);
- Utilizar **herança e composição** na modelagem das classes (ex.: produtos físicos/digitais, itens do pedido e carrinho);
- Implementar **métodos especiais** (`__str__`, `__repr__`, `__eq__`, `__len__`, `__lt__`);
- Construir regras de negócio para cálculo de frete, aplicação de cupons, pagamentos e estorno de estoque;
- Implementar controle de estados do pedido (`CRIADO`, `PAGO`, `ENVIADO`, `ENTREGUE`, `CANCELADO`);
- Desenvolver um módulo simples de persistência em JSON/SQLite acompanhado de rotina de *seed*;
- Construir uma suíte de testes automatizados utilizando `pytest`.

---

## Funcionalidades

O sistema possui as seguintes funcionalidades:

- **Produtos (CRUD):** cadastro, validação de SKU único, preço unitário (> 0), estoque e controle ativo/inativo;
- **Clientes (CRUD):** cadastro de clientes com validação e controle para impedir duplicidade de e-mail ou CPF;
- **Carrinho de Compras:** adição, remoção e alteração de quantidade de itens, validação de disponibilidade de estoque e cálculo de subtotal;
- **Cupons de Desconto:** validação por código, tipo (valor fixo ou percentual), validade, limite de usos e categorias elegíveis;
- **Cálculo de Frete:** cálculo parametrizado por UF/CEP e definição de prazos de entrega (produtos digitais isentos);
- **Gestão de Pedidos:** fechamento a partir do carrinho, geração de resumo/nota textual e máquinas de estado;
- **Pagamentos:** registro de transações (PIX, Crédito, Débito, Boleto) e transição para `PAGO` ao quitar o total;
- **Expedição:** geração de código de rastreamento fictício (`ENVIADO`) e registro de data de entrega (`ENTREGUE`);
- **Cancelamento e Estorno:** cancelamento dentro da janela permitida e repotencialização/estorno automático do estoque;
- **Relatórios Analíticos:** faturamento por período, Top N produtos mais vendidos, ticket médio e vendas por categoria/UF.

---

## Tecnologias utilizadas

- **Python 3.10+:** linguagem principal para implementação das classes e regras do sistema;
- **Pytest:** execução da suíte de testes unitários e de integração;
- **JSON / SQLite3:** armazenamento e persistência simples dos dados;
- **Markdown:** produção da documentação técnica;
- **Git e GitHub:** controle de versão e armazenamento do repositório.

---

## Arquitetura

O sistema é estruturado em três camadas principais:

1. **Interface / CLI:** comandos de terminal (`main.py`) para interação do usuário com os serviços;
2. **Camada de Serviços e Persistência:** regras de negócio complexas, relatórios e controle de leitura/escrita em dados (`dados.py`);
3. **Modelos de Domínio (POO):** classes que representam os conceitos e entidades do e-commerce (`models/`).

[Interface CLI (main.py)] ---> [Serviços & Regras de Negócio] <---> [Modelos OO (models/)]
                                         ^
                                         |
                                         v
                             [Persistência (dados.py / JSON)]

---

## Estrutura do projeto

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

---

## Documentação e Modelagem das Classes

A arquitetura detalhada do modelo orientado a objetos, atributos, métodos e diagramas estão organizados em arquivos separados na pasta de documentação:

- 📑 **[Estrutura Detalhada das Classes](docs/estrutura_classes.md):** detalhamento de atributos, propriedades, métodos especiais e responsabilidades de cada entidade.
- 📐 **[Diagrama UML Textual](docs/uml.txt):** mapeamento completo das relações de herança, composição, agregação e assinaturas dos métodos.

---


## Requisitos

Antes de executar o projeto, é necessário ter instalado na máquina:

- Python 3.10 ou superior;
- Gerenciador de pacotes `pip`.

Para verificar as instalações, execute no terminal:

python --version
pip --version

---

## Instalação

### 1. Clonar o repositório

git clone https://github.com/malaquiaso841-cyber/SISTEMA-DE-LOJA-VIRTUAL-SIMPLIFICADA.git

Entre na pasta do projeto:

cd SISTEMA-DE-LOJA-VIRTUAL-SIMPLIFICADA

### 2. Configurar o ambiente virtual e dependências

python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt

---

## Execução

A aplicação é executada via linha de comando utilizando o arquivo `main.py`.

### Exemplos de comandos CLI

# Cadastrar um novo produto
python main.py cadastrar-produto --sku "PROD01" --nome "Notebook" --preco 3500.00 --estoque 10

# Cadastrar um cliente
python main.py cadastrar-cliente --nome "Maria Silva" --email "maria@email.com" --cpf "12345678900"

# Operações do carrinho e pedido
python main.py add-carrinho --sku "PROD01" --qtd 2
python main.py fechar-pedido --cliente-id 1
python main.py pagar --pedido-id 1 --forma "PIX"

# Relatórios
python main.py relatorio faturamento
python main.py relatorio top

---

## Testes

Os testes unitários e de integração garantem a integridade das regras de negócio e validações de POO.

Para rodar toda a suíte de testes com o `pytest`, execute:

pytest

Os principais cenários testados incluem:
- Encapsulamento de preço (> 0) e estoque (≥ 0);
- Validação de formato de e-mail e CPF único;
- Tentativa de inclusão no carrinho com estoque insuficiente;
- Aplicação e rejeição de cupons expirados ou inválidos;
- Cálculo correto de frete e isenção para produtos digitais;
- Mudanças de estado do pedido e estorno de estoque em caso de cancelamento.

---

## Licença

Este projeto foi desenvolvido para fins estritamente acadêmicos para a disciplina de Programação Orientada a Objetos da Universidade Federal do Cariri (UFCA).