import json
import sys
import importlib
import traceback
import re
import sqlite3
from time import sleep
from glob import glob

#pip install requests
import requests

import config
    
def p(msg):
    print msg
    sys.stdout.flush()

db = sqlite3.connect("pyphage.db")
def query(sql, *params):
    c = db.cursor()
    c.execute(sql, params)
    rows = c.fetchall()
    c.close()
    db.commit()
    return rows

hooks = {}
def init_plugins():
    for plugin in glob('plugins/[!_]*.py'):
        try:
            mod = importlib.import_module(plugin.replace("/", ".")[:-3])
            modname = mod.__name__.split('.')[1]

            for hook in re.findall("on_(\w+)", " ".join(dir(mod))):
                hookfun = getattr(mod, "on_" + hook)
                p("attaching %s.%s to %s" % (modname, hookfun, hook))
                hooks.setdefault(hook, []).append(hookfun)

            if mod.__doc__:
                firstline = mod.__doc__.split('\n')[0]
                hooks.setdefault('help', []).append(firstline)
                hooks.setdefault('extendedhelp', {})[modname] = mod.__doc__

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
    r = requests.post("https://convore.com/api/topics/%s/messages/create.json" % topic_id,
                      data={"message": message.encode('utf-8')}, auth=conv_auth)

    assert r.status_code == 200
    p("successful send")

def help(message):
    """Look for a help request and handle it if it's found"""
    if 'help' not in hooks: return

    r = re.search(r"\/help ?([\w.\-_]+)?", message['message'])
    if not r: return

    if not r.group(1):
        msg = "The python chatbot currently implements these commands:\n" + "\n".join(hooks['help'])
    else:
        if r.group(1) in hooks['extendedhelp']:
            msg = hooks['extendedhelp'][r.group(1)]
        else:
            msg = "Sorry, could not find help on %s" % r.group(1)
    send(message['topic']['id'], msg)

def main():
    init_plugins()

    conv_auth = requests.AuthObject(config.username, config.password)

    def req(params={}):
        return requests.get('https://convore.com/api/live.json', params=params, auth=conv_auth)

    cursor = None
    while 1:
        try:
            p('requesting')
            r = req({'cursor': cursor}) if cursor else req()

            if not r.status_code == 200:
                p("Got invalid status code %s on response body %s. Sleeping for 60." % (r.status_code, r.content))
                sleep(60)
                continue

            response = json.loads(r.content)
            for message in response['messages']:
                cursor = message['_id']

                #ignore messages sent by ourselves to (try and) avoid infinite loops
                if message['user']['username'] == config.username:
                    continue

                if message['kind'] == 'message':
                    help(message)

                #if we have any hooks for this kind of message, run the function
                if message['kind'] in hooks:
                    for hook in hooks[message['kind']]:
                        p("calling %s" % hook)
                        hook(message)

                #don't print login, logout, or read messages. Eventually TODO: DELETEME
                if message['kind'] not in ['login', 'logout', 'read']:
                    p(message)
        except KeyboardInterrupt:
            sys.exit(0)


if __name__=="__main__":
    main()
