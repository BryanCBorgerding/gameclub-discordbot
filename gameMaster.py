#!/usr/bin/env python3
import argparse
import os
import sqlite3


def main():
    return

def initParser():
    """
    Initializes the argument parsing, and adds arguments to the parser
    """
    parser = argparse.ArgumentParser(description="A tool to store game master history")
    parser.add_argument("path", help ="location to create/read database from")
    parser.add_argument("-v","--verbose", action="store_true", help ="prints more detailed outputs")
    parser.add_argument("-f","--function", nargs = "+", metavar=("FUNC","ARGS"), help ="executes a specific function")
    return parser.parse_args()

if __name__=="__main":
    main()