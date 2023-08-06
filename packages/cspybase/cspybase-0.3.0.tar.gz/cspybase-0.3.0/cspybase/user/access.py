
## @package access
## Módulo responsável pelo acesso (já estabelecido por conexão) a um sistema CSBase

from cspybase.core.access import CsPyAccess
from cspybase.user.user import CsPyUser


## Classe que representa um acesso bem sucedido a um servidor.
class CsPyUserAccess(CsPyAccess):

    ## Construtor
    ## @param self objeto do tipo acesso
    ## @param connection conexão previamente estabelecida.
    def __init__(self, connection):
        super().__init__(connection)

    ## Consulta a lista de usuários do sistema
    ## @param self objeto do tipo acesso
    ## @return uma tupla com objeto do tipo usuário
    def getusers(self):
        users = self.getconnection().get(self.getuserspath(), {})
        userslist = []
        usersiter = iter(users)
        for user in usersiter:
            userslist.append(CsPyUser(self.getconnection(), user))
        return tuple(userslist)

    ## Retorna um usuário com base em seu id
    ## @param self objeto do tipo acesso
    ## @param userid o id a ser pesquisado
    ## @return o usuário ou None (caso este não seja encontrado)
    def getuser(self, userid):
        users = self.getusers()
        for usr in users:
            if usr.getid() == userid:
                return usr
        return None

