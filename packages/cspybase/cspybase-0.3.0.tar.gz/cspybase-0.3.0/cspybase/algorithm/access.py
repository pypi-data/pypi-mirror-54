

from cspybase.core.access import CsPyAccess
from cspybase.algorithm.algorithm import CsPyAlgorithm

## Classe que representa um acesso bem sucedido a um servidor.
class CsPyAlgorithmAccess(CsPyAccess):

    ## Construtor
    ## @param self objeto do tipo acesso
    ## @param connection conexão previamente estabelecida.
    def __init__(self, connection):
        super().__init__(connection)

    ## Consulta a lista de algoritmos disponíveis para este acesso
    ## @param self objeto do tipo acesso
    ## @return uma tupla com os algoritmos.
    def getalgorithms(self):
        algos = self.getconnection().get(self.getalgorithmspath(), {})
        algolist = []
        algoit = iter(algos)
        for algo in algoit:
            algolist.append(CsPyAlgorithm(self.getconnection(), algo))
        return tuple(algolist)

    ## Retorna um algoritmo com base em seu id
    ## @param self objeto do tipo acesso
    ## @param algoid o id a ser pesquisado
    ## @return o algoritmo ou None (caso este não seja encontrado)
    def getalgorithm(self, algoid):
        algos = self.getalgorithms()
        for algo in algos:
            if algo.getid() == algoid:
                return algo
        return None

