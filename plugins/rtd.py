"""/rtd <module> <function>: return a link to readthedocs for <module> and <function>"""
import re
from urllib import quote

from chatbot import send

def on_message(message):
    r = re.search(r"\/rtd ([\w._-]+) ?([\w._-]+)?", message[u'message'])
    if not r: return

    project = r.group(1)
    term = r.group(2) or ""

    link = "http://%s.rtfd.org/%s" % (quote(project), quote(term))

    send(message['topic']['id'], link)
