import csv

from cspybase.cli.core import createconnection
from cspybase.cli.core import chooseprojectname
from cspybase.project.access import CsPyProjectAccess


def main():
    connection = createconnection()
    access = CsPyProjectAccess(connection);
    projectname = chooseprojectname()
    project = access.getproject(projectname)
    rootdir = project.getroot()
    csvfile = rootdir.openfile("teste.csv", "wt")
    spamwriter = csv.writer(csvfile, delimiter=' ',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    spamwriter.writerow(['Spam'] * 5 + ['Baked Beans'])
    spamwriter.writerow(['Spam', 'Lovely Spam', 'Wonderful Spam'])
    csvfile.close()

    connection.disconnect()
