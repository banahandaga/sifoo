# =========================================
# Created by Ridwan Renaldi, S.Kom. (rr867)
# =========================================
from django.conf import settings
from urllib.parse import urlencode
import requests
import json
import os


# =================[NOTE]================
# https://eu.wablas.com/documentation/api

class API_WABLAS:
    url       = settings.WABLAS_URL
    token     = ''

    def __init__(self, token):
        self.token = token
    

    def logprint(self, function, message):
        print('[WABLAS-{function}] : {message}'.format(function=function, message=message))


    def urlformat(self, suburl, params=None):
        if params:
            params = urlencode(params)
            return '{mainurl}/api/{suburl}?{params}'.format(mainurl=self.url, suburl=suburl, params=params)
        else:
            return '{mainurl}/api/{suburl}'.format(mainurl=self.url, suburl=suburl)


    def getToken(self):
        return self.token
    

    def CheckPhone(self, phone:str):
        params = { 'phones' : phone }
        url = 'https://phone.wablas.com/check-phone-number?{}'.format(urlencode(params))
        self.logprint('CheckPhone', url)
        header = { 'Authorization' : self.token, 'url' : self.url }
        response = requests.get(url, headers=header)
        return response.json()
    

    def DeviceInfo(self):
        params = { 'token' : self.token }
        url = self.urlformat('device/info', params)
        self.logprint('DeviceInfo', url)
        header = { 'Authorization' : self.token }
        response = requests.get(url, headers=header)
        return response.json()
    

    def SendSimpleText(self, phone:str, message:str, isGroup:bool=False, retry:bool=False):
        # Docs : https://eu.wablas.com/documentation/api#send-simple-text
        params = {
            'token'     : self.token,
            'phone'     : phone,
            'message'   : message,
            'isGroup'   : isGroup,
            'retry'     : retry,
        }
        url = self.urlformat('send-message', params)
        self.logprint('SendSimpleText', url)
        response = requests.get(url)
        return response.json()


    def SingleSendText(self, phone:str, message:str, isGroup:bool=False, retry:bool=False):
        # Docs : https://eu.wablas.com/documentation/api#single-send-text
        data = {
            'phone'     : phone,
            'message'   : message,
            'isGroup'   : isGroup,
            'retry'     : retry,
        }
        url = self.urlformat('send-message')
        self.logprint('SingleSendText', url)
        header = { 'Authorization' : self.token }
        response = requests.post(url, headers=header, data=data)
        return response.json()
    

    def SingleSendImage(self, phone:str, image_url:str, caption:str=None, isGroup:bool=False, retry:bool=False):
        # Docs : https://eu.wablas.com/documentation/api#single-send-image
        data = {
            'phone'     : phone,
            'image'     : image_url,
            'isGroup'   : isGroup,
            'retry'     : retry,
        }
        if caption:
            data['caption'] = caption

        url = self.urlformat('send-image')
        self.logprint('SingleSendImage', url)
        header = { 'Authorization' : self.token }
        response = requests.post(url, headers=header, data=data)
        return response.json()
    

    def SingleSendDocument(self, phone:str, document_url:str, caption:str=None, isGroup:bool=False, retry:bool=False):
        # Docs : https://eu.wablas.com/documentation/api#single-send-document
        data = {
            'phone'     : phone,
            'document'  : document_url,
            'isGroup'   : isGroup,
            'retry'     : retry,
        }
        if caption:
            data['caption'] = caption

        url = self.urlformat('send-document')
        self.logprint('SingleSendDocument', url)
        header = { 'Authorization' : self.token }
        response = requests.post(url, headers=header, data=data)
        return response.json()


    
apiwablas = API_WABLAS(settings.WABLAS_TOKEN)