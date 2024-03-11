import sqlite3
conn = sqlite3.connect('test.db')
print("open database successfully!")
c = conn.cursor()
c.execute('''CREATE TABLE test
       (
       term           TEXT    NOT NULL,
       explain        TEXT    NOT NULL);''')
print("create table successfully")
conn.commit()
conn.close()