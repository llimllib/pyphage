"""/doc <something>: return python 2.7's documentation for <something>"""
import re
import importlib
import pydoc

from chatbot import send, p

#by default, render_doc uses shell escapes. Stop that.
class PlainTextDoc(pydoc.TextDoc):
    def bold(self, x): return x
pydoc.text = PlainTextDoc()

def on_message(message):
    r = re.search(r"\/doc ([\w.]+)", message[u'message'])
    if not r: return

    thing = r.group(1)
    try:
        docs = pydoc.render_doc(bytes(thing))
        #truncate to 20 lines and note that it's been truncated
        docs = "\n".join(docs.split("\n")[:20]) + "\n<truncated>"
        send(message['topic']['id'], docs)
    except ImportError:
        send(message['topic']['id'], "unable to find help on %s" % thing)
    except pydoc.ErrorDuringImport as e:
        send(message['topic']['id'], "error importing %s: %s" % (thing, e.value.message))
