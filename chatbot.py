import requests
import json
import sys

import config

conv_auth = requests.AuthObject(config.username, config.password)

def req(params={}):
    return requests.get('https://convore.com/api/live.json', params=params, auth=conv_auth)
    
cursor = None

def p(msg):
    print msg
    sys.stdout.flush()

while 1:
    p('requesting')
    r = req({'cursor': cursor}) if cursor else req()
    assert r.status_code == 200
    response = json.loads(r.content)
    for message in response['messages']:
        #toss login and logout messages for now
        #toss "x read group y" messages too
        if message['kind'] in ['login', 'logout', 'read']:
            continue

        p(message)

        cursor = message['_id']
