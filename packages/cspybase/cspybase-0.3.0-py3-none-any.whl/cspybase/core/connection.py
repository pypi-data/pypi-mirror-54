## @package connection
## Módulo responsável pelo controle de acesso (conexão) a um sistema CSBase

import http.client
import urllib.parse
import json
import tempfile
import os

import requests

from cspybase.core.exception import CsPyException

## Classe de conexão a um servidor CSBase.
class CsPyConnection:
    
    ## Construtor
    ## @param host endereço do servidor do sistema
    ## @param port porta opcional a ser utilizada (o default é 8010)
    def __init__(self, host, port = 8010):
        self._host = host
        self._port = port
        self._token = None
        self._userid = None
        self._isconnected = False
        self._setunconnected()
        self._connection = http.client.HTTPConnection(host, port)

    ## Inicia uma conexão com base em um login/senha
    ## @param login id/login do usuário
    ## @param password senha
    ## @return True ou False se a conexão foi bem sucedida
    def connectwithlogin(self, login, password):
        try:
           self._setunconnected()
           params = {'login': login, 'password': password}
           data = self.post("/v1/authentication", params)
           return self._setconnected(data['accessToken'], data['user']['id'])
        except Exception:
           return self._setunconnected()

    ## Inicia uma conexão com base em um token
    ## @param token token
    ## @return True ou False se a conexão foi bem sucedida
    def connectwithtoken(self, token):
        try:
           self._setunconnected()
           params = {'userToken': token, 'validationType': 'access' }
           data = self.post("/v1/authentication/token/validation", params)
           if not data['valid']:
              raise Exception("invalid token!") 
           return self._setconnected(token, 'no-user')
        except Exception as e:
           return self._setunconnected()

    ## Inicia uma conexão com base em um protocolo de acesso automático com base em uma variável de ambiente 'CS_AUTH_TOKEN'
    ## @return True ou False se a conexão foi bem sucedida
    def autoconnect(self):
        varname = 'CS_AUTH_TOKEN'
        varvalue = os.environ.get(varname)
        if varvalue is None:
           return self._setunconnected()
        return self.connectwithtoken(varvalue)

    ## Consulta a URL de conexão
    ## @return a URL
    def geturl(self):
        return "http://" + str(self.gethost()) + ":" + str(self.getport())

    ## Consulta a máquina de conexão
    ## @return a máquina
    def gethost(self):
        return self._host

    ## Consulta a porta da conexão
    ## @return a porta
    def getport(self):
        return self._port

    ## Consulta o token da conexão
    ## @return o token (se houver) ou None (caso não haja conexão)
    def gettoken(self):
        return self._token

    ## Faz a desconexão ao sistema CSBase
    def disconnect(self):
        self._connection.close()
        self._setunconnected()

    ## Verifica se há conexão estabelecida
    ## @return indicativo (True ou False)
    def isconnected(self):
        return self._isconnected

    ## Consulta o id do usuário da conexão
    ## @return o identificador do usuário (se houver)
    def getuserid(self):
        return self._userid

    def post(self, path, parameters = {}, urlParams=False, isJsonContent = False):
        return self._request("POST", path, parameters,urlParams, isJsonContent)


    def get(self, path, parameters = {}, urlParams=False):
        return self._request("GET", path, parameters,urlParams)


    def delete(self, path, parameters = {}, urlParams=False):
        return self._request("DELETE", path, parameters,urlParams)

    def touch(self, path, remotefilename):
        tmpname = tempfile.mktemp()
        tmpfile = open(tmpname, "wb")
        tmpfile.close()
        self.upload(path, tmpname, remotefilename)
        os.remove(tmpname)
    
    def upload(self, path, localfilename, remotefilename):
        hds = {}
        if self.isconnected():
           hds['Authorization'] = "Bearer " + self.gettoken()
        prs = {}
        fls = {'file' : (remotefilename, open(localfilename, 'rb')) }
        dts = {'uploadType': 'multipart'}
        url = self.geturl() + path
        response = requests.post(url, files=fls, headers=hds, params=prs, data=dts)
        if response.status_code >= 400:
           code = str(response.status_code)
           reason = str(response.reason)
           raise CsPyException("Request post to [" + url + "] failed. Status: " + code + " - " + reason)


    def _encodeparams(self, paramsdict, isJobPost = False):
        if isJobPost:
            return json.dumps(paramsdict)
        return urllib.parse.urlencode(paramsdict)


    def _encodeheaders(self, isJsonContent = False):
        if isJsonContent:
            hds = { "Content-type": "application/json" }
        else:
            hds = { "Content-type": "application/x-www-form-urlencoded",  "Accept": "application/json" }
        if self.isconnected():
           hds['Authorization'] = "Bearer " + self.gettoken()
        return hds

    def _request(self, requesttype, path, parameters, urlParams=False, isJsonContent = False):
        headers = self._encodeheaders(isJsonContent)
        params = self._encodeparams(parameters,isJsonContent)
        #self._connection.set_debuglevel(1) #ajuda no debug das chamadas http
        if urlParams:
            self._connection.request(requesttype, path + "?" + params,self._encodeparams({}), headers)    
        else:
            self._connection.request(requesttype, path, params, headers)
        response = self._connection.getresponse()
        if response.status >= 400:
           statusstr = str(response.status)
           reasonstr = str(response.reason)
           data = response.read().decode('utf-8')
           raise CsPyException("Request to [" + path + "] failed. Status: " + statusstr + " - " + reasonstr + "| \ninfo: "+ data)
        data = response.read().decode('utf-8')
        if not data or data is None:
           return None
        if isJsonContent:
            return data
        return json.loads(data)

    def _setconnected(self, token, userid):
        self._token = token
        self._userid = userid
        self._isconnected = True
        return True

    def _setunconnected(self):
        self._token = None
        self._userid = None
        self._isconnected = False
        return False

    

