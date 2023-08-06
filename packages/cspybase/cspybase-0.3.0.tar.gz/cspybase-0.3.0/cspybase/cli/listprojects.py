
from cspybase.project.access import CsPyProjectAccess
from cspybase.cli.core import createconnection


def main():
    connection = createconnection()
    access = CsPyProjectAccess(connection)
    projects = access.getprojects()
    for p in projects:
        print(p)
    connection.disconnect()
