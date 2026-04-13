# models.py

class Jogo:
    def __init__(self, nome, desenvolvedora, dataLancamento, genero, sinopse, plataformas,
                 categoria_id=None, id=None, imagem=None,
                 tag_lancamento=False, tag_destaque=False, tag_promocao=False):
        self.__nome = nome
        self.__desenvolvedora = desenvolvedora
        self.__dataLancamento = dataLancamento
        self.__genero = genero
        self.__sinopse = sinopse
        self.__plataformas = plataformas
        self.__id = id
        self.__imagem = imagem
        self.__categoria_id = categoria_id
        self.__tag_lancamento = bool(tag_lancamento)
        self.__tag_destaque = bool(tag_destaque)
        self.__tag_promocao = bool(tag_promocao)

    @property
    def tag_lancamento(self):
        return self.__tag_lancamento

    @tag_lancamento.setter
    def tag_lancamento(self, valor):
        self.__tag_lancamento = bool(valor)

    @property
    def tag_destaque(self):
        return self.__tag_destaque

    @tag_destaque.setter
    def tag_destaque(self, valor):
        self.__tag_destaque = bool(valor)

    @property
    def tag_promocao(self):
        return self.__tag_promocao

    @tag_promocao.setter
    def tag_promocao(self, valor):
        self.__tag_promocao = bool(valor)


    # Getters e Setters
    @property
    def categoria_id(self):
        return self.__categoria_id
    
    @categoria_id.setter
    def categoria_id(self, valor):
        self.__categoria_id = valor    
    @property
    def nome(self):
        return str.capitalize(self.__nome)
    
    @nome.setter
    def nome(self, valor):
        self.__nome = str.capitalize(valor)

    @property
    def desenvolvedora(self):
        return self.__desenvolvedora
    
    @desenvolvedora.setter
    def desenvolvedora(self, valor):
        self.__desenvolvedora = str.upper(valor)

    @property
    def dataLancamento(self):
        return self.__dataLancamento
    
    @dataLancamento.setter
    def dataLancamento(self, valor):
        self.__dataLancamento = valor

    @property
    def genero(self):
        return self.__genero
    
    @genero.setter
    def genero(self, valor):
        self.__genero = valor

    @property
    def sinopse(self):
        return self.__sinopse
    
    @sinopse.setter
    def sinopse(self, valor):
        self.__sinopse = valor

    @property
    def plataformas(self):
        return self.__plataformas
    
    @plataformas.setter
    def plataformas(self, valor):
        self.__plataformas = valor

    @property
    def id(self):
        return self.__id
    
    @id.setter
    def id(self, valor):
        self.__id = valor

    @property
    def imagem(self):
        return self.__imagem

    @imagem.setter
    def imagem(self, valor):
        self.__imagem = valor




class Usuario:
    def __init__(self, nome, email, senha, foto="default.png", is_admin=False):
        self.__nome = nome
        self.__email = email
        self.__senha = senha
        self.__foto = foto
        self.__is_admin = is_admin

    @property
    def is_admin(self):
        return self.__is_admin

    @is_admin.setter
    def is_admin(self, valor):
        self.__is_admin = valor

    @property
    def foto(self):
        return self.__foto

    @foto.setter
    def foto(self, valor):
        self.__foto = valor

    @property
    def nome(self):
        return self.__nome
    
    @nome.setter
    def nome(self, valor):
        self.__nome = valor

    @property
    def email(self):
        return self.__email
    
    @email.setter
    def email(self, valor):
        self.__email = valor

    @property
    def senha(self):
        return self.__senha
    
    @senha.setter
    def senha(self, valor):
        self.__senha = valor


class Categoria:
    def __init__(self, nome, id=None):
        self.__id = id
        self.__nome = nome

    @property
    def id(self):
        return self.__id

    @property
    def nome(self):
        return self.__nome