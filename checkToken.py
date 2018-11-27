import requests
import json

def checkTokenValidity():
    # read a list of lines into data
    with open('api_credentials.txt', 'r') as file:
            credentials = file.readlines()

    #Get credentials for api login from the text file(remove new line otherwise it creates problems when used)
    username = credentials[0].replace('\n', '')
    pswd = credentials[1].replace('\n', '')
    bearer = credentials[2].replace('\n', '')
    headers = {"Authorization":"Bearer " + bearer}
    api_endpoint = "http://tourism.opendatahub.bz.it/api/RegionReduced"
    login_endpoint = "http://tourism.opendatahub.bz.it/api/LoginApi"

    tokenCheck = requests.get(api_endpoint, headers=headers)

    if (tokenCheck.status_code == 200):
        # Check call successful: Use the bearer we have for the chatbot requests
        print("SUCCESS")
    elif (tokenCheck.status_code == 401):
        # Check call unsuccessful, unauthorised: Get a new bearer token
        payload = {"username":username, "pswd":pswd}
        login_call = requests.post(login_endpoint, data=payload)
        login_call_json = login_call.json()
  
        # Get new bearer from response data and save it to write it to the file later.
        new_bearer = login_call_json['access_token']
        credentials[2] = new_bearer

        with open('api_credentials.txt', 'w') as file:
            file.writelines(credentials) #write to the credentials.txt the new bearer

        file.close() # close the file stream    
    else:
        # Other errors (unexpected)    
        print("Error: " + tokenCheck.status_code)