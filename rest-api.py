
import requests
from flask import Flask
from flask import request

from urllib.parse import urlencode
import json
import re
import urllib
import subprocess

url = "https://vision.googleapis.com/v1/images:annotate"
url2 = "http://127.0.0.1:8000/parse"




app = Flask(__name__)


@app.route('/',methods=["POST"])
def hello():
    json_body = request.json
    image = json_body["image_b64"]
    #print(image)
    
    token = subprocess.check_output("gcloud auth application-default print-access-token",shell=True).decode("utf-8")
    print(token)
    headers = {
    'Content-Type': "application/json; charset=utf-8",
    'Authorization': 'Bearer "{}"'.format(token[:-1]),
    'User-Agent': "PostmanRuntime/7.19.0",
    'Accept': "*/*",
    'Cache-Control': "no-cache",
    'Postman-Token': "863bdbdb-aaf3-4a9e-9f6e-cea7789d266e,49cd7aa1-a72c-4b94-9985-893f7a6d4bf5",
    'Host': "vision.googleapis.com",
    'Accept-Encoding': "gzip, deflate",
    'Content-Length': "71077",
    'Connection': "keep-alive",
    'cache-control': "no-cache"
    }

    
    
    payload = {
    "requests": [
        {
            "image": {
                "content": image
            },
            "features": [
                {
                    "type": "DOCUMENT_TEXT_DETECTION"
                }
            ]
        }
    ]
    }
    print(headers)         
    print(headers["Authorization"])
    response = requests.request("POST", url, json=payload, headers=headers)

    json_resp = json.loads(response.text)
    finaltext = json_resp["responses"][0]["fullTextAnnotation"]["text"].lower()
    print(finaltext)
    finaltext = finaltext.replace('\n',' ')
#    match=re.search('(\d{1,4}([.\-/])((jan|january|feb|february|mar|march|apr|april|may|jun|june|jul|july|aug|august|sep|september|oct|october|nov|november|dec|december)|(\d{1,2}))([.\-/])\d{1,4})',finaltext)
#    s = match.start()
#    e = match.end()
#    finaltext=finaltext[s:e]
    payload2 = {
            "text": "{}".format(finaltext),
            "locale": "en_GB"
            }
    payload3 = {
            "text": "{}".format(finaltext),
            "locale": "en_US"
            }
    print(payload2)
    headers2 = {
    'User-Agent': "PostmanRuntime/7.19.0",
    'Accept': "*/*",
    'Cache-Control': "no-cache",
    'Postman-Token': "2b11c69f-85c7-4f51-9679-917a4594d289,fb96a496-d057-442a-b241-eec120cc15e4",
    'Host': "52.191.214.35:8000",
    'Content-Type': "application/x-www-form-urlencoded",
    'Accept-Encoding': "gzip, deflate",
    'Content-Length': "513",
    'Connection': "keep-alive",
    'cache-control': "no-cache"
    }

    response2 = requests.request("POST", url2, data=urllib.parse.urlencode(payload2), headers=headers2)
    response3 = requests.request("POST", url2, data=urllib.parse.urlencode(payload3), headers=headers2)
    #print(response.text)
    json_resp2 = json.loads(response2.text)
    json_resp3 = json.loads(response3.text)
    
    matches=[]
    
    
    for item in json_resp2:
        if(item["dim"]=="time"):
            matches.append({"op_date": item["value"]["value"][:10],"match_len": int(item["end"])-int(item["start"])})
            break
    for item in json_resp3:
        if(item["dim"]=="time"):
            matches.append({"op_date": item["value"]["value"][:10],"match_len": int(item["end"])-int(item["start"])})
            break
        
    matches = sorted(matches, key = lambda i: i['match_len'])   
    
    
    print(matches)
    if(len(matches)==0):    
        return {"date": "None"} 
    else:
        return {"date": matches[1]["op_date"]} 
if __name__ == '__main__':
    app.run(host='0.0.0.0')