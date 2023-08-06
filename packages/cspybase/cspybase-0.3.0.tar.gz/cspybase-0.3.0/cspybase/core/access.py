## @package access
## Módulo responsável pelo acesso (já estabelecido por conexão) a um sistema CSBase

from cspybase.project.project import CsPyProject
from cspybase.core.exception import CsPyException
from cspybase.core.object import CsPyObject
from cspybase.algorithm.algorithm import CsPyAlgorithm
from cspybase.job.job import CsPyJob


## Classe que representa um acesso bem sucedido a um servidor.
class CsPyAccess(CsPyObject):

    ## Construtor
    ## @param self objeto do tipo acesso
    ## @param connection conexão previamente estabelecida.
    def __init__(self, connection):
        super().__init__(connection)

