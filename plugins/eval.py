"""/eval <expression>: use a restricted python environment to return the result of <expression>

Examples:

/eval 1+2
3

/eval zip(*[[1,2],[3,4]])
[(1,3), (2,4)]"""
import re
#pip install sandbox
from sandbox import Sandbox

from chatbot import send

sandbox = Sandbox()

def on_message(message):
    r = re.search(r"\/eval (.+)", message['message'])
    if not r: return

    try:
        result = sandbox.call(lambda: eval(r.group(1)))
    #we're running code, any error could throw an exception
    except:
        send(message['topic']['id'], "Error running code")
    send(message['topic']['id'], str(result))
