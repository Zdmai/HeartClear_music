import sqlite3

conn = sqlite3.connect('web.sql')

with open('db.sql') as f:
    conn.executescript(f.read())