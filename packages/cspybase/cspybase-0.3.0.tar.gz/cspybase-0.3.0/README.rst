A CSBase for Python
===================

Just planning...


Comandos Úteis
--------------

Montagem de programas CLI

>>> python setup.py develop


Publicação

>>> pip install twine
>>> python setup.py sdist bdist_wheel
>>> cspybase/
>>> │
>>> └── dist/
>>>     ├── cspybase-1.0.0-py3-none-any.whl
>>>     └── cspybase-1.0.0.tar.gz
>>> tar tzf dist/cspybase-1.0.0.tar.gz 
>>> twine check dist/*
>>> twine upload --repository-url https://cspybase.pypi.org/legacy/ dist/*
>>> twine upload dist/*
