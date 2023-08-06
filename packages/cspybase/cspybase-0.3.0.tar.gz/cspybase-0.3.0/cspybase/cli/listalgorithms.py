from cspybase.algorithm.access import CsPyAlgorithmAccess

from cspybase.cli.core import createconnection


def main():
    connection = createconnection()
    access = CsPyAlgorithmAccess(connection)
    algos = access.getalgorithms()
    for a in algos:
        print(a)
    connection.disconnect()
