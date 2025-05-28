#!/usr/bin/env python3
import argparse
import os
import sqlite3

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
        return

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