import sqlite3


con = sqlite3.connect("db.sqlite",check_same_thread=False)
cur = con.cursor()

cur.execute("""create table currencies (
            name string,
            id integer autoincrement,
            
)""")