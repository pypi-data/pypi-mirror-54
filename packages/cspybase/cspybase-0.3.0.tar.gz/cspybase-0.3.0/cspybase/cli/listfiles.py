
from cspybase.project.access import CsPyProjectAccess
from cspybase.cli.core import createconnection, chooseprojectname


def main():
    connection = createconnection()
    access = CsPyProjectAccess(connection)
    projectname = chooseprojectname()
    if (projectname is None):
        connection.disconnect()
        return

    project = access.getproject(projectname)
    root = project.getroot()
    files = root.list()
    for f in files:
        print(f)
    connection.disconnect()
