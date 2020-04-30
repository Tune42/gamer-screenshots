import sqlite3

conn = sqlite3.connect('gamerscreenshots.db')
c = conn.cursor()
author = ("Tune42",)

c.execute('SELECT * FROM posts WHERE Author=?', author)

print(c.fetchall())

conn.close()