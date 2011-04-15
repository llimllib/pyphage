"""/pep <number>: return a link and the introduction to pep <number>"""
import re
import xml.sax.saxutils

import requests

from chatbot import send

def unescape(s):
    """do some additional unescaping to unmash python.org HTML"""
    s = xml.sax.saxutils.unescape(s)
    s = s.replace("&#32;", " ")
    s = s.replace("&#97;", "a")
    return s

def on_message(message):
    r = re.search(r"\/pep (\d+)", message['message'])
    if not r: return

    pep = r.group(1)

    link = "http://www.python.org/dev/peps/pep-%s/" % pep.rjust(4, '0')

    r = requests.get(link)
    if r.status_code == 404:
        send(message['topic']['id'], "unable to find pep %s" % pep)
    else:
        fields = re.findall('class="field-name">(.*?):.*?</th><td.*?>(.*?)<', r.content)
        msg = "\n".join("%s: %s" % tuple(map(unescape, (k,v))) for k,v in fields)
        msg += "\n" + link
        send(message['topic']['id'], msg)
