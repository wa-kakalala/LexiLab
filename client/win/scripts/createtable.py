import sqlite3
conn = sqlite3.connect('userinfo.db')
print("open database successfully!")
c = conn.cursor()
c.execute('''CREATE TABLE userinfo
(
        username           TEXT    NOT NULL,
        password           TEXT    NOT NULL,
        email              TEXT    NOT NULL,
        date               TEXT    NOT NULL,
        last               TEXT    
);''')
print("create table successfully")
conn.commit()
conn.close()