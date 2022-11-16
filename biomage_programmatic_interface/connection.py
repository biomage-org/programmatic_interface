import boto3
import requests
import biomage_programmatic_interface.exceptions as exceptions

class Connection:
    def __init__(self, username, password, instance_url, verbose=True):
        self.verbose = verbose
        self.__api_url = self.__get_api_url(instance_url)
        cognito_params = self.__get_cognito_params().json()
        clientId = cognito_params['clientId']
        region = cognito_params['clientRegion']
        self.__authenticate(username, password, clientId, region)

    def fetch_api(self, url, json, method='POST'):
        methods = {
            'POST': requests.post,
            'PATCH': requests.patch,
            'GET': requests.get
        }

        headers = {
            'Authorization': 'Bearer ' + self.__jwt,
            'Content-Type': 'application/json'
        }

        return methods[method](self.__api_url + url, json=json, headers=headers)

    def upload_to_S3(self, signed_url, file_path):
        headers = { 'Content-type': 'application/octet-stream' }
        with open(file_path, 'rb') as file:
            response = requests.put(signed_url, headers = headers, data = file.read())
            print(response.content)

    def __get_cognito_params(self):
        try:
            return requests.get(self.__api_url + 'v2/programmaticInterfaceClient')
        except Exception as e:
            raise exceptions.InstanceNotFound() from None

    def __authenticate(self, username, password, clientId, region):
        client = boto3.client('cognito-idp', region_name=region)

        try:
            resp = client.initiate_auth(
                ClientId=clientId,
                AuthFlow='USER_PASSWORD_AUTH',
                AuthParameters = { 
                    "USERNAME": username,
                    "PASSWORD": password
                }
            )
        except Exception as e:
            raise exceptions.IncorrectCredentials() from None

        print('Authorization succesfull') if self.verbose else ""

        self.__jwt = resp['AuthenticationResult']['IdToken']
    
    def __get_api_url(self, instance_url):
        if instance_url == 'local':
            return 'http://localhost:3000/'
        if instance_url.startswith('https://'):
            return instance_url
        return f'https://api.{instance_url}/'