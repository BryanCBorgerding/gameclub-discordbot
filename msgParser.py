#!/usr/bin/env python3
import argparse
import os
import sqlite3
import json
import random

class messageConstructor():
    Verbose = False
    databasePath = None

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
        query = f"""
        INSERT INTO UserID (Player, DiscordID) VALUES ('{User}','{ID}');
        """
        self._qsql(query)
        return
    
    def removeUserID(self, User):
        return

    def randomMessage(self):
        return

    def constructMessage(self):
        return

    

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
        case "findUser":
            data = msg.findUserID(args.function[1])
            if data != False:
                print(data)
        case "addUser":
            msg.addUserID(args.function[1],args.function[2])
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