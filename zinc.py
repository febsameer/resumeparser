import requests
import os
import json
index = "resume"
host = "http://localhost:4080"

def createResumeDoc(docId, payload):
    cred = os.environ.get('zincCred','')
    
    headers = {
      'Authorization': 'Basic ' + cred,
      'Content-Type': 'application/json'
    }
    
    zinc_url = host + "/api/" + index + "/_doc/" + str(docId)
    # print(zinc_url)
    response = requests.request("PUT", zinc_url, headers=headers, data=payload)

    return response
    

def searchResume(cid, query):
    query = "+CID:" + str(cid) + " " + buildQuery(query)
    
    params = {
    "search_type": "querystring",
    "query": {
        "term": query
    },
    "sort_fields": ["_score"],
    "from": 0,
    "max_results": 20,
    "_source": ["consultantID"]
}
    
    cred = os.environ.get('zincCred','')
    
    headers = {
      'Authorization': 'Basic ' + cred,
      'Content-Type': 'application/json'
    }
    
    
    zinc_url = host + "/api/" + index + "/_search"

    res = requests.request("POST", zinc_url, headers=headers, data=json.dumps(params))
    return res

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