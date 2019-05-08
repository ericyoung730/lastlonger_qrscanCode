from JWT import Jwt, jwt
from Util import randHex
import requests, time

'''
API document: https://api.goodtogo.tw/#api-Containers-Containers_rent_container
You can look up all the meaning of status code with the corresponding endpoints in document
'''

baseUrl = 'https://app.goodtogo.tw'

class Uri:
    login = '/users/login'
    userToken = '/stores/getUser/'
    socketToken = '/containers/challenge/token'
    returnContainer = '/containers/return/'
    lendContainer = '/containers/rent/'
    usedAmount = '/stores/usedAmount'

class Api:    
    ver = 'test'

    def __init__(self):
        self.apiKey = '0ad1995bbd'
        self.secretKey = 'DgA/uuv8ZgO0dOWG'

    def setAuthorization(self, apiKey, secretKey):
        '''
        Description   - set the authorization info
        Parameters    - api key(string)
                        secret key(string)
        Return values - N/A
        '''
        self.apiKey = apiKey
        self.secretKey = secretKey

    def login(self, username, password):
        '''
        This api is no longer need to be called since it's using a bot account currently.
        '''
        headers = {'reqID': randHex(10), 'reqTime': str(time.time()*1000) }
        body = { 'phone': username, 'password': password}
        r = requests.post(baseUrl+'/'+self.ver+Uri.login, data = body, headers = headers)
        encoded = r.headers['Authorization']
        payload = jwt.decode(encoded, algorithms=['HS256'], verify=False)
        self.secretKey = payload['roles']['clerk']['secretKey']
        self.apiKey = payload['roles']['clerk']['apiKey']
        return (self.apiKey, self.secretKey)

    def fetchSocketNamespaceAndToken(self):
        '''
        Description   - Fetch crucial information used for connecting to server websocket
        Parameters    - N/A
        Retrun values - status code(number), 
                        token(string)
                        real uri(string)                         
        '''
        headers = { 'Authorization': Jwt.standard(self.secretKey), 'apiKey': self.apiKey }
        r = requests.get(baseUrl+'/'+self.ver+Uri.socketToken, headers = headers)
        json = r.json()
        print(json)
        (token, uri) = (json['token'], json['uri'])
        return (r.status_code, token, uri)

    def returnContainer(self, id):
        '''
        Description   - Mark a container as taken back from an user
        Parameters    - id: containerId
        Return values - status code(number)
                        previous host(string)
                        container id(string)
                        container type(string)
        '''
        headers = {'Authorization': Jwt.addDate(self.secretKey), 'apiKey': self.apiKey, 'Content-Type': 'application/json'}
        r = requests.post(baseUrl+'/'+self.ver+Uri.returnContainer+str(id), headers = headers, json={'storeId': 17})
        if r.status_code == 200:
            if (r.json()['message'] == 'Already Return'):
                return (r.status_code, user, None, None)
            container = r.json()['containerList'][0]
            user = r.json()['oriUser']
            return (r.status_code, user, str(container['id']), container['typeName'])
        else:
            return (r.status_code, '', '', '')

    def rentContainer(self, id, userApiKey):
        '''
        Description   - Rent a container to an user
        Parameters    - id: container id
                        userApiKey: the apiKey of the user, you can get it by calling `fetchUserToken(self, user)`
        Return values - status code(number)
        '''
        headers = {'Authorization': Jwt.addDate(self.secretKey), 'apiKey': self.apiKey, 'userApiKey': userApiKey}
        r = requests.post(baseUrl+'/'+self.ver+Uri.lendContainer+str(id), headers=headers)
        return (r.status_code)


    def fetchUserToken(self, user):
        '''
        Description   - fetch the apiKey of a specific user
        Parameters    - user: phone number of the user
        Return values - status code(number)
                        api key(string)
        '''
        headers = {'Authorization': Jwt.standard(self.secretKey), 'apiKey': self.apiKey}
        r = requests.get(baseUrl+'/'+self.ver+Uri.userToken+user, headers = headers)
        if r.status_code == 200:
            json = r.json()
            return (r.status_code, json['apiKey'])
        else:
            return (r.status_code, '')

    def usedAmount(self):
        '''
        Description   - get used amount of this bot
        Parameters    - N/A
        Return values - status code(number)
                        total amount of used containers(number)
        '''
        headers = {'Authorization': Jwt.standard(self.secretKey), 'apiKey': self.apiKey}
        r = requests.get(baseUrl+'/'+self.ver+Uri.usedAmount, headers = headers)
        json = r.json()
        storeRecords = json['store']

        total = 0

        if r.status_code == 200:
            for record in storeRecords:
                total += record['amount']
            return (r.status_code, total)
        else:
            return (r.status_code, 0)
