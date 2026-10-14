# Sistema de Loja Virtual Simplificada

Sistema acadêmico desenvolvido em Python para simular operações essenciais de uma loja virtual por meio de uma interface de terminal. O projeto aplica conceitos de Programação Orientada a Objetos, validação de dados, persistência em JSON e testes automatizados.

## Informações acadêmicas

- **Instituição:** Universidade Federal do Cariri (UFCA)
- **Curso:** Engenharia de Software
- **Disciplina:** Programação Orientada a objetos
- **Professor:** Jayr Alencar Perreira
- **Integrante:** Malaquias de Oliveira do Nascimento

## Repositório

[ Acessar o projeto no GitHub ](https://github.com/malaquiaso841-cyber/SISTEMA-DE-LOJA-VIRTUAL-SIMPLIFICADA)

## Documentação

- [Estrutura das classes](docs/estrutura_classes.md)
- [Diagrama UML](docs/uml.txt)

Os links acima são relativos ao repositório: depois de substituir este README na raiz do projeto, eles abrirão os arquivos correspondentes no GitHub.

## Funcionalidades

### Produtos

- Cadastrar e listar produtos;
- Atualizar dados do produto;
- Ativar ou inativar produtos;
- Remover produtos inativos;
- Validar SKU, preço e quantidade em estoque;
- Identificar produtos físicos e digitais.

### Clientes

- Cadastrar e listar clientes;
- Atualizar dados cadastrais;
- Remover clientes;
- Manter endereço associado ao cliente;
- Validar nome, e-mail, CPF, CEP e UF;
- Evitar duplicidade de e-mail e CPF.

### Carrinho, cupons e pedidos

- Selecionar cliente e endereço de entrega;
- Adicionar produtos e quantidades ao carrinho;
- Consultar subtotal;
- Aplicar cupom, quando informado;
- Calcular frete conforme a configuração;
- Criar e consultar pedidos;
- Registrar pagamentos;
- Atualizar o status do pedido;
- Cancelar pedidos conforme as regras implementadas no sistema.

### Relatórios

- Estoque;
- Pedidos;
- Pedidos agrupados por status;
- Faturamento por período;
- Produtos mais vendidos e ticket médio;
- Vendas por unidade federativa (UF).

## Tecnologias e ferramentas

- **Python 3.10 ou superior**
- **pytest** para testes automatizados
- **JSON** para persistência local dos dados
- **Git e GitHub** para controle de versão

## Estrutura do projeto

```text
SISTEMA-DE-LOJA-VIRTUAL-SIMPLIFICADA/
├── data/
│   ├── clientes.json
│   ├── cupons.json
│   ├── pedidos.json
│   └── produtos.json
├── docs/
│   ├── estrutura_classes.md
│   └── uml.txt
├── interface/
│   └── menu.py
├── models/
│   ├── __init__.py
│   ├── carrinho.py
│   ├── cliente.py
│   ├── cupom.py
│   ├── endereco.py
│   ├── frete.py
│   ├── item_carrinho.py
│   ├── item_pedido.py
│   ├── pagamento.py
│   ├── pedido.py
│   └── produto.py
├── services/
│   ├── __init__.py
│   ├── cadastros.py
│   ├── dados.py
│   ├── operacoes_pedido.py
│   ├── relatorios.py
│   └── seed.py
├── tests/
│   ├── __init__.py
│   ├── test_cadastros.py
│   ├── test_carrinho.py
│   ├── test_modelos_base.py
│   ├── test_operacoes_pedido.py
│   ├── test_regras_negocio.py
│   └── test_seed.py
├── main.py
├── README.md
├── requirements.txt
└── settings.json
```

### Organização das camadas

- `models/`: entidades do domínio e validações dos atributos;
- `services/`: operações de cadastro, persistência, pedidos, relatórios e carga inicial;
- `interface/`: interação com o usuário por menus no terminal;
- `data/`: arquivos JSON usados para armazenar os dados;
- `tests/`: testes automatizados;
- `docs/`: documentação da modelagem e diagrama UML;
- `settings.json`: parâmetros de frete.

## Requisitos

- Python 3.10 ou superior;
- pip.

Confira as versões instaladas:

```powershell
python --version
pip --version
```

## Instalação e execução

Clone o repositório e acesse a pasta do projeto:

```powershell
git clone https://github.com/malaquiaso841-cyber/SISTEMA-DE-LOJA-VIRTUAL-SIMPLIFICADA.git
cd SISTEMA-DE-LOJA-VIRTUAL-SIMPLIFICADA
```

Crie e ative um ambiente virtual no Windows:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Instale as dependências:

```powershell
pip install -r requirements.txt
```

Inicie a aplicação:

```powershell
python main.py
```

A aplicação apresenta um menu interativo no terminal. Siga as opções exibidas para acessar os cadastros, pedidos e relatórios.

## Carga inicial de dados

Para adicionar os registros de exemplo fornecidos pelo projeto, execute na raiz:

```powershell
python -m services.seed
```

A carga inicial pode ser executada mais de uma vez: os registros de exemplo já existentes não são adicionados novamente. Os arquivos de dados ficam na pasta `data/`.

## Testes automatizados

Execute a suíte de testes na raiz do projeto:

```powershell
pytest
```

Os testes existentes cobrem modelos, carrinho, cadastros, operações de pedido, regras de negócio e carga inicial. **Conforme informado pelo integrante do projeto, os testes estão funcionando.**

## Persistência dos dados

Os registros são armazenados localmente em arquivos JSON dentro de `data/`. Para reiniciar os dados, faça uma cópia de segurança antes de limpar ou editar esses arquivos. A aplicação não utiliza banco de dados remoto.

## Limitações

- O sistema é acadêmico e executado localmente pelo terminal;
- Pagamentos e rastreamento são simulações, sem integração com gateways ou transportadoras reais;
- Os arquivos JSON são destinados a uso didático e não oferecem os recursos de concorrência e segurança de um banco de dados de produção.

## Licença e finalidade

Projeto desenvolvido para fins acadêmicos na disciplina de Programação Orientada a objetos da Universidade Federal do Cariri (UFCA).

