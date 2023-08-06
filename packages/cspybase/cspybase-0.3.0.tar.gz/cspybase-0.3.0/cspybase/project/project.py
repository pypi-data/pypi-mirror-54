## @package project
## Módulo responsável pela abstração do conceito de projetos no sistema

from cspybase.user.user import CsPyUser
from cspybase.project.file import CsPyFile
from cspybase.core.exception import CsPyException
from cspybase.core.object import CsPyObject

## Classe que representa um projeto dentro do servidor.
class CsPyProject(CsPyObject):

    # Construtor
    # @param self objeto do tipo arquivo/diretório
    # @param connection conexão
    # @param info dicionário informativo dos dados o arquivo/diretório
    def __init__(self, connection, info):
        super().__init__(connection)
        self._me = {}
        self._updateme(info)

    ## Consulta o nome do projeto.
    ## @param self objeto do tipo projeto.
    ## @return o nome.
    def getname(self):
        return self._me['name']

    ## Consulta o identificador do projeto.
    ## @param self objeto do tipo projeto.
    ## @return o id.
    def getid(self):
        return self._me['id']

    ## Consulta o usuário dono do projeto.
    ## @param self objeto do tipo projeto.
    ## @return o usuário.
    def getowner(self):
        return self._me['owner']

    ## Consulta o diretório-raiz do projeto
    ## @param self objeto do tipo projeto.
    ## @return o diretório.
    def getroot(self):
        info = self.getconnection().get(self.getprojectspath() + "/" + self.getid() + "/files/root/metadata", {})
        if info is None:
            raise CsPyException("bad info for project root!")
        return CsPyFile(self.getconnection(), self.getid(), info.get('file'))

    ## Faz busca de dados no servidor
    ## @param self objeto.
    def _fetchdata(self):
        info = self.getconnection().get(self.getprojectspath() + "/" + self.getid(), {})
        self._updateme(info)

    ## Atualiza estruturas internas com base em um dicionário 
    ## @param self objeto.
    ## @param info dicionário informativo
    def _updateme(self, info):
        if info is None:
            raise CsPyException("info for project cannot be none!")
        self._me['id'] = info['id']
        self._me['name'] = info['name']
        self._me['description'] = info['description']
        self._me['owner'] = CsPyUser(self.getconnection(), info['owner'])

    ## Consulta representação textual.
    ## @param self objeto.
    ## @return texto
    def __str__(self):
        name = self.getname()
        myid = self.getid()
        return "Project: " + name + " - " + myid + " (Owner: " + str(self.getowner()) + ")"

    ## Consulta representação textual.
    ## @param self objeto.
    ## @return texto
    def __repr__(self):
        return self.__str__()



