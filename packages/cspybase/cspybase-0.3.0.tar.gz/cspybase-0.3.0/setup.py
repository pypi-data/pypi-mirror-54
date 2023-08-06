""" Setup """

import io
import os
import re

from setuptools import setup, find_packages
from codecs import open
from os import path


def read(*names, **kwargs):
    with io.open(
        os.path.join(os.path.dirname(__file__), *names),
        encoding=kwargs.get("encoding", "utf8")
    ) as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


here = path.abspath(path.dirname(__file__))

# Pegando descrição do arquivo.
with open(path.join(here, 'DESCRIPTION.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    # Nome do pacote
    name='cspybase',

    # Detalhes em:
    # https://packaging.python.org/en/latest/single_source_version.html
    version=find_version("cspybase/__init__.py"),

    # Descrição
    description='A Python CSBase binding',

    long_description=long_description,
    long_description_content_type='text/markdown',

    # Página do projeto
    url='https://git.tecgraf.puc-rio.br/csrxbase/cspybase',

    # Autor
    author='André Luiz Clinio',
    author_email='clinio@tecgraf.puc-rio.br',

    # Licença
    license='Other/Proprietary License',

    # Ver https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[

        # Estado
        'Development Status :: 1 - Planning',

        # Tópico e audiência
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',

        # Licença
        'License :: Other/Proprietary License',

        # Versões de Python
        'Programming Language :: Python :: 3 :: Only',
    ],

    # Palavras chave
    keywords='csbase gridcomputing',

    # Listagem de pacotes
    packages=['cspybase', 'cspybase.core'],
    package_dir={'cspybase': 'cspybase'},

    # Dependências de runtime
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=['requests'],

    # Grupo de dependências. Exemplo:
    # $ pip install -e .[dev,test]
    extras_require={
        'dev': ['check-manifest', 'wheel'],
        'doc': [],
        'test': [],
    },

    # Arquivos de dados
    package_data={
    },

    # Scripts executáveis
    entry_points={
        'console_scripts': [
           'list-algorithms = cspybase.cli.listalgorithms:main',
           'list-jobs = cspybase.cli.listjobs:main',
           'list-users = cspybase.cli.listusers:main',
           'list-projects = cspybase.cli.listprojects:main',
           'list-files = cspybase.cli.listfiles:main',
           'get-token = cspybase.cli.gettoken:main',
        ],
    }
)
