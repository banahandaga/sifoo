# =========================================
# Created by Ridwan Renaldi, S.Kom. (rr867)
# =========================================
from django.conf import settings

import requests
import json
import os


# ===================[Response SUCCESS]===================
# {
#     "success": "true",
#     "token": "8934ebeaf48b694b41ca66ad26031f5e"
# }
# =====[OR]=====
# {
#     "success": "true",
#     "kode": "20222",
#     "tahun": "2022/2023",
#     "semester": "Genap"
# }
# =====[OR]=====
# {
#     "success": "true",
#     "records": 21,
#     "rows": [
#         {
#             "fid": "J218",
#             "prodi": "Magister Keperawatan"
#         },
#         
#         .
#         .
#         .
#         .
#         
#         {
#             "fid": "W100",
#             "prodi": "Magister Akuntansi"
#         }
#     ]
# }

# ====================[Response ERROR]====================
# {
#     "success": "false",
#     "error_code": "11",
#     "error_desc": "username/password salah",
#     "data": ""
# }
# =====[OR]=====
# {
#     "success": "false",
#     "error_code": "17",
#     "error_desc": "Data KRS tidak ada",
#     "data": ""
# }

class API_STAR:
    url      = settings.API_STAR_URL
    username = ''
    password = ''
    token    = ''
    filename = ''

    def __init__(self, username, password, filename=None):
        self.username = username
        self.password = password
        self.filename = 'token/{0}.json'.format(filename) if filename else 'token/{0}.json'.format(username)
        os.makedirs(os.path.dirname(self.filename), exist_ok=True)


    def getNewToken(self):
        body = { 'username' : self.username, 'password' : self.password, 'act' : 'GetToken' }
        response = requests.post(self.url, data=body)
        response = response.json()

        if response['success'] and response['success'].lower() == 'true' :

            with open(self.filename,'w') as file:
                json.dump(response, file, indent=4)

            self.token = response['token']
            return response
        else:
            return response



    def getToken(self):
        try:
            with open(self.filename) as file:
                data = json.load(file)

            if not data:
                getNewToken = self.getNewToken()
                if getNewToken['success'] and getNewToken['success'].lower() == 'true' :
                    self.token = getNewToken['token']
                    return getNewToken
                else:
                    return getNewToken

            else:
                self.token = data['token']
                return data

        except:
            getNewToken = self.getNewToken()
            if getNewToken['success'] and getNewToken['success'].lower() == 'true' :
                self.token = getNewToken['token']
                return getNewToken
            else:
                return getNewToken

    

    def getMhsProfile(self, nim:str):
        gettoken = self.getToken()

        if gettoken['success'] and gettoken['success'].lower() == 'true' :
            body = { 'act' : 'Mhs', 'token' : self.token, 'nim' : nim }
            response = requests.post(self.url, data=body)
            response = response.json()

            print('[Request getMhsProfile] : ', response)

            if response['success'].lower() == 'false' and response['error_code'] == '13':
                self.getNewToken()
                self.getMhsProfile(nim)

            return response
        else:
            return gettoken
        
    
    def getMhsProfileWithoutAuth(self, nim:str):
        response = requests.get(url = 'https://star.ums.ac.id/sia/api/mhs-detail/'+nim , verify=False)
        response = response.json()

        print('[Request getMhsProfileWithoutAuth] : ', response)

        if response and response['success']:
            response = response['data'][0]
            response['success'] = True
        else:
            response = response

        return response
    

apistar = API_STAR(settings.API_STAR_USERNAME, settings.API_STAR_PASSWORD, 'star')