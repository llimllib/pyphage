"""/karma: who in the python room has the most karma?"""
import re

from chatbot import send, query

query("""
    CREATE TABLE IF NOT EXISTS karma (user_id INTEGER, user_name STRING, karma INTEGER);
""")

def on_unstar(message):
    unstarred = message["star"]["message"]["user"]
    unstarrer = message["star"]["user"]

    #starring yourself? lame.
    if unstarred['id'] == unstarrer['id']: return

    if query("SELECT * FROM karma WHERE user_id=?", unstarred['id']):
        query("UPDATE karma SET karma = karma - 10 WHERE user_id=?", unstarred['id'])
    else:
        query("""INSERT INTO karma (user_id, user_name, karma)
                 VALUES (?, ?, ?)""", unstarred['id'], unstarred['username'], 10)

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

def on_message(message):
    r = re.search(r"\/karma", message['message'])
    if not r: return

    msg = ""
    for user, karma in query("SELECT user_name, karma FROM karma ORDER BY karma DESC LIMIT 5"):
        msg += "%s: %s\n" % (user, karma)

    send(message['topic']['id'], msg)
