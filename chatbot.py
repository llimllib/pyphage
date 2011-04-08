import json
import sys
import importlib
import traceback
import re
from glob import glob

#pip install requests
import requests

import config
    
def p(msg):
    print msg
    sys.stdout.flush()

hooks = {}
def init_plugins():
    for plugin in glob('plugins/[!_]*.py'):
        try:
            mod = importlib.import_module(plugin.replace("/", ".")[:-3])
            for hook in re.findall("on_(\w*)", " ".join(dir(mod))):
                p("attaching %s to %s" % (getattr(mod, "on_" + hook), hook))
                hooks.setdefault(hook, []).append(getattr(mod, "on_" + hook))
        #bare except, because the modules could raise any number of errors
        #on import, and we want them not to kill our server
        except:
            p("import failed on module %s, module not loaded" % plugin)
            p("%s" % sys.exc_info()[0])
            p("%s" % traceback.format_exc())

def send(topic_id, message):
    p("trying to send: %s to %s" % (message, topic_id))
    #does this make a request?
    conv_auth = requests.AuthObject(config.username, config.password)
    requests.post("https://convore.com/api/topics/%s/messages/create.json" % topic_id,
                  data=message, auth=conv_auth)

def main():
    init_plugins()

    conv_auth = requests.AuthObject(config.username, config.password)

    def req(params={}):
        return requests.get('https://convore.com/api/live.json', params=params, auth=conv_auth)

    cursor = None
    while 1:
        p('requesting')
        r = req({'cursor': cursor}) if cursor else req()
        assert r.status_code == 200
        response = json.loads(r.content)
        for message in response['messages']:

            #if we have any hooks for this kind of message, run the function
            if message['kind'] in hooks:
                for hook in hooks[message['kind']]:
                    p("calling %s" % hook)
                    hook(message)

            #toss login and logout messages for now
            #toss "x read group y" messages too
            if message['kind'] in ['login', 'logout', 'read']:
                continue

            p(message)

            cursor = message['_id']

if __name__=="__main__":
    main()
