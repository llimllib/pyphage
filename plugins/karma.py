"""/karma: who in the python group has the most karma?"""
import re

from chatbot import send, query

query("""
    CREATE TABLE IF NOT EXISTS karma (user_id INTEGER, user_name STRING, karma INTEGER);
""")

def on_star(message):
    starred = message["star"]["message"]["user"]
    starrer = message["star"]["user"]

    #starring yourself? lame.
    if starred['id'] == starrer['id']: return
     
    if query("SELECT * FROM karma WHERE user_id=?", starred['id']):
        query("UPDATE karma SET karma = karma + 10 WHERE user_id=?", starred['id'])
    else:
        query("""INSERT INTO karma (user_id, user_name, karma)
                 VALUES (?, ?, ?)""", starred['id'], starred['username'], 10)

def on_unstar(message):
    unstarred = message["star"]["message"]["user"]
    unstarrer = message["star"]["user"]

    if unstarred['id'] == unstarrer['id']: return

    if query("SELECT * FROM karma WHERE user_id=?", unstarred['id']):
        query("UPDATE karma SET karma = karma - 10 WHERE user_id=?", unstarred['id'])
    else:
        query("""INSERT INTO karma (user_id, user_name, karma)
                 VALUES (?, ?, ?)""", unstarred['id'], unstarred['username'], 10)

def on_message(message):
    r = re.search(r"\/karma ?([\w\-_]+)?", message['message'])
    if not r: return

    if not r.group(1):
        msg = "The 5 users with the highest karma are:\n"
        for user, karma in query("SELECT user_name, karma FROM karma ORDER BY karma DESC LIMIT 5"):
            msg += "%s: %s\n" % (user, karma)
    else:
        karma = query("SELECT karma FROM karma WHERE user_name=?", r.group(1))
        if not karma:
            msg = "Unable to find user %s" % r.group(1)
        else:
            msg = "%s: %s" % (r.group(1), karma[0][0])

    send(message['topic']['id'], msg)
