## @package algorithmgroup
## Módulo reponsável pela estrutrura de grupos de parâmetros em algoritmos.

from cspybase.core.exception import CsPyException
from cspybase.algorithm.algorithmparameter import CsPyAlgorithmParameter

## Classe que representa um grupo de configuração de algoritmo.
class CsPyAlgorithmGroup:
    
    ## Construtor
    ## @param self objeto do tipo acesso
    ## @param connection conexão previamente estabelecida.
    ## @param info dicionário informativo da versão.
    def __init__(self, configuration, info):
        if configuration is None:
           raise CsPyException("Configuration cannot be none.")
        self._configuration = configuration
        self._me = {}
        self._parameters = ()
        self._updateme(info)

    ## Consulta a configuração
    ## @param self objeto do tipo acesso
    ## @return a configuração
    def getconfiguration(self):
        return self._configuration

    ## Consulta o identificador.
    ## @param self objeto do tipo versão.
    ## @return o id.
    def getid(self):
        return self._me['id']

    ## Consulta o rótulo.
    ## @param self objeto do tipo versão.
    ## @return o id.
    def getlabel(self):
        return self._me['label']

    ## Informa se o grupo é colapsável
    ## @param self objeto do tipo versão.
    ## @return o indicativo.
    def iscollapsable(self):
        return self._me['collapsable']

    ## Consulta os parâmetros do grupo
    ## @param self objeto do tipo versão.
    ## @return os parâmettros do grupo
    def getparameters(self):
        return self._parameters

    ## Atualiza estruturas internas com base em um dicionário 
    ## @param self objeto do tipo versão.
    ## @param info dicionário informativo
    def _updateme(self, info):
        if info is None:
           raise CsPyException("info for algorithm configuration group cannot be none!")
        # print(info)
        self._me['id'] = info.get('id')
        self._me['label'] = info.get('label') 
        self._me['collapsable'] = info.get('collapsable') if info.get('collapsable') is not None else False
        self._updateparameters(info.get('parameters'))

    ## Faz atualização interna dos parâmetros
    ## @param self objeto do tipo versão.
    ## @param infos lista de informativos de parâmetros
    def _updateparameters(self, infos):
        params = []
        if infos is not None:
           for info in infos:
               params.append(CsPyAlgorithmParameter(self, info))
        self._parameters = tuple(params)


    ## Consulta representação textual.
    ## @param self objeto.
    ## @return texto
    def __str__(self):
        cnf = self.getconfiguration()
        myid = self.getid()
        return "Algorithm version configuration group: " + str(myid) + " : " + str(cnf)

    ## Consulta representação textual.
    ## @param self objeto.
    ## @return texto
    def __repr__(self):
        return self.__str__()

