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
        status_code = response.status_code
        status_codes = self.response_status_codes
        status_codes[401] = "Invalid credentials and/or API token"

        if (status_code != 200):
            raise Exception(status_codes[status_code])

        self.token = response.json()['token']
        self.getHeader['Authorization'] = 'Bearer ' + self.token

    def refresh_token(self):
        url = self.url + '/refresh_token'
        
        assert 'Authorization' in self.getHeader
        response = requests.get(url, headers=self.getHeader)

        assert response.status_code == 200
        self.token = response.json()['token']
        self.getHeader['Authorization'] = 'Bearer ' + self.token
