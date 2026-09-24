from models.endereco import Endereco

class Cliente:
    def __init__(self, id_cliente, nome, email, cpf, enderecos=None):
        self.id_cliente = id_cliente
        self.nome = nome
        self.email = email
        self.cpf = cpf
        self.enderecos = enderecos if enderecos is not None else []

    @property
    def id_cliente(self):
        return self._id_cliente

    @id_cliente.setter
    def id_cliente(self, valor):
        valor_str = str(valor).strip() if valor is not None else ""
        if not valor_str:
            raise ValueError("O id do cliente não pode ser vazio")
        self._id_cliente = valor_str

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, valor):
        nome_limpo = str(valor).strip() if valor is not None else ""
        if not nome_limpo:
            raise ValueError("O nome não pode ser vazio")
        if not nome_limpo.replace(" ", "").isalpha():
            raise ValueError("O nome do cliente deve conter apenas letras.")
        self._nome = nome_limpo

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, valor):
        email_limpo = str(valor).strip().lower() if valor is not None else ""

        # 2. Valida se o e-mail não está vazio e se possui um formato válido com '@' e '.'
        if not email_limpo or "@" not in email_limpo or "." not in email_limpo.split("@")[-1]:
            raise ValueError("O e-mail informado é inválido.")

        self._email = email_limpo

    @property
    def cpf(self):
        return self._cpf

    @cpf.setter
    def cpf(self, valor):
        cpf_str = str(valor) if valor is not None else ""
        #Extrai apenas os dígitos numéricos (remove pontos, traços e espaços)
        cpf_limpo = "".join(caractere for caractere in cpf_str if caractere.isdigit())

        if len(cpf_limpo) != 11:
            raise ValueError("O CPF deve conter exatamente 11 dígitos numéricos.")
        self._cpf = cpf_limpo

    @property
    def enderecos(self):
        return self._enderecos   

    @enderecos.setter
    def enderecos(self, lista_enderecos):
        if not isinstance(lista_enderecos, list):
            raise ValueError("A propriedade 'enderecos' deve ser uma lista.")

        for end in lista_enderecos:
            if not isinstance(end, Endereco):
                raise ValueError("Todos os itens da lista devem ser instâncias da classe Endereco.")

        self._enderecos = list(lista_enderecos)

    #Métodos de Manipulação de Endereços

    def adicionar_endereco(self, endereco):
        if not isinstance(endereco, Endereco):
            raise ValueError("O objeto fornecido deve ser uma instância da classe Endereco.")
        if endereco not in self.enderecos:
            self._enderecos.append(endereco)

    def remover_endereco(self, endereco):
        if endereco in self.enderecos:
            self.enderecos.remove(endereco)

    def obter_endereco_principal(self):
        """Retorna o primeiro endereço cadastrado ou None se a lista estiver vazia."""
        return self._enderecos[0] if self._enderecos else None
    
    def cpf_formatado(self):
        """Retorna o CPF no formato visual 000.000.000-00."""
        return f"{self._cpf[:3]}.{self._cpf[3:6]}.{self._cpf[6:9]}-{self._cpf[9:]}"

    def to_dict(self):
        return{
            "id_cliente": self.id_cliente,
            "nome": self.nome,
            "email": self.email,
            "cpf": self.cpf,
            "enderecos": [end.to_dict() for end in self.enderecos]
        }

    # MÉTODOS ESPECIAIS

    def __str__(self):
        """Retorna representação legível para exibição do cliente."""
        return f"{self.nome} (CPF: {self.cpf_formatado()}) - {self.email}"

    def __repr__(self):
        """Retorna representação técnica do objeto para depuração."""
        return f"Cliente(id='{self.id_cliente}', cpf='{self.cpf}', email='{self.email}')"

    def __eq__(self, other):
        """Compara se dois clientes são iguais pelo CPF ou pelo e-mail."""
        if not isinstance(other, Cliente):
            return False
        return self.cpf == other.cpf or self.email == other.email