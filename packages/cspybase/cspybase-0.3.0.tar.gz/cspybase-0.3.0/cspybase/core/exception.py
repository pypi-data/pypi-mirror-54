
## Classe de exceção genérica da biblioteca
class CsPyException(Exception):

    # Construtor
    # @param self objeto do tipo exceção
    # @param message mensagem associada a exceção.
    def __init__(self, message):
        super().__init__(message)


## Classe de exceção relativa a uma conexão inválida (não estabelecida)
class CsPyUnconnectedException(CsPyException):

    # Construtor
    # @param self objeto do tipo exceção
    # @param message mensagem associada a exceção.
    def __init__(self):
        super().__init__("The connection must me online (established)")
