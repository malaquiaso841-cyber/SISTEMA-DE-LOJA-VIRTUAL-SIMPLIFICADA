class Endereco:
    def __init__(self, logradouro, numero, bairro, cidade, uf, cep, complemento=""):
        self.logradouro = logradouro
        self.numero = numero
        self.bairro = bairro
        self.cidade = cidade
        self.uf = uf
        self.cep = cep
        self.complemento = complemento

    @property
    def logradouro(self):
        return self._logradouro

    @logradouro.setter
    def logradouro(self, valor):
        if not valor or not valor.strip():
            raise ValueError("O logradouro não pode ser vazio.")
        self._logradouro = valor.strip()

    @property
    def numero(self):
        return self._numero

    @numero.setter
    def numero(self, valor):
        valor_str = str(valor).strip() if valor is not None else ""
        if not valor_str:
            raise ValueError("O número do endereço não pode ser vazio.")
        self._numero = valor_str

    @property
    def bairro(self):
        return self._bairro

    @bairro.setter
    def bairro(self, valor):
        if not valor or not valor.strip():
            raise ValueError("O bairro não pode ser vazio")
        self._bairro = valor.strip()

    @property
    def cidade(self):
        return self._cidade

    @cidade.setter
    def cidade(self, valor):
        if not valor or not valor.strip():
            raise ValueError("A cidade não pode ser vazia")
        self._cidade = valor.strip()

    @property
    def uf(self):
        return self._uf

    @uf.setter
    def uf(self, valor):
        valor_limpo = str(valor).strip().upper() if valor else ""
        
        if len(valor_limpo) != 2 or not valor_limpo.isalpha():
            raise ValueError("A UF deve conter exatamente 2 letras (ex: 'CE', 'SP').")
            
        self._uf = valor_limpo

    @property
    def cep(self):
        return self._cep

    @cep.setter
    def cep(self, valor):
        cep_str = str(valor) if valor else ""
        cep_limpo = "".join(caractere for caractere in cep_str if caractere.isdigit())
        
        if len(cep_limpo) != 8:
            raise ValueError("O CEP deve conter exatamente 8 dígitos numéricos.")
            
        self._cep = cep_limpo

    def cep_formatado(self):
        """Retorna o CEP formatado com hífen (ex: 63100-000)."""
        return f"{self._cep[:5]}-{self._cep[5:]}"

    def to_dict(self):
    
        return {
            "logradouro": self.logradouro,
            "numero": self.numero,
            "bairro": self.bairro,
            "cidade": self.cidade,
            "uf": self.uf,
            "cep": self.cep,
            "complemento": self.complemento
        }

    # MÉTODOS ESPECIAIS 

    def __str__(self):
        """Retorna o endereço formatado para exibir no resumo do pedido/nota."""
        comp = f", {self.complemento}" if self.complemento else ""
        return f"{self.logradouro}, {self.numero}{comp} - {self.bairro}, {self.cidade}/{self.uf} - CEP: {self.cep_formatado()}"

    def __repr__(self):
        """Retorna a representação do objeto para depuração e testes."""
        return f"Endereco(cep='{self.cep}', uf='{self.uf}', cidade='{self.cidade}')"

    def __eq__(self, other):
        """Compara se dois endereços são iguais pelo CEP, número e complemento."""
        if not isinstance(other, Endereco):
            return False
        return (self.cep == other.cep and 
                self.numero == other.numero and 
                self.complemento == other.complemento)
    

    
    