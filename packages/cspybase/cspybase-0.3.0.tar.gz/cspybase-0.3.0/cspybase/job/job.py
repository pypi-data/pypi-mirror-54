from cspybase.core.object import CsPyObject
from cspybase.user.user import CsPyUser
from cspybase.core.exception import CsPyException
from datetime import datetime
import re

## Classe que representa um Job.
class CsPyJob(CsPyObject):
    
    ## Construtor
    ## @param self objeto do tipo acesso
    ## @param connection conexão previamente estabelecida.
    ## @param info dicionário informativo do algoritmo.
    def __init__(self, connection, info):
        super().__init__(connection)
        self._me = {}
        self._versions = ()
        self._updateme(info)

    ## Consulta o id do algoritmo utilizado no job.
    ## @param self objeto do tipo job.
    ## @return string com o id do algoritmo utilizado no Job.
    def getalgorithmid(self):
        return self._me['algorithmId']

    ## Consulta o identificador do job.
    ## @param self objeto do tipo job.
    ## @return o id.
    def getid(self):
        return self._me['jobId']

    ## Consulta o usuário owner do job.
    ## @param self objeto do tipo job.
    ## @return o usuário.
    def getowner(self):
        return self._me['owner']

    ## Consulta o estado do job.
    ## @param self objeto do tipo job.
    ## @return o estado.
    def getState(self):
        return self._me['state']
    
    ## Consulta a maquina em que o job foi executado.
    ## @param self objeto do tipo job.
    ## @return o nome da maquina.
    def getExecutionMachine(self):
        return self._me['executionMachine']

    ## Retorna o id do algoritmo executado
    ## @param self objeto do tipo job.
    ## @return o id do algoritmo.
    def getAlgorithmId(self):
        return self._me['algorithmId']

    ## Retorna o timestamp de criação do job
    ## @param self objeto do tipo job.
    ## @return o timestamp.
    def getsubmissiontime(self):
        return self._me['submissionTime']

    ## Retorna o timestamp da ultima modificação do job
    ## @param self objeto do tipo job.
    ## @return o timestamp.
    def getlastmodifiedtime(self):
        return self._me['lastModifiedTime']

    ## Atualiza estruturas internas com base em um dicionário 
    ## @param self objeto.
    ## @param info dicionário informativo
    def _updateme(self, info):
        if info is None:
           raise CsPyException("info for job cannot be none!")
        self._me['jobId'] = info['jobId']
        self._me['algorithmId'] = info['algorithmId']
        self._me['algorithmVersion'] = info['algorithmVersion']
        self._me['algorithmName'] = info['algorithmName']
        self._me['executionMachine'] = info['executionMachine']  
        self._me['state'] = info['state']
        dataRep = [ int(x) for x in re.split( '[:T.-]', info['lastModifiedTime']) ]
        data = datetime(*dataRep)
        self._me['lastModifiedTime'] = int(data.timestamp())
        dataRep = [ int(x) for x in re.split( '[:T.-]', info['submissionTime']) ]
        data = datetime(*dataRep)
        self._me['submissionTime'] = int(data.timestamp())
        cnn = self.getconnection()
        # a resposta de job não traz todas as infos do usuario
        userInfo = { 'owner': {'id':info['jobOwner'],'name': info['jobOwnerName'], 'login':''} }
        self._fillme(userInfo, 'owner', 'owner', lambda infovalue: CsPyUser(cnn, infovalue))
        # self._fillme(info, 'version', 'Version', lambda infovalue: CsPyAlgorithmVersion(self, cnn, infovalue))
        # self._updateversions(info.get('versions'))
        

    ## Consulta representação textual.
    ## @param self objeto.
    ## @return texto
    def __str__(self):
        myid = self.getid()
        algoId = self.getalgorithmid()
        owner = self.getowner()
        return "job: " + myid + " - algoritmId" + algoId + " (Owner: " + str(owner) + ") " + "state: " + self.getState()

    ## Consulta representação textual.
    ## @param self objeto.
    ## @return texto
    def __repr__(self):
        return self.__str__()
