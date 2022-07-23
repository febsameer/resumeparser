import requests
import os
import json
index = "resume"
host = "http://localhost:4080"

def createResumeDoc(payload):
    cred = os.environ.get('zincCred','')
    
    headers = {
      'Authorization': 'Basic ' + cred,
      'Content-Type': 'application/json'
    }
    
    zinc_url = host + "/api/" + index + "/_doc"
    response = requests.request("POST", zinc_url, headers=headers, data=payload)

    return response
    

def searchResume(cid, query):
    params = {
        "query":
        {
            "bool":
            {
                "must":
                [
                    {
                        "query_string":
                        {
                            "query": "+CID:" + str(cid) + " " + buildQuery(query)
                        }
                    }
                ]
            }
        },
        "sort":
        [
            "-@timestamp"
        ]
    }
    
    cred = os.environ.get('zincCred','')
    
    headers = {
      'Authorization': 'Basic ' + cred,
      'Content-Type': 'application/json'
    }
    
    
    zinc_url = host + "/api/" + index + "/_search"

    return requestsrequest("POST", zinc_url, headers=headers, data=json.dumps(params))

def buildTerm(term):
    term = term.upper()
    if term == 'AND':
        return '+'
    elif term == 'OR':
        return ' '
    elif term == 'NOT':
        return '-'
    else:
        return ''

def buildQuery(query):
    zQuery = '+'
    
    for term in query.split():
        bTerm = buildTerm(term)
        if bTerm == '':
            zQuery += term + ' '
        else:
            zQuery += bTerm
    
    return zQuery