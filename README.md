# Sistema de Loja Virtual Simplificada

Sistema acadêmico desenvolvido em Python para simular operações de uma loja virtual. O projeto oferece interface de terminal e interface gráfica, aplica conceitos de Programação Orientada a Objetos e utiliza arquivos JSON para persistir os dados.

## Informações acadêmicas

- **Instituição:** Universidade Federal do Cariri (UFCA)
- **Curso:** Engenharia de Software
- **Disciplina:** Programação Orientada a Objetos
- **Professor:** Jayr Alencar Perreira
- **Integrante:** Malaquias de Oliveira do Nascimento

## Repositório

[Acessar o projeto no GitHub](https://github.com/malaquiaso841-cyber/SISTEMA-DE-LOJA-VIRTUAL-SIMPLIFICADA)

## Documentação

- [Estrutura das classes](https://github.com/malaquiaso841-cyber/SISTEMA-DE-LOJA-VIRTUAL-SIMPLIFICADA/blob/main/docs/estrutura_classes.md)
- [Diagrama UML](https://github.com/malaquiaso841-cyber/SISTEMA-DE-LOJA-VIRTUAL-SIMPLIFICADA/blob/main/docs/uml.txt)
- [Regras de negócio adotadas](https://github.com/malaquiaso841-cyber/SISTEMA-DE-LOJA-VIRTUAL-SIMPLIFICADA/blob/main/docs/regras_de_negocio.md)
- [Funcionalidades do sistema](docs/Funcionalidades.md)

## Funcionalidades

O sistema oferece cadastro de produtos e clientes, criação de pedidos, pagamentos, frete e relatórios. Consulte a documentação completa em [Funcionalidades do sistema](docs/Funcionalidades.md).


## Tecnologias e ferramentas

- **Python 3.10 ou superior**
- **Tkinter** para a interface gráfica, incluído na maioria das instalações do Python para Windows
- **pytest** para testes automatizados
- **JSON** para persistência local dos dados
- **Git e GitHub** para controle de versão

## Estrutura do projeto

```text
SISTEMA-DE-LOJA-VIRTUAL-SIMPLIFICADA/
├── docs/
│   ├── estrutura_classes.md
│   ├── regras_de_negocio.md
│   └── uml.txt
├── interface/
│   ├── gui.py
│   └── menu.py
├── models/
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
│   ├── cadastros.py
│   ├── configuracao.py
│   ├── dados.py
│   ├── operacoes_pedido.py
│   ├── relatorios.py
│   └── seed.py
├── tests/
│   ├── test_cadastros.py
│   ├── test_carrinho.py
│   ├── test_modelos_base.py
│   ├── test_operacoes_pedido.py
│   
│   └── test_seed.py
├── main.py
├── requirements.txt
└── settings.json
```

Os dados JSON são criados na pasta `data/` conforme o sistema salva produtos, clientes, cupons e pedidos.

### Organização das camadas

- [`models/`](https://github.com/malaquiaso841-cyber/SISTEMA-DE-LOJA-VIRTUAL-SIMPLIFICADA/tree/main/models): classes do domínio, regras e validações;
- [`services/`](https://github.com/malaquiaso841-cyber/SISTEMA-DE-LOJA-VIRTUAL-SIMPLIFICADA/tree/main/services): cadastros, persistência, operações de pedido, relatórios, configurações e carga inicial;
- [`interface/`](https://github.com/malaquiaso841-cyber/SISTEMA-DE-LOJA-VIRTUAL-SIMPLIFICADA/tree/main/interface): menu de terminal e interface gráfica;
- [`tests/`](https://github.com/malaquiaso841-cyber/SISTEMA-DE-LOJA-VIRTUAL-SIMPLIFICADA/tree/main/tests): testes automatizados;
- [`docs/`](https://github.com/malaquiaso841-cyber/SISTEMA-DE-LOJA-VIRTUAL-SIMPLIFICADA/tree/main/docs): estrutura das classes, regras de negócio e diagrama UML;
- `data/`: arquivos JSON usados para armazenar os dados; são criados durante a execução;
- `settings.json`: configurações de frete, cancelamento, validade padrão dos cupons e limite de produtos nos relatórios.

## Requisitos

- Python 3.10 ou superior;
- pip;
- pytest para executar os testes;
- Tkinter para abrir a interface gráfica.

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

Instale o pytest:

```powershell
python -m pip install pytest
```

O projeto usa módulos da biblioteca padrão do Python para sua execução. O `requirements.txt` pode ser usado para registrar dependências adicionais caso sejam incluídas futuramente.

### Interface de terminal

```powershell
python main.py --terminal
```

### Interface gráfica

```powershell
python main.py --grafica
```

É necessário escolher uma das opções. O programa não inicia uma interface automaticamente sem um argumento. 

OBS: A interface grafica foi feita inteiramente com IA com base na pasta menu.py.

## Carga inicial de dados

Para adicionar produtos, cliente e cupons de exemplo, execute na raiz do projeto:

```powershell
python -m services.seed
```

A carga inicial não duplica os registros de exemplo que já existirem. Os cupons usam a validade padrão definida em `settings.json`. As regras de frete também são carregadas desse arquivo.

## Configurações

O arquivo `settings.json` permite configurar o frete por UF, uma regra padrão, a janela de cancelamento, a validade padrão dos cupons e o limite padrão do relatório de produtos mais vendidos.

Exemplo da configuração atual:

```json
{
  "frete": {
    "por_uf": {
      "CE": { "valor": 15.0, "prazo_dias": 5 },
      "SP": { "valor": 25.0, "prazo_dias": 8 }
    },
    "padrao": { "valor": 30.0, "prazo_dias": 12 }
  },
  "politica_cancelamento": {
    "janela_horas": 24
  },
  "cupons": {
    "validade_padrao_dias": 30
  },
  "relatorios": {
    "top_n_produtos": 5
  }
}
```

Os valores podem ser alterados conforme as regras desejadas para a execução do sistema.

## Testes automatizados

Na raiz do projeto, execute:

```powershell
python -m pytest
```

A suíte cobre modelos, carrinho, cadastros, operações de pedido, regras de negócio, relatórios e carga inicial de dados.

## Persistência dos dados

Os dados são armazenados localmente em arquivos JSON na pasta `data/`. O projeto não utiliza banco de dados remoto.

Para reiniciar ou editar os dados, faça uma cópia de segurança dos arquivos JSON antes de alterá-los. A carga inicial pode ser executada novamente para incluir registros de exemplo que ainda não existam.

## Limitações

- O sistema é acadêmico e executado localmente;
- Pagamentos e rastreamento são simulações, sem integração com gateways ou transportadoras reais;
- O frete é calculado a partir das regras configuradas no `settings.json`;
- Os arquivos JSON são adequados para uso didático, mas não oferecem os recursos de concorrência e segurança de um banco de dados de produção.

## Licença e finalidade

Projeto desenvolvido para fins acadêmicos na disciplina de Programação Orientada a Objetos da Universidade Federal do Cariri (UFCA).