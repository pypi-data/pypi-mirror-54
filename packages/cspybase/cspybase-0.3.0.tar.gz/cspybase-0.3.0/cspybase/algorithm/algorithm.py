## @package algorithm
## Módulo reponsável pela estrutrura de algoritmos.

from cspybase.core.object import CsPyObject
from cspybase.user.user import CsPyUser
from cspybase.core.exception import CsPyException
from cspybase.algorithm.algorithmversion import CsPyAlgorithmVersion

## Classe que representa um algoritmo.
class CsPyAlgorithm(CsPyObject):
    
    ## Construtor
    ## @param self objeto do tipo acesso
    ## @param connection conexão previamente estabelecida.
    ## @param info dicionário informativo do algoritmo.
    def __init__(self, connection, info):
        super().__init__(connection)
        self._me = {}
        self._versions = ()
        self._updateme(info)

    ## Consulta o nome do algoritmo.
    ## @param self objeto do tipo algoritmo.
    ## @return o nome.
    def getname(self):
        return self._me['name']

    ## Consulta o identificador do algoritmo.
    ## @param self objeto do tipo algoritmo.
    ## @return o id.
    def getid(self):
        return self._me['id']

    ## Consulta o usuário criador do algoritmo.
    ## @param self objeto do tipo algoritmo.
    ## @return o usuário.
    def getcreator(self):
        return self._me['creator']

    ## Consulta a última versão do algoritmo.
    ## @param self objeto do tipo algoritmo.
    ## @return a versão.
    def getlastversion(self):
        return self._me['lastversion']

    ## Consulta versões do algoritmo.
    ## @param self objeto do tipo algoritmo.
    ## @return as versões.
    def getversions(self):
        return self._me['versions']

    ## Atualiza estruturas internas com base em um dicionário 
    ## @param self objeto.
    ## @param info dicionário informativo
    def _updateme(self, info):
        if info is None:
           raise CsPyException("info for algorithm cannot be none!")
        self._me['id'] = info['id']
        self._me['name'] = info['name']
        cnn = self.getconnection()
        self._fillme(info, 'creator', 'whoCreated', lambda infovalue: CsPyUser(cnn, infovalue))
        self._fillme(info, 'lastversion', 'lastVersion', lambda infovalue: CsPyAlgorithmVersion(self, cnn, infovalue))
        self._updateversions(info.get('versions'))
        
    ## Atualiza estruturas internas das versões com base em dicionários
    ## @param self objeto.
    ## @param info dicionários informativos de versões
    def _updateversions(self, infos):
        versions = []
        if infos is not None:
           for info in infos:
               versions.append(CsPyAlgorithmVersion(self, self.getconnection(), info))
        self._me['versions'] = tuple(versions)


    ## Consulta representação textual.
    ## @param self objeto.
    ## @return texto
    def __str__(self):
        myid = self.getid()
        name = self.getname()
        creator = self.getcreator()
        return "Algorithm: " + name + " - " + myid + " (Creator: " + str(creator) + ") " + "versions: " + str(self.getversions())

    ## Consulta representação textual.
    ## @param self objeto.
    ## @return texto
    def __repr__(self):
        return self.__str__()
