#!/usr/bin/env python3
import argparse
import os
import sqlite3
import json
import random

class messageConstructor():
    Verbose = False
    databasePath = None
    msgDefault = [
        "And the Winner is... '$USER'"
    ]

    def __init__(self, PATH, Verbose = False):
        if Verbose:
            print("Hello messages!")
            self.Verbose = True
        self.initDB(PATH)
        return

    def initDB(self, path):
        self.databasePath = path
        if self.Verbose:
            print(f"Filepath is '{path}'")
        if os.path.isfile(path):
            if self.Verbose:
                print("Database already exists!")
            return True
        else:
            if self.Verbose:
                print(f"Database not found, creating new database at {path}!")
            # Need to create new Database at that location!
            query = f"""
            CREATE TABLE UserID (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Player TEXT,
            DiscordID INTEGER
            );
            """
            self._qsql(query)
            # Read in default player list from a JSON Config
            default = self._readConfig("config.json")
            if default ==  False:
                # No config found, pass
                if self.Verbose:
                    print("No configuration file found: Table will be empty!")
                return
            else:
                default = default["DefaultUserIDs"]
                if self.Verbose:
                    print(f"Adding UserID Defaults to table!")
                for name,ID in default.items():
                    if self.Verbose:
                        print(f"Adding UserID for user {name}!")
                    query = f"""
                    INSERT INTO UserID (Player, DiscordID) VALUES ('{name}','{ID}');
                    """
                    self._qsql(query)
            return
    """
    Helper function to handle all of the sql querying
    """
    def _qsql(self,QUERY,read = False):
        path = self.databasePath
        with sqlite3.connect(path) as conn:
            cursor = conn.cursor()
            cursor.execute(QUERY)
            if read:
                data = cursor.fetchall()
                return data
            else:
                return

    """
    Checks for a config file, if present, it uses it to populate the database, if not returns a false
    """
    def _readConfig(self,path):
        if os.path.isfile(path):
            if self.Verbose:
                print("Reading config file")
            with open(path, 'r') as file:
                config = json.load(file)
            return config
        else:
            return False

    def printDB(self):
        query = f"""
        SELECT * FROM UserID;
        """
        data = self._qsql(query,read=True)
        return data

    def findUserID(self, User):
        try:
            query = f"""
            SELECT DiscordID FROM UserID WHERE Player = '{User}';
            """
            data = self._qsql(query,read=True)
            return data[0][0]
        except Exception as e:
            print("User Not Found! Add them first using addUser")
            return False
    
    def addUserID(self, User, ID):
        if self.Verbose:
            print(f"Adding {User} to the database with ID {ID}")
        query = f"""
        INSERT INTO UserID (Player, DiscordID) VALUES ('{User}','{ID}');
        """
        self._qsql(query)
        return
    
    def removeUserID(self, User):
        if self.Verbose:
            print(f"Removing {User} from the Database!")
        query = f"""
        DELETE FROM UserID WHERE Player = '{User}';
        """
        self._qsql(query)
        return

    def _readMessages(self):
        conf = self._readConfig("config.json")
        if conf ==  False:
                # No config found, pass
                if self.Verbose:
                    print("No configuration file found! will use the default message")
                return self.msgDefault
        try:
            messages = conf["CustomMessages"]
            return messages
        except Exception as e:
            if self.Verbose:
                print("No messages found in the configuration file, will use the default message")
            return self.msgDefault
            


    def randomMessage(self):
        # Custom messages are not stored in any database, they will be pulled from config.json during runtime!
        messages = self._readMessages()
        length = len(messages)
        rand = random.randint(0, length-1)
        return messages[rand]

    def constructMessage(self, User):
        message = self.randomMessage()
        newMessage = message.replace("'$USER'", User)
        return newMessage

    

def main():
    args = initParser()
    PATH = args.path
    if args.verbose:
        msg = messageConstructor(PATH, Verbose=True)
    else:
        msg = messageConstructor(PATH)
    if not args.function:
        return
    match args.function[0]:
        case "printDB":
            print(msg.printDB())
        case "findUser":
            data = msg.findUserID(args.function[1])
            if data != False:
                print(data)
        case "addUser":
            msg.addUserID(args.function[1],args.function[2])
        case "removeUser":
            msg.removeUserID(args.function[1])
        case "randMessage":
            print(msg.randomMessage())
    return


def initParser():
    """
    Initializes the argument parsing, and adds arguments to the parser
    """
    parser = argparse.ArgumentParser(description="A tool to do random wheel spins")
    parser.add_argument("path", help ="location to create/read database from")
    parser.add_argument("-v","--verbose", action="store_true", help ="prints more detailed outputs")
    parser.add_argument("-f","--function", nargs = "+", metavar=("FUNC","ARGS"), help ="executes a specific function")
    return parser.parse_args()

if __name__ == "__main__":
    main()