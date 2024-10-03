import sqlite3



def init():
    conn = sqlite3.connect('app.db')
    conn.execute("""CREATE TABLE users (
        username TEXT NOT NULL,
        password TEXT NOT NULL,
        avatar TEXT NOT NULL,
        bio TEXT NOT NULL,
        PRIMARY KEY (username)
    );""")
    conn.commit()
    conn.close()


def verify_user(username, password):
    with sqlite3.connect("app.db") as conn:
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM users WHERE username=? AND password=?", (username, password))
        res = cur.fetchone()
    
    return True if res else False
        
def get_user(username):
    with sqlite3.connect("app.db") as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username=?", (username,))
        res = cur.fetchone()
    
    return res

def create_user(username, password, avatar, bio):
    with sqlite3.connect("app.db") as conn:
        cur = conn.cursor()
        conn.execute("INSERT INTO users VALUES (?,?,?,?)", (username, password, avatar, bio))


def update_user(username, avatar, bio):
     with sqlite3.connect("app.db") as conn:
        cur = conn.cursor()
        conn.execute("UPDATE users SET avatar=?, bio=? where username=?", (avatar,bio, username))




    