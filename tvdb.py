import requests
import json

class tvdb:

    url = 'https://api.thetvdb.com'

    postHeader = {'Content-Type': 'application/json'}
    getHeader = {'Accept': 'application/json'}

    token = '' 

    response_status_codes = {
        200:"success",
        404:"Resource not found"
    }

    def __handleStatusCodes(self, status_codes, status_code):
        if (status_code != 200):
            raise Exception(status_codes[status_code])

    def __init__(self, userkey, apikey, username):
        self.userkey = userkey
        self.apikey = apikey
        self.username = username
        self.login()

    def login(self):
        #setup url
        url = self.url + '/login'
        
        #get response
        data = {
            'userkey':self.userkey,
            'apikey':self.apikey,
            'username':self.username
        }
        response = requests.post(url, data=json.dumps(data), headers=self.postHeader)

        #setup response code exceptions
        status_codes = self.response_status_codes
        status_codes[401] = "Invalid credentials and/or API token"

        #hanlde response status codes
        self.__handleStatusCodes(status_codes, response.status_code)

        #perform function
        assert 'application/json' in response.headers.get('content-type')
        assert 'token' in response.json()
        self.token = response.json()['token']
        self.getHeader['Authorization'] = 'Bearer ' + self.token

    def refresh_token(self):
        #setup url
        url = self.url + '/refresh_token'

        #get reponse
        assert 'Authorization' in self.getHeader
        response = requests.get(url, headers=self.getHeader)

        #setup response code exceptions
        status_codes = self.response_status_codes
        status_codes[401] = "Returned if your JWT token is missing or expired"

        #handle response status codes
        self.__handleStatusCodes(status_codes, response.status_code)
        
        #perform function
        assert 'application/json' in response.headers.get('content-type')
        assert 'token' in response.json()
        self.token = response.json()['token']
        self.getHeader['Authorization'] = 'Bearer ' + self.token

    def episodes(self, id, Accept_Language=None):
        #setup url
        url = self.url + '/episodes/{}'.format(id)

        #get response
        assert 'Authorization' in self.getHeader
        headers = self.getHeader
        headers['Accept-Language'] = Accept_Language
        response = requests.get(url, headers=headers)

        #setup response code exceptions
        status_codes = self.response_status_codes
        status_codes[401] = "Returned if your JWT token is missing or expired"
        status_codes[404] = "Returned if the given episode ID does not exist"

        #handle response status codes
        self.__handleStatusCodes(status_codes, response.status_code)

        #perform function
        assert 'application/json' in response.headers.get('content-type')
        return response.json()

    def __languages0(self):
        #setup url
        url = self.url + '/languages'

        #get response
        assert 'Authorization' in self.getHeader
        response = requests.get(url, headers=self.getHeader)

        #setup response code exceptions
        status_codes = self.response_status_codes
        status_codes[401] = "Returned if your JWT token is missing or expired"

        #hanlde response status codes
        self.__handleStatusCodes(status_codes, response.status_code)

        #perform function
        assert 'application/json' in response.headers.get('content-type')
        return response.json()

    def __languages1(self, id):
        #setup url
        url = self.url + '/languages/{}'.format(id)

        #get response
        assert 'Authorization' in self.getHeader
        headers = self.getHeader
        response = requests.get(url, headers=headers)

        #setup response code exceptions
        status_codes = self.response_status_codes
        status_codes[401] = "Returned if your JWT token is missing or expired"
        status_codes[404] = "Returned if the given language ID does not exist"

        #hanlde response status codes
        self.__handleStatusCodes(status_codes, response.status_code)

        #perform function
        assert 'application/json' in response.headers.get('content-type')
        return response.json()

    def languages(self, *arg):
        if len(arg) == 0:
            return self.__languages0()
        return self.__languages1(*arg)

    def movies(self, id, Accept_Language=None):
        #setup url
        url = self.url + '/movies/{}'.format(id)

        #get response
        assert 'Authorization' in self.getHeader
        headers = self.getHeader
        headers['Accept-Language'] = Accept_Language
        response = requests.get(url, headers=headers)

        #setup response code exceptions
        status_codes = self.response_status_codes
        status_codes[401] = "Returned if your JWT token is missing or expired"
        status_codes[404] = "Returned if the given series ID does not exist"

        #hanlde response status codes
        self.__handleStatusCodes(status_codes, response.status_code)

        #perform function
        assert 'application/json' in response.headers.get('content-type')
        return response.json()

    def movieupdates(self, since):
        #setup url
        url = self.url + '/movieupdates?since={}'.format(since)

        #get response
        assert 'Authorization' in self.getHeader
        headers = self.getHeader
        response = requests.get(url, headers=headers)

        #setup response code exceptions
        status_codes = self.response_status_codes
        status_codes[401] = "Returned if your JWT token is missing or expired"
        status_codes[405] = "Missing query params are given"
        status_codes[422] = "Invalid params provided"

        #hanlde response status codes
        self.__handleStatusCodes(status_codes, response.status_code)

        #perform function
        assert 'application/json' in response.headers.get('content-type')
        return response.json()

    def searchSeries(self, **args):
        #setup url
        url = self.url + '/search/series'

        #get response
        assert 'Authorization' in self.getHeader
        headers = self.getHeader
        if 'Accept_Language' in args:
            headers['Accept-Language'] = str(args['Accept_Language'])
            del args['Accept_Language']
        response = requests.get(url, headers=headers, params=args)

        #setup response code exceptions
        status_codes = self.response_status_codes
        status_codes[401] = "Returned if your JWT token is missing or expired"
        status_codes[404] = "Returned if no records are found that match your query"
        status_codes[405] = "Requires only one of name, imdbId, zap2itId, slug params"

        #hanlde response status codes
        self.__handleStatusCodes(status_codes, response.status_code)

        #perform function
        assert 'application/json' in response.headers.get('content-type')
        return response.json()

    def searchSeriesParams(self):
        #setup url
        url = self.url + '/search/series/params'

        #get response
        assert 'Authorization' in self.getHeader
        headers = self.getHeader
        response = requests.get(url, headers=headers)

        #setup response code exceptions
        status_codes = self.response_status_codes
        status_codes[401] = "Returned if your JWT token is missing or expired"

        #hanlde response status codes
        self.__handleStatusCodes(status_codes, response.status_code)

        #perform function
        assert 'application/json' in response.headers.get('content-type')
        return response.json()

    