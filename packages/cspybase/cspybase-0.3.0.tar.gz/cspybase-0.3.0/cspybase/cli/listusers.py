
from cspybase.user.access import CsPyUserAccess
from cspybase.cli.core import createconnection


def main():
    connection = createconnection()
    access = CsPyUserAccess(connection)
    users = access.getusers()
    for u in users:
        print(u)
    connection.disconnect()
