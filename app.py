from flask import *
import requests
import sys
import time
import os
app = Flask(__name__)
key = os.environ['POKEMON_API_KEY']

@app.route("/")
def hello_world():
   return render_template('index.html')

@app.route("/get_image", methods=['POST', 'GET'])
def get_image():
    pinput = json.loads(request.data)['input']
    pr = pastResults(pinput)

    if pr:
        return pr

    payload = json.dumps({"version": "3554d9e699e09693d3fa334a79c58be9a405dd021d3e11281256d53185868912",  "input": {"prompt" : pinput, "num_outputs" : 1}})
    headers = {'content-type': 'application/json', 'Authorization': f'Token {key}'}
    res = requests.post('https://api.replicate.com/v1/predictions', data=payload,  headers=headers)

    if res.status_code > 201:
        print(res.reason, file=sys.stderr)
        return ['https://replicate.delivery/pbxt/qMJKDzX8SmIoMhYsokEY7rRrgyCdlYph8NTozXR6dJmTUBAE/out-0.png']

    prediction = json.loads(res.text)
    time.sleep(5)

    image = getImage(prediction['urls']['get'])
    trys = 0
    while image['status'] != 'succeeded':
        if trys > 45:
            getImage(json.loads(res.text)['urls']['cancel'])
            return ['https://replicate.delivery/pbxt/qMJKDzX8SmIoMhYsokEY7rRrgyCdlYph8NTozXR6dJmTUBAE/out-0.png']
            break
        print(trys, file=sys.stderr)
        trys = trys + 1
        time.sleep(1)
        image = getImage(prediction['urls']['get'])

    return image['output']

def getImage(url):
    headers = {'content-type': 'application/json', 'Authorization': f'Token {key}'}
    raw = requests.get(url, headers=headers)
    result = json.loads(raw.text)
    print(result['logs'], file=sys.stderr)
    return result

def pastResults(prompt):
    headers = {'content-type': 'application/json', 'Authorization': f'Token {key}'}
    raw = requests.get('https://api.replicate.com/v1/predictions?cursor=cD0yMDIyLTExLTE0KzE4JTNBMTAlM0E1My4zNzA4MjAlMkIwMCUzQTAw', headers=headers)
    result = json.loads(raw.text)
    print(result, file=sys.stderr)
    for r in result['results']:
        if r['input']['prompt'] == prompt:
            return r['output'][0]
    return False