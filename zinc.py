import requests
import json
import os

url = "http://localhost:4080/api/resume/_doc"

def createResumeDoc(contents):
    
    payload = json.dumps({
      "contents": contents
    })
    
    cred = os.environ.get('zincCred','')
    
    headers = {
      'Authorization': 'Basic ' + cred,
      'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response