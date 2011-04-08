import re
from chatbot import send, p

def on_message(message):
    r = re.search(r"\/help (\w+)", message[u'message'])
    if not r: return

    h = r.group(1)
    p("helping: " + h)
    #importlib changes __builtins__ into a dictionary??!?
    if h in __builtins__:
        p("sending: " + __builtins__[h].__doc__)
        send(message['topic']['id'], __builtins__[h].__doc__)
    else:
        p("__builtins__ doesn't have " + h)
        p("__builtins__: %s" % __builtins__)
