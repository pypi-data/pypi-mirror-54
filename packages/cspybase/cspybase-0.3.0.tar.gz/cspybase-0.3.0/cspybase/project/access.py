
from cspybase.core.access import CsPyAccess
from cspybase.project.project import CsPyProject


## Classe que representa um acesso bem sucedido a um servidor.
class CsPyProjectAccess(CsPyAccess):

    ## Construtor
    ## @param self objeto do tipo acesso
    ## @param connection conexão previamente estabelecida.
    def __init__(self, connection):
        super().__init__(connection)

    ## Consulta a lista de projetos disponíveis para este acesso
    ## @param self objeto do tipo acesso
    ## @return uma tupla com os projetos.
    def getprojects(self):
        prjs = self.getconnection().get(self.getprojectspath(), {})
        prjlist = []
        itprjs = iter(prjs)
        for prj in itprjs:
            prjlist.append(CsPyProject(self.getconnection(), prj))
        return tuple(prjlist)

    ## Cria um novo projeto
    ## @param self objeto do tipo acesso
    ## @param name nome do novo projeto a ser criado
    ## @param description descrição do novo projeto (opcional)
    ## @return o novo projeto criado
    def createproject(self, name, description = None):
        if description is None:
           description = name
        params = {'name': name, 'description': description}
        info = self.getconnection().post(self.getprojectspath(), params)
        return CsPyProject(self.getconnection(), info)

    ## Retorna um projeto com base em seu nome
    ## @param self objeto do tipo acesso
    ## @param name o nome a ser pesquisado
    ## @return o projeto ou None (caso este não seja encontrado)
    def getproject(self, name):
        prjs = self.getprojects()
        for prj in prjs:
            if prj.getname() == name:
               return prj
        return None

    ## Retorna um projeto com base em seu nome
    ## @param self objeto do tipo acesso
    ## @param projectid o id a ser pesquisado
    ## @return o projeto ou None (caso este não seja encontrado)
    def getprojectbyid(self, projectid):
        prj = self.getconnection().get(self.getprojectspath() + '/' + projectid, {})
        print(prj)
        return prj

    ## Apaga um projeto com base em seu nome.
    ## @param self objeto do tipo acesso
    ## @param name o nome a ser apagado
    def deleteproject(self, name):
        prj = self.getproject(name)
        if prj is not None:
           prjid = prj.getid()
           self.getconnection().delete(self.getprojectspath() + "/" + prjid, {})

    ## Apaga um projeto com base em seu id.
    ## @param self objeto do tipo acesso
    ## @param id do projeto a ser apagado
    def deleteprojectbyid(self, id):
        self.getconnection().delete(self.getprojectspath() + "/" + id, {})
    

