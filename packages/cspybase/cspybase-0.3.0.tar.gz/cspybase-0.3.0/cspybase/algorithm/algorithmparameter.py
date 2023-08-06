## @package algorithmparameter
## Módulo reponsável pela estrutrura de parâmetros de algoritmos.

from cspybase.core.exception import CsPyException


## Classe que representa uma ação de configuração de algoritmo.
class CsPyAlgorithmParameter:
    
    ## Construtor
    ## @param self objeto parâmetro
    ## @param group grupo do parâmetro
    ## @param info dicionário informativo da versão.
    def __init__(self, group, info):
        if group is None:
           raise CsPyException("group cannot be none.")
        self._group = group
        self._me = {}
        self._updateme(info)

    ## Consulta o grupo
    ## @param self objeto parâmetro
    ## @return grupo
    def getgroup(self):
        return self._group

    ## Consulta o identificador
    ## @param self objeto parâmetro
    ## @return id
    def getid(self):
        return self._me['id']

    ## Consulta o rótulo
    ## @param self objeto parâmetro
    ## @return rótulo
    def getlabel(self):
        return self._me['label']

    ## Consulta a descrição
    ## @param self objeto parâmetro
    ## @return descrição
    def getdescription(self):
        return self._me['description']

    ## Atualiza estruturas internas com base em um dicionário 
    ## @param self objeto.
    ## @param info dicionário informativo
    def _updateme(self, info):
        if info is None:
           raise CsPyException("info for algorithm configuration parameter cannot be none!")
        self._me['id'] = info.get('id')
        self._me['label'] = info.get('label')
        self._me['type'] = info.get('type')
        self._me['description'] = info.get('description') if info.get('description') is not None else ""
        self._me['optional'] = info.get('optional') if info.get('optional') is not None else False
        self._me['hidden'] = info.get('hidden') if info.get('hidden') is not None else False
        self._me['ignoreifhidden'] = info.get('ignoreIfHidden') if info.get('ignoreIfHidden') is not None else False
        self._me['ignoreifdisabled'] = info.get('ignoreIfDisabled') if info.get('ignoreIfDisabled') is not None else False
        self._me['defaultvalue'] = info.get('defaultValue')

    ## Consulta representação textual.
    ## @param self objeto.
    ## @return texto
    def __str__(self):
        myid = self.getid()
        mylabel = self.getlabel()
        return "Algorithm version configuration parameter: " + str(myid) + " : " + str(mylabel)

    ## Consulta representação textual.
    ## @param self objeto.
    ## @return texto
    def __repr__(self):
        return self.__str__()
