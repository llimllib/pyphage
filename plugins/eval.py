"""/eval <expression>: use a restricted python environment to return the result of <expression>

Examples:

/eval 1+2
3

/eval zip(*[[1,2],[3,4]])
[(1,3), (2,4)]"""
import re
import traceback
import sys
#pip install pysandbox
from sandbox import Sandbox, SandboxConfig

from chatbot import send, p

config = SandboxConfig("encodings", "math")
config.timeout = 5
sandbox = Sandbox(config)

def on_message(message):
    r = re.search(r"\/eval (.+)", message['message'])
    if not r: return

    try:
        ns = {'__result': None}
        sandbox.execute("import math; __result = " + r.group(1), locals=ns)
        res = unicode(ns['__result'])
        if len(res) > 500:
            res = res[:500] + " ..."
        send(message['topic']['id'], res)
    #we're running code, any error could throw an exception
    except:
        send(message['topic']['id'], "Error running code")
        p("%s" % sys.exc_info()[0])
        p("%s" % traceback.format_exc())
