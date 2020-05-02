import requests
import json

class tvdb:

    url = 'https://api.thetvdb.com'

    postHeader = {'Content-Type': 'application/json'}
    getHeader = {'Accept': 'application/json'}

    token = '' 

    response_status_codes = {
        200:"success"
    }

    def __handleException(self, status_codes, status_code):
        if (status_code != 200):
            raise Exception(status_codes[status_code])

    def __init__(self, userkey, apikey, username):
        self.userkey = userkey
        self.apikey = apikey
        self.username = username
        self.login()

    def login(self):
        url = self.url + '/login'
        data = {
            'userkey':self.userkey,
            'apikey':self.apikey,
            'username':self.username
        }
        response = requests.post(url, data=json.dumps(data), headers=self.postHeader)
        status_codes = self.response_status_codes
        status_codes[401] = "Invalid credentials and/or API token"
        self.__handleException(status_codes, response.status_code)
        self.token = response.json()['token']
        self.getHeader['Authorization'] = 'Bearer ' + self.token

    def refresh_token(self):
        url = self.url + '/refresh_token'
        assert 'Authorization' in self.getHeader
        response = requests.get(url, headers=self.getHeader)
        status_codes = self.response_status_codes
        status_codes[401] = "Returned if your JWT token is missing or expired"
        self.__handleException(status_codes, response.status_code)
        self.token = response.json()['token']
        self.getHeader['Authorization'] = 'Bearer ' + self.token

    def episodes(self, id):
        url = self.url + '/episodes/{}'.format(id)
        assert 'Authorization' in self.getHeader
        response = requests.get(url, headers=self.getHeader)
        status_codes = self.response_status_codes
        status_codes[401] = "Returned if your JWT token is missing or expired"
        status_codes[404] = "Returned if the given episode ID does not exist"
        self.__handleException(status_codes, response.status_code)
        assert response.headers.get('content-type') == 'application/json; charset=utf-8'
        return response.json()