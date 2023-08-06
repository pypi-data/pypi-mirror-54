
from cspybase.cli.core import createconnection


def main():
    connection = createconnection()
    token = connection.gettoken()
    print('Token', token)
    connection.disconnect()
