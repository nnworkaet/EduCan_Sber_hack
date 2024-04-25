import sqlite3
import time
class Database:
    def __init__(self, db_name="gpt/db/db.db"):
        self.conn = sqlite3.connect(db_name)
        self.cur = self.conn.cursor()

    def create(self, key, state):
        self.cur.execute("""
            INSERT INTO keys (key, state, timestamp) VALUES (?, ?,?)
        """, (key, state,time.time()))
        self.conn.commit()
    def read_active_after_429(self):
        self.cur.execute("SELECT key, timestamp FROM keys WHERE state = ?", ("429",))
        results = self.cur.fetchall()
        array = []

        for item in results:
            key = item[0]
            timestamp = item[1]

            if time.time() - timestamp > 30:
                array.append(key)
        for i in array:
            self.change_state(i,"1")
        return array
    def read_active(self):
        self.cur.execute("SELECT key, timestamp FROM keys WHERE state = ?", ("1",))
        results = self.cur.fetchall()
        array = []

        for item in results:

            key = item[0]
            timestamp = item[1]

            if time.time() - timestamp > 10:
                array.append(key)


        list_1=array
        list_429=self.read_active_after_429()
        list_active=list_1+list_429
        if list_active==[]:
            return "No keys"
        else:
            return list_active

    def change_state(self, key, new_state):
        self.cur.execute("""
            UPDATE keys SET state = ? WHERE key = ?
        """, (new_state, key))
        self.conn.commit()
    def change_time(self, key):
        self.cur.execute("""
            UPDATE keys SET timestamp = ? WHERE key = ?
        """, (time.time(),key))
        self.conn.commit()

    def set_state_all_to(self, new_state):
        self.cur.execute("""
            UPDATE keys SET state = ?
        """, (new_state,))
        self.conn.commit()

    def turn_off_30(self,key):
        #без асинк не ворк
        self.change_state(key,"429")

    #Функции для proxy
    def create_proxy(self, type_proxy, state,link,auth):
        self.cur.execute("""
            INSERT INTO proxy (type, state, link, auth) VALUES (?, ?,?,?)
        """, (type_proxy, state,link,auth))
        self.conn.commit()
    def read_active_proxy(self):
        self.cur.execute("SELECT link, auth,type FROM proxy WHERE state = ?", ("1",))
        results = self.cur.fetchall()
        array = []

        for item in results:

            link = item[0]
            auth = item[1]
            type = item[2]

            array.append((link,auth,type))

        list_active=array
        if list_active==[]:
            return "No proxies"
        else:
            return list_active

    def change_state_proxy(self, link, new_state):
        self.cur.execute("""
               UPDATE proxy SET state = ? WHERE key = ?
           """, (new_state, link))
        self.conn.commit()

    #logs

    def create_log(self, type, msg):
        self.cur.execute("""
            INSERT INTO logs (type, msg, timestamp) VALUES (?, ?,?)
        """, (type, msg,time.time()))
        self.conn.commit()
