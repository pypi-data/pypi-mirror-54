
from cspybase.job.access import CsPyJobAccess
from cspybase.project.access import CsPyProjectAccess
from cspybase.cli.core import createconnection, chooseprojectname


def main():
    connection = createconnection()
    prjaccess = CsPyProjectAccess(connection)
    projectname = chooseprojectname()
    if projectname is None:
        connection.disconnect()
        return

    project = prjaccess.getproject(projectname)
    prjid = project.getid()
    jobaccess = CsPyJobAccess(connection)
    jobs = jobaccess.getjobs(prjid)
    for j in jobs:
        print(j)
    connection.disconnect()
