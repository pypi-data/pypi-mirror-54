
from cspybase.core.exception import CsPyException
from cspybase.core.access import CsPyAccess
from cspybase.job.job import CsPyJob

## Classe que representa um acesso bem sucedido a um servidor.
class CsPyJobAccess(CsPyAccess):

    ## Construtor
    ## @param self objeto do tipo acesso
    ## @param connection conexão previamente estabelecida.
    def __init__(self, connection):
        super().__init__(connection)


    ## Consulta a lista de jobs em um determinado projeto
    ## @param self objeto do tipo acesso
    ## @param projectId id do projeto
    ## @return uma tupla com os jobs.
    def getjobs(self, projectId):
        if projectId:
            info = { 'q': "projectId==\"{}\"".format(projectId) }
        else:
            info = {}
        jobs = self.getconnection().get(self.getjobspath(), info,True)
        joblist = []
        jobit = iter(jobs['jobs'])
        for job in jobit:
            if not job:
                print('error!')
            joblist.append(CsPyJob(self.getconnection(), job))
        return tuple(joblist)

    ## Consulta de um job
    ## @param self objeto do tipo acesso
    ## @param jobId id do projeto
    ## @return um job.
    def getjob(self, jobId): 
        resp = self.getconnection().get(self.getjobspath() + '/' + jobId , {})
        return CsPyJob( self.getconnection(), resp)

    ## faz submit de um job
    ## @param self objeto do tipo access
    ## @param algorithm objeto do tipo algorithm
    ## @projectId string com o id do projeto onde o job deve ser guardado
    ## @info dicionario com os parametros de execução 
    def submitjob(self, algorithmid, versionid , projectId, info):
        params = {
                "remoteCommand": {
                    'algorithmId':algorithmid,
                    'projectId': projectId,
                    'versionId': versionid
                },
                "args": info['args'], # parametros do algoritimo
                "description": info['description'],
                "priority": info['priority'],
                "email": 
                    info['email']
                ,
                "emailOnTerminated": False,
                "candidateMachines": [ ],
                "numberOfJobs": 1
                }
        return self.getconnection().post(self.getjobspath(), params,isJsonContent=True)

    ## Faz o polling do job e retorna o estado do job além de usas informaçoes
    ## @param self objeto do tipo access
    ## @projectId string com o id do projeto onde o job deve ser guardado
    ## @jobid string com o id do job a ser consultado
    ## @date timestamp em segundos 
    ## returns: uma lista com 2 elementos: [0]: string com o estado do job ou False em caso de erro
    ##                                     [1]: resposta da requisição com as infos do job
    def pulljob(self, projectid, jobid, date = 0):
        info = {
            'projectId': projectid,
            'jobId': jobid,
            'date': date
        }
        resp = self.getconnection().get( self.getjobspullpath(), info , True )
        if 'jobs' in resp:
            state = resp['jobs'][0]['state']
        else:
            state = False
        return state, resp

    ## Fica fazendo o pooling do job e só retorna quando o Job termina
    ## @projectId string com o id do projeto onde o job deve ser guardado
    ## @jobid string com o id do job a ser consultado
    ## @date timestamp em segundos
    ## @maxtimeouts numero max de timeouts antes de retornar [opcional]. obs 0 == sem limite de timeout
    ## returns True quando o job chega ao estado de finished, false caso tenha atingido o numero max de timeouts sem chegar em finished
    def waitforjob( self, projectid, jobid, date, verbose = False, maxtimeouts = None ):
        info = {
            'projectId': projectid,
            'jobId': jobid,
            'date': date
        }
        state = ""
        lastState = state
        timeouts = 0
        while state != "FINISHED":
            resp = self.getconnection().get( self.getjobspullpath(), info , True )            
            info['date'] = resp['date']
            if 'jobs' not in resp:
                timeouts += 1
                if maxtimeouts and maxtimeouts < timeouts:
                    if verbose:
                        print('Max timeouts achieved, returning from "waitforjob"')
                    return False
                continue
            state = resp['jobs'][0]['state']
            if verbose and lastState != state:
                lastState = state
                print('Job {} state: {}'.format(jobid,state))

        return True
    
    ## Cancela os jobs recebidos por parametro
    ## @jobids lista de strings contendo o id dos jobs a serem cancelados
    def canceljobs(self, jobids):
        info = {
            'jobIds': jobids
        }
        try: # Só vai continuar no fluxo normal se receber 200
            self.getconnection().post( self.getjobscancelpath(), info )
            return True
        except CsPyException as e:
            print(e)
            return False
