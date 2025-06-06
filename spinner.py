#!/usr/bin/env python3
import argparse
import os
import sqlite3
import json
import random

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
        return data
    
    """
    Checks the database for every player in the blacklist.
    The intent of the blacklist is to prevent anyone from getting chosen more than once before the entire pool has been chosen
    """
    def checkBlacklist(self):
        query = f"""
        SELECT * FROM Blacklist; 
        """
        data = self._qsql(query,read=True)
        return data
    
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
    def spinTheWheel(self):
        #TODO Pull from Pool and Blacklist. Compare two and remove any matches. Roll a number between 1 and number of remaining players. Print result
        # Get pool from db
        pool = self.checkPool()
        # process it a bit
        pool = [name for _, name in pool]
        if self.Verbose:
            print(f"Current entries in pool: {pool}")
        # Get blacklist from db
        bl = self.checkBlacklist()
        # process it a bit
        bl = [name for _, name in bl]
        if self.Verbose:
            print(f"Current entries in blacklist: {bl}")
        # do the comparison
        Entrants = [name for name in pool if name not in bl]
        if self.Verbose:
            print(f"And the entrants are... {Entrants}")
        length = len(Entrants)
        if length == 0:
            # Pool is empty for some reason...
            print("Error: Number of Entrants is zero... Please add players to the pool")
            return
        rand = random.randint(0, length-1)
        if self.Verbose:
            print(f"Random number selection result: {rand}")
        win = Entrants[rand]
        if self.Verbose:
            print(f"And the winner is... {win}!")
        # Now, need to add winner to blacklist
        if self.Verbose:
            print(f"Adding {win} to the blacklist")
        bl.append(win)
        # Check if blacklist is equal to the pool
        if set(pool) == set(bl):
            # Empty the blacklist
            if self.Verbose:
                print("Blacklist is full! Everyone has had a turn, so let's reset to zero...")
            for i in range(len(bl)):
                self.clearFromBlacklist(bl[i])
        else:
            # push new entry to database
            self.add2Blacklist(win)
        return win


def main():
    args = initParser()
    PATH = args.path 
    if args.verbose: 
        wheel = wheelSpin(PATH,Verbose=True)
    else:
        wheel = wheelSpin(PATH)
    if not args.function:
        return
    match args.function[0]:
        case "checkPool":
            print(wheel.checkPool())
        case "checkBlacklist":
            print(wheel.checkBlacklist())
        case "addPlayer":
            wheel.addPlayer(args.function[1])
        case "addBlacklist":
            wheel.add2Blacklist(args.function[1])
        case "dropPlayer":
            wheel.dropPlayer(args.function[1])
        case "dropBlacklist":
            wheel.clearFromBlacklist(args.function[1])
        case "spin":
            winner = wheel.spinTheWheel()
            print(f"And the winner is... {winner}!")
        case _:
            print("Invalid command!")
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