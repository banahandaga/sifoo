# =========================================
# Created by Ridwan Renaldi, S.Kom. (rr867)
# =========================================
from django.conf import settings

import requests
import json
import jwt
import datetime
import os

class API_GATEWAY:
    url         = settings.API_GATEWAY_URL
    username    = ''
    password    = ''
    access      = ''
    refresh     = ''
    filename    = ''

    def __init__(self, username, password, filename=None):
        self.username = username
        self.password = password
        self.filename = 'token/{0}.json'.format(filename) if filename else 'token/{0}.json'.format(username)
        os.makedirs(os.path.dirname(self.filename), exist_ok=True)

    def checkRequest(self, response, get='data', convert=True):
        try:
            if response.status_code in [200,201,202,203]:
                responsejson = response.json()

                if convert:
                    if get == 'data':
                        if not responsejson['success']:
                            return { 
                                'status'    : False, 
                                'message'   : responsejson['message'],
                            }
                        
                        elif responsejson['records'] == 0:
                            return { 
                                'status'    : False, 
                                'message'   : 'Data Not Found',
                            }

                        else:
                            return { 
                                'status'    : True, 
                                'message'   : 'Success',
                                'records'   : responsejson['records'],
                                'data'      : responsejson['rows'],  
                            }
                    else:
                        result = { 
                            'status'    : True, 
                            'message'   : 'Success',
                            'records'   : 0,
                            'data'      : responsejson,  
                        }

                        try:
                            result['records'] = responsejson['records']
                        except Exception as e:
                            print('[Warning] : This request has no record field')

                        return result
                else:
                    return responsejson

            else:
                return { 
                    'status'    : False,
                    'message'   : 'There is an error {0}. Please contact the system admin'.format(response.status_code),
                }

        except requests.Timeout:
            return { 
                'status'    : False, 
                'message'   : 'Server took too long to respond. Please try again soon',
            }
            
        except requests.exceptions.ConnectionError:
            return { 
                'status'    : False, 
                'message'   : 'Failed to contact the API system, Please try again later',
            }

        except Exception as e:
            return { 
                'status'    : False,
                'message'   : '[Error] : {0}'.format(e),
            }



    def getNewToken(self):
        url = '%stoken/' % (self.url)
        body = { 'username' : self.username, 'password' : self.password }
        response = self.checkRequest( requests.post(url, data=body), 'token' )

        if response['status'] :

            with open(self.filename,'w') as file:
                json.dump(response['data'], file, indent=4)

            self.access = response['data']['access']
            self.refresh = response['data']['refresh']

            return response
        else:
            return response



    def getRefreshToken(self, refresh):
        url = '%stoken/refresh/' % (self.url)
        body = { 'refresh' : refresh }
        response = self.checkRequest( requests.post(url, data=body), 'token')

        if response['status'] :
            token = { "refresh": refresh, "access": response['data']['access'] }
            response['data'] = token

            with open(self.filename,'w') as file:
                json.dump(token, file, indent=4)

            self.refresh = refresh
            self.access = response['data']['access']

            return response
        else:
            return response



    def getToken(self):
        try:
            with open(self.filename) as file:
                data = json.load(file)

            decode_refresh = jwt.decode(data['refresh'], options={"verify_signature": False})
            decode_access = jwt.decode(data['access'], options={"verify_signature": False})
            exp_refresh = decode_refresh['exp']
            exp_access = decode_access['exp']

            # If the token has expired then take a new token
            datetimenow = datetime.datetime.now().timestamp()
            if exp_access <= datetimenow:
                if exp_refresh <= datetimenow:
                    return self.getNewToken()
                else:
                    return self.getRefreshToken(data['refresh'])
                    
            else:
                self.access = data['access']
                self.refresh = data['refresh']
                return {
                    'status'    : True,
                    'message'   : 'Managed to retrieve the old token',
                    'data'      : data,
                }

        except:
            return self.getNewToken()

    

    def get(self, suburl:str):
        gettoken = self.getToken()

        if gettoken['status']:
            url = self.url + suburl
            print('[Request GET] : '+url)
            header = { 'Authorization' : 'Bearer %s' % (self.access) }
            response = self.checkRequest( requests.get(url, headers=header) )

            if response['status'] :
                return {
                    'status'    : True,
                    'message'   : 'Success',
                    'data'      : response['data'],
                }
            else :
                return response
        else:
            return gettoken



    def post(self, suburl:str, data=None, files=None):
        gettoken = self.getToken()

        if gettoken['status']:
            url = self.url + suburl
            print('[Request POST] : '+url)
            header = { 'Authorization' : 'Bearer %s' % (self.access) }
            response = self.checkRequest( requests.post(url, headers=header, data=data, files=files) )

            if response['status'] :
                return {
                    'status'    : True,
                    'message'   : 'Success',
                    'data'      : response['data'],
                }
            else :
                return response
        else:
            return gettoken

    
    def put(self, suburl:str, data=None, files=None):
        gettoken = self.getToken()

        if gettoken['status']:
            url = self.url + suburl
            print('[Request PUT] : '+url)
            header = { 'Authorization' : 'Bearer %s' % (self.access) }
            response = self.checkRequest( requests.put(url, headers=header, data=data, files=files) )

            if response['status'] :
                return {
                    'status'    : True,
                    'message'   : 'Success',
                    'data'      : response['data'],
                }
            else :
                return response
        else:
            return gettoken
    

    def delete(self, suburl:str, data=None, files=None):
        gettoken = self.getToken()

        if gettoken['status']:
            url = self.url + suburl
            print('[Request DELETE] : '+url)
            header = { 'Authorization' : 'Bearer %s' % (self.access) }
            response = self.checkRequest( requests.delete(url, headers=header, data=data, files=files) )

            if response['status'] :
                return {
                    'status'    : True,
                    'message'   : 'Success',
                    'data'      : response['data'],
                }
            else :
                return response
        else:
            return gettoken


apigateway = API_GATEWAY(settings.API_GATEWAY_USERNAME, settings.API_GATEWAY_PASSWORD, 'apigateway')