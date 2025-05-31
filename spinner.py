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
            with sqlite3.connect(path) as conn:
                conn.execute(query1)
                conn.execute(query2)
            
            # Read in default player list from a JSON Config
            default = self.readConfig("config.json")
            if default ==  False:
                # No config found, pass
                if self.Verbose:
                    print("No configuration file found: Tables will be empty!")
                return
            else:
                return
    """
    Checks for a config file, if present, it uses it to populate the database, if not returns a false
    """
    def readConfig(self,path):
        if os.path.isfile(path):
            return
        else:
            return False

    """
    Checks the database for every player in the pool
    """ 
    def checkPool(self):
        return
    
    """
    Checks the database for every player in the blacklist.
    The intent of the blacklist is to prevent anyone from getting chosen more than once before the entire pool has been chosen
    """
    def checkBlacklist(self):
        return
    
    """
    API to add a person to the pool
    """
    def addPlayer(self,playerName):
        return
    
    """
    API to remove a person from the pool
    """
    def dropPlayer(self,playerName):
        return
    
    """
    API to add a person to the un-allowable wheel choices
    """
    def add2Blacklist(self,playerName):
        return
    
    """
    API to remove a person from the un-allowable wheel choices
    """
    def clearFromBlacklist(self,playerName):
        return


def main():
    args = initParser()
    PATH = args.path 
    if args.verbose: 
        wheel = wheelSpin(PATH,Verbose=True)
    else:
        wheel = wheelSpin(PATH)
    return

def initParser():
    """
    Initializes the argument parsing, and adds arguments to the parser
    """
    parser = argparse.ArgumentParser(description="A tool to do random wheel spins")
    parser.add_argument("path",help="location to create/read database from")
    parser.add_argument("-v","--verbose", action="store_true", help="prints more detailed outputs")
    return parser.parse_args()

if __name__ == "__main__":
    main()