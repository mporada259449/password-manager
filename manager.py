import sqlite3
from os import urandom, path
import hashlib
from pyperclip import copy as copy_clipboard
from time import sleep
#plik z logiką działania
class Manager:
    def __init__(self, file="./passwords.db"):
        self.file = file
        self.conn = sqlite3.connect(self.file)
        self.c = self.conn.cursor()
        self.c.execute("PRAGMA foreign_keys = 1")

    def createDatabase(self):
        #if path.isfile(self.file):
        #    return 0

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
                FOREIGN KEY(name) REFERENCES passwords(name) ON DELETE CASCADE 
            ) 
        """)

        self.conn.commit()

    def addPassword(self, name, password, username = None, description = None):
        self.c.execute("SELECT password FROM passwords WHERE name=?", (name,))
        if len(self.c.fetchall()) != 0:
            print("This password already exist")
            return False
        else:
            self.c.execute("INSERT INTO passwords VALUES(?,?,?,?)",(name, password, username, description))
            self.c.execute("INSERT INTO integrity VALUES(?,?)", (name, self.getHash(password)))
            self.conn.commit()
            return True


    def deletePassword(self, name):
        self.c.execute("DELETE FROM passwords WHERE name=?", (name,))
        if self.c.rowcount == 0:
            print("This entry didn't exist in the datebase")
        else:
            self.conn.commit()      
    
    def getPassword(self, name, verbose = False):
        self.c.execute("SELECT password FROM passwords WHERE name=?", (name,))
        passcopy = self.c.fetchone()
        if passcopy is None:
            print("Password with given name doesn't exist")
        else:
            print("Password is copied into the clipboard")
            copy_clipboard(passcopy[0])
            if verbose == True:
                print(f"password: {passcopy[0]}")
            sleep(10)
            copy_clipboard("")
        
        self.conn.commit()

    def setData(self, name, data):
        #data = {password: str, username: str, description: str}
        change = {k:v for k,v in data.items() if v != None}
        self.c.execute("SELECT password FROM passwords WHERE name = ? ", (name,))
        if len(self.c.fetchall()) == 0:
            print("Entry with this name doesn't exist")
        else:
            query = f"UPDATE passwords SET "
            for key in change.keys():
                query += f"{key} = \"{change[key]}\", "
            query = query[:-2] + f" WHERE name=\"{name}\""
            print(query)
            self.c.execute(query)


            if "password" in data.keys():
                query_integrity = f"""UPDATE integrity
                                    SET hash = \"{self.getHash(data["password"])}\"
                                    WHERE name = \"{name}\""""
                self.c.execute(query_integrity)

            self.conn.commit()
            
       

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

    def getHash(self, data):
        hash = hashlib.sha256()
        databytes = data.encode("utf-8")
        hash.update(databytes)
        return hash.hexdigest()



if __name__ == "__main__":
    m = Manager("nowabaza.db")
    #m.createDatabase()
    #m.addPassword(name="new1", password=m.generate())
    ##m.getPassword(name="second", verbose=True)
    #m.c.execute("SELECT * FROM integrity")
    #print(m.c.fetchall())
    m.c.execute("SELECT * FROM passwords")
    print(m.c.fetchall())
    #m.deletePassword(name= "new1")
    ##m.c.execute("SELECT * FROM integrity")
    #print(m.c.fetchall())
    #m.c.execute("SELECT * FROM passwords")
    #print(m.c.fetchall())
    #m.setData(name = "second", data={"password":"nowehaslo1", "username": "elo", "description": "jakiś tam opis"})
    #m.c.execute("SELECT * FROM integrity")
    #print(m.c.fetchall())
    
