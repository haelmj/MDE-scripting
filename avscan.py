import json
import csv
import requests
from assets.popups import *
from assets.fileexplorer import *
import json

# create prompt to receive this info. Store tenantId and appId on inital config then later on appSecret and csv will always be requested
# if info exists then move on to popup for appsecret then csv file
# else show popup to add this info

class AVScan():
    def __init__(self):
        try:
            with open('app.json', 'r') as f:
                data = json.load(f)
            if data['tenantID'] and data['appID']:
                self.tenantId = data['tenantID']
                self.appId = data['appID']
            else:
                self.tenantId = popup('TenantId', "Enter TenantId")
                self.appId = popup('App ID', 'Enter Application ID')
        except FileNotFoundError:
            data ={}
            self.tenantId = popup('TenantId', "Enter TenantId")
            self.appId = popup('App ID', 'Enter Application ID')
            data['tenantID'] = self.tenantId
            data['appID'] = self.appId
            with open('app.json', 'w') as f:
                json.dump(data, f)
        self.appSecret = popup('App Secret', 'Enter Application Secret')

    def get_access_token(self):
        url = f"https://login.microsoftonline.com/{self.tenantId}/oauth2/token"

        resourceAppIdUri = "https://api.securitycenter.microsoft.com"
        headers = {"Content-Type":"application/x-www-form-urlencoded"}
        body = {"resource": resourceAppIdUri,"client_id": self.appId,"client_secret": self.appSecret,"grant_type": "client_credentials"}
        response = requests.post(url, body, headers)
        jsonResponse = response.json()
        aadToken = jsonResponse["access_token"]
        return aadToken
    def trigger_scan(self):
        aadToken = self.get_access_token()            
        url = "https://api.securitycenter.microsoft.com/api/machines"
        headers = { 
            'Content-Type' : 'application/json',
            'Accept' : 'application/json',
            'Authorization' : "Bearer " + aadToken
        }

        file = fileExplorer()
        body = {"Comment": "Check machine for viruses","ScanType": "Full"}

        with open(file) as f:
            csvreader = csv.reader(f)
            for row in csvreader:
                id = row[0]
                new_url = url + f"/{id}/runAntiVirusScan"
                response = requests.post(new_url, json=body, headers=headers)
                jsonResponse = response.json()
                print(jsonResponse)
            show_info('Trigger Scans', 'Scans Triggered Successfully!')

AVScan().trigger_scan()