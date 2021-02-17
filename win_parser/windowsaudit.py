"""
Navigating Directories and FilePaths 
Use the os.path.join() function to combine folders with the correct slash.
The current working directory is the oflder that any relative paths are relative to.
os.getcwd() will return the current working directory.
os.chdir() will change the current working directory.
os.path.abspath() returns an absolute path form of the path passed to it.
os.path.relpath() returns the relative path between two paths passed to it.
os.makedirs() can make folders.
os.path.getsize() returns a file's size.
os.listdir() returns a list of strings of filenames.
os.path.exists() returns True if the filename passed to it exists.
os.path.isfile() and os.path.isdir() return True if they were passed a filename or file path. 

Reading and Writing Plaintext Files
The open() function will return a file object which has reading and writing –related methods.
Pass ‘r' (or nothing) to open() to open the file in read mode. Pass ‘w' for write mode. Pass ‘a' for append mode.
Opening a nonexistent filename in write or append mode will create that file.
Call read() or write() to read the contents of a file or write a string to a file.
Call readlines() to return a list of strings of the file's content.
Call close() when you are done with the file.
The shelve module can store Python values in a binary file.
The shelve.open() function returns a dictionary-like shelf value.
"""

import os, winreport, string, random
from winsys import WinSys

def parseDirectory(dir:str, option:str) -> list: #List of WinSys objects
    systems = []
    if (directoryIsValid(dir)):
        for filename in os.listdir(dir):
            filepath = os.path.join(dir, filename)
            data = open(filepath).readlines()
            systems.append(WinSys(data, option))
    return systems

def directoryIsValid(dir:str) -> bool:
    if (not os.path.exists(dir)):
        print("Invalid path: " + dir)
        return False
    for filename in os.listdir(dir):
        if (not filename.endswith('.txt')):
            print("ATTENTION:" + filename + " was not recognized as plaintext (.txt). File has been skipped.")
            return False
    return True

if __name__ == "__main__":
    currentDir = os.getcwd()
    evidenceDir = os.path.join(os.getcwd(), "Windows OS Sample Set")
    systems = parseDirectory(evidenceDir, 'script')




    
    




         




    
