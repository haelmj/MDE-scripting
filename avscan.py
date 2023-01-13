import json
import urllib.request
import urllib.parse
import csv
import requests
from assets.popups import *

tenantId = '' # Paste your own tenant ID here
appId = '' # Paste your own app ID here
appSecret = '' # Paste your own app secret here



# create prompt to receive this info. Store tenantId and appId on inital config then later on appSecret and csv will always be requested
# if info exists then move on to popup for appsecret then csv file
# else show popup to add this info

# get access token

class AVScan():
    def __init__(self):
        self.tenantId = popup('TenantId', "Enter TenantId")
        self.appId = appId
        self.appSecret = appSecret

    def get_access_token(self):
        url = f"https://login.microsoftonline.com/{self.tenantId}/oauth2/token"

        resourceAppIdUri = "https://api.securitycenter.microsoft.com"

        body = {"resource": resourceAppIdUri,"client_id": appId,"client_secret": appSecret,"grant_type": "client_credentials"}

        data = urllib.parse.urlencode(body).encode('utf-8')
        req = urllib.request.Request(url, data)
        with urllib.request.urlopen(req) as response:
            jsonResponse = json.loads(response.read())
            aadToken = jsonResponse["access_token"]
        return aadToken
    def trigger_scan(self):
        pass



# # get machine ids

# url = "https://api.securitycenter.microsoft.com/api/machines"
# headers = { 
#     'Content-Type' : 'application/json',
#     'Accept' : 'application/json',
#     'Authorization' : "Bearer " + aadToken
# }


# req = urllib.request.Request(url, headers=headers)
# response = urllib.request.urlopen(req)
# jsonResponse = json.loads(response.read())
# machines = jsonResponse["value"]


# # # trigger av scans
# body = {"Comment": "Check machine for viruses","ScanType": "Full"}


# with open('DeviceID.csv') as f:
#     csvreader = csv.reader(f)
#     for row in csvreader:
#         id = row[0]
#         new_url = url + f"/{id}/runAntiVirusScan"
#         response = requests.post(new_url, json=body, headers=headers)
#         jsonResponse = response.json()
#         print(jsonResponse)


