## @package algorithmaction
## Módulo reponsável pela estrutrura de parâmetros de algoritmos.

from cspybase.core.exception import CsPyException


## Classe que representa uma ação de configuração de algoritmo.
class CsPyAlgorithmAction:
    
    ## Construtor
    ## @param self objeto do tipo acesso
    ## @param connection conexão previamente estabelecida.
    ## @param info dicionário informativo da versão.
    def __init__(self, configuration, info):
        if configuration is None:
           raise CsPyException("Configuration cannot be none.")
        self._configuration = configuration
        self._me = {}
        self._updateme(info)

    ## Consulta o identificador
    ## @param self objeto parâmetro
    ## @return id
    def getname(self):
        return self._me['name']

    ## Consulta o rótulo
    ## @param self objeto parâmetro
    ## @return rótulo
    def gettargetid(self):
        return self._me['targetid']

    ## Atualiza estruturas internas com base em um dicionário 
    ## @param self objeto.
    ## @param info dicionário informativo
    def _updateme(self, info):
        if info is None:
           raise CsPyException("info for algorithm configuration parameter cannot be none!")
        # print(info)
        self._me['name'] = info.get('name')
        self._me['targetid'] = info.get('targetId') 

    ## Consulta representação textual.
    ## @param self objeto.
    ## @return texto
    def __str__(self):
        name = self.getname()
        target = self.gettargetid()
        return "Algorithm version configuration action: " + str(name) + " -> " + str(target)

    ## Consulta representação textual.
    ## @param self objeto.
    ## @return texto
    def __repr__(self):
        return self.__str__()

