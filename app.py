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
    payload = json.dumps({"version": "3554d9e699e09693d3fa334a79c58be9a405dd021d3e11281256d53185868912",  "input": {"prompt" : pinput, "num_outputs" : 1}})
    headers = {'content-type': 'application/json', 'Authorization': f'Token {key}'}
    res = requests.post('https://api.replicate.com/v1/predictions', data=payload,  headers=headers)

    prediction = json.loads(res.text)['urls']['get']
    time.sleep(5)

    image = getImage(prediction)
    trys = 0
    while image['status'] != 'succeeded':
        if trys > 45:
            getImage(json.loads(res.text)['urls']['cancel'])
            return ['https://replicate.delivery/pbxt/qMJKDzX8SmIoMhYsokEY7rRrgyCdlYph8NTozXR6dJmTUBAE/out-0.png']
            break
        print(trys, file=sys.stderr)
        trys = trys + 1
        time.sleep(1)
        image = getImage(prediction)

    return image['output']

def getImage(url):
    headers = {'content-type': 'application/json', 'Authorization': f'Token {key}'}
    raw = requests.get(url, headers=headers)
    result = json.loads(raw.text)
    print(result['logs'], file=sys.stderr)
    return result