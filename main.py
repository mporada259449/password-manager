import argparse
from manager import Manager
from os import path
#plik z interfejsem cli
def getData(data):
    important_data = ["password", "description", "name", "username"]
    return {k:v for k,v in data.items() if k in important_data}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Manager haseł")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--add", help = "add password", action="store_true", required=False)
    parser.add_argument("--generate", help = "generate password", action = "store_true", required = False)
    group.add_argument("--change", help= "change data connected to given name (password, username, description)", action="store_true" ,required=False)
    group.add_argument("--delete", help = "delete password with given name", action="store_true", required=False)
    group.add_argument("--create", help="create new file", action="store_true", required=False)
    group.add_argument("--get", help="get password by name", action="store_true", required = False)
    parser.add_argument("-p", "--password", help="password", type = str, required=False)
    parser.add_argument("-n", "--name", help="name", type = str , required=False)
    parser.add_argument("-d", "--description", help="description", type=str, required=False)
    parser.add_argument("-u", "--username", help="username", type = str, required=False)
    parser.add_argument("-f", "--file", help="database file", type = str, required= False, default="./passwords.db") #zmienić na True teraz to tylko do testów
    parser.add_argument("-v", help="print password", action = "store_true", required = False, default=False)

    args = parser.parse_args()
    print(vars(args))
    manager = Manager(args.file)
    if args.add == True:
        function_args = getData(vars(args))
        if args.generate == True:
            manager.addPassword(name = function_args["name"], password = manager.generate(), description=function_args["description"], username = function_args["username"] )
        else:
            manager.addPassword(name = function_args["name"], password = function_args["password"], description=function_args["description"], username = function_args["username"] )
    elif args.change == True:
        function_args = getData(vars(args))
        manager.setData(name = function_args["name"], data = {k:v for k,v in function_args.items() if k!="name"})
    elif args.delete == True:
        function_args = getData(vars(args))
        manager.deletePassword(name = function_args["name"])
    elif args.create == True:
        manager.createDatabase()
    elif args.get == True:
        manager.getPassword(args.name, verbose = args.v)

    manager.closeDatabase()
    