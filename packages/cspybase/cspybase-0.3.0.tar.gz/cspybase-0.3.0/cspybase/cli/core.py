
import getpass


from cspybase.core.connection import CsPyConnection
from cspybase.core.exception import CsPyUnconnectedException


def chooseprojectname():
    projectname = input("project name [teste]: ") or "teste"
    return projectname


def createconnection():
    hostname = input("Host name [localhost]: ") or "localhost"
    user = input("User name [admin]: ") or "admin"
    password = getpass.getpass(prompt="Password: ")
    connection = CsPyConnection(hostname)
    connected = connection.connectwithlogin(user, password)
    if not connected:
        raise CsPyUnconnectedException()
    return connection
