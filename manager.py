import sqlite3
from os import urandom
import hashlib
#plik z logiką działania
class Manager:
    def __init__(self, file="./passwords.db"):
        self.file = file
        self.conn = sqlite3.connect(self.file)
        self.c = self.conn.cursor()

    def createDatabase(self):
        self.c.execute("""
            CREATE TABLE passwords(
                name TEXT PRIMARY KEY UNIQUE,
                password TEXT,
                username TEXT,
                description TEXT
            )
        """)

        self.c.execute("""
            CREATE TABLE integrity(
                name TEXT,
                hash TEXT,
                FOREIGN KEY(name) REFERENCES passwords(name)
            ) 
        """)

        self.conn.commit()

    def addPassword(self, name, password, username = None, description = None):
        self.c.execute("SELECT password FROM passwords WHERE name=?", (name,))
        if len(self.c.fetchall()) != 0:
            print("This password already exist")
            return False
        self.c.execute("INSERT INTO passwords VALUES(?,?,?,?)",(name, password, username, description))
        hash = hashlib.sha256()
        passbytes = password.encode("utf-8")
        hash.update(passbytes)
        self.c.execute("INSERT INTO integrity VALUES(?,?)", (name, hash.hexdigest()))
        self.conn.commit()
        return True


    def deletePassword(self):
        pass
    
    def getPassword(self, name):
        pass

    def setPassword(self):
        pass

    def closeDatabase(self):
        self.conn.close()

    def generate(self, passlen=16, lc=True, uc=True, s=True, n=True):
        password = []
        i=0
        while i<passlen:
            typeofchar = int.from_bytes(urandom(1), "big")
            if typeofchar%4 == 0 and lc==True:
                character = int.from_bytes(urandom(1), "big")
                character = chr(character%26+97)
                password.append(character)
                i+=1
            elif typeofchar%4 == 1 and uc==True:
                character = int.from_bytes(urandom(1), "big")
                character = chr(character%26+65)
                password.append(character)
                i+=1
            elif typeofchar%4 == 2 and s==True:
                character = int.from_bytes(urandom(1), "big")
                character = character%32
                if character>=0 and character<=14:
                    character = chr(character+33)
                elif character>=15 and character<=21:
                    character = chr(character+58-15)
                elif character>=22 and character<= 27:
                    character = chr(character+91-22)
                elif character>=28 and character<=31:
                    character = chr(character+123-28)
                password.append(character)
                i+=1 
            elif typeofchar%4 == 3 and n==True:
                character = int.from_bytes(urandom(1), "big")
                password.append(str(character%10))
                i+=1
        return "".join(password)



if __name__ == "__main__":
    m = Manager()
    #m.createDatabase()
    m.addPassword(name="first", password=m.generate())
    m.c.execute("SELECT * FROM passwords, integrity")
    print(m.c.fetchall())
    
