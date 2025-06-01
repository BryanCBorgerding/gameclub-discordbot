#!/usr/bin/env python3
import argparse
import os
import sqlite3
import json

class wheelSpin:
    """
    Private Variables
    """
    Verbose = False
    databasePath = None

    """
    Initialization Function. Checks verbosity and calls inits
    """
    def __init__(self, PATH, Verbose = False, ):
        if Verbose:
            print("Hello Spin!")
            self.Verbose = True
        self.initDB(PATH)
        return
    
    """
    Checks for database at a filepath, creates one if it doesn't exist
    """
    def initDB(self,path):
        self.databasePath = path
        if self.Verbose:
            print(f"Filepath is '{path}'")
        if os.path.isfile(path):
            if self.Verbose:
                print("Database already exists!")
            # if file exists, should return
            return True
        else:
            if self.Verbose:
                print(f"Database not found, creating new database at {path}!")
            # Need to create the database at that location
            query1 = f"""
            CREATE TABLE Pool (
	        id INTEGER PRIMARY KEY AUTOINCREMENT,
	        Player TEXT
            );
            """
            query2 = f"""
            CREATE TABLE Blacklist (
	        id INTEGER PRIMARY KEY AUTOINCREMENT,
	        Player TEXT
            );
            """
            self._qsql(query1)
            self._qsql(query2)       
            # Read in default player list from a JSON Config
            default = self._readConfig("config.json")
            default = default['DefaultPlayers']
            if default ==  False:
                # No config found, pass
                if self.Verbose:
                    print("No configuration file found: Tables will be empty!")
                return
            else:
                if self.Verbose:
                    print(f'Adding {default} to the pool!')
                for i in range(len(default)):
                    query = f"""
                    INSERT INTO Pool (Player) VALUES ('{default[i]}');
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

    """
    Checks the database for every player in the pool
    """ 
    def checkPool(self):
        query = f"""
        SELECT * FROM Pool;
        """
        data = self._qsql(query,read=True)
        print(data)
        return
    
    """
    Checks the database for every player in the blacklist.
    The intent of the blacklist is to prevent anyone from getting chosen more than once before the entire pool has been chosen
    """
    def checkBlacklist(self):
        query = f"""
        SELECT * FROM Blacklist; 
        """
        data = self._qsql(query,read=True)
        print(data)
        return
    
    """
    API to add a person to the pool
    """
    def addPlayer(self,playerName):
        query = f"""
        INSERT INTO Pool (Player) VALUES ('{playerName}');
        """
        self._qsql(query)
        return
    
    """
    API to remove a person from the pool
    """
    def dropPlayer(self,playerName):
        query = f"""
        DELETE FROM Pool WHERE Player = '{playerName}';
        """
        self._qsql(query)
        return
    
    """
    API to add a person to the un-allowable wheel choices
    """
    def add2Blacklist(self,playerName):
        query = f"""
        INSERT INTO Blacklist (Player) VALUES ('{playerName}');
        """
        self._qsql(query)
        return
    
    """
    API to remove a person from the un-allowable wheel choices
    """
    def clearFromBlacklist(self,playerName):
        query = f"""
        DELETE FROM Blacklist WHERE Player = '{playerName}';
        """
        self._qsql(query)
        return
    """
    API to spin the wheel and select a player
    """
    def spinTheWheel():
        #TODO Pull from Pool and Blacklist. Compare two and remove any matches. Roll a number between 1 and number of remaining players. Print result 
        return


def main():
    args = initParser()
    PATH = args.path 
    if args.verbose: 
        wheel = wheelSpin(PATH,Verbose=True)
    else:
        wheel = wheelSpin(PATH)
    match args.function[0]:
        case "checkPool":
            wheel.checkPool()
        case "checkBlacklist":
            wheel.checkBlacklist()
        case "addPlayer":
            wheel.addPlayer(args.function[1])
        case "addBlacklist":
            wheel.add2Blacklist(args.function[1])
        case "dropPlayer":
            wheel.dropPlayer(args.function[1])
        case "dropBlacklist":
            wheel.clearFromBlacklist(args.function[1])
        case "spin":
            wheel.spinTheWheel()
        case _:
            pass
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