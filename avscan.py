import json
import urllib.request
import urllib.parse

tenantId = '00000000-0000-0000-0000-000000000000' # Paste your own tenant ID here
appId = '11111111-1111-1111-1111-111111111111' # Paste your own app ID here
appSecret = '22222222-2222-2222-2222-222222222222' # Paste your own app secret here

# get access token

url = "https://login.microsoftonline.com/%s/oauth2/token" % (tenantId)

resourceAppIdUri = 'https://api.securitycenter.microsoft.com'

body = {
    'resource' : resourceAppIdUri,
    'client_id' : appId,
    'client_secret' : appSecret,
    'grant_type' : 'client_credentials'
}

data = urllib.parse.urlencode(body).encode("utf-8")

req = urllib.request.Request(url, data)
response = urllib.request.urlopen(req)
jsonResponse = json.loads(response.read())
aadToken = jsonResponse["access_token"]

# get machine ids

url = "https://api.securitycenter.microsoft.com/api/machines"
headers = { 
    'Content-Type' : 'application/json',
    'Accept' : 'application/json',
    'Authorization' : "Bearer " + aadToken
}



req = urllib.request.Request(url, headers)
response = urllib.request.urlopen(req)
jsonResponse = json.loads(response.read())
machines = jsonResponse["value"]

# trigger av scans
body = {
  "Comment": "Check machine for viruses",
  "ScanType": "Full"
}

for m in machines:
    new_url = url + f"/{m.id}/runAntiVirusScan"
    data = urllib.parse.urlencode(body).encode("utf-8")
    req = urllib.request.Request(url, data, headers)
    jsonResponse = json.loads(response.read())
    print(jsonResponse)