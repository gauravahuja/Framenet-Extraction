try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
    
import sqlite3 as db
import sys
import os
from parseLUFile import * 
from parseFrameFile import * 
from createTables import *
from dropTables import *

from config import * 

def main():
    if (not dbName) or (not framenetPath):
        print "Varibles not set in config.py"
        sys.exit(0)
    
    conn = db.connect(dbName)
    c = conn.cursor()
    
    dropTables(c)
    conn.commit()
    createTables(c)
    conn.commit()
    print "Parsing LU Files"
    parseLUFiles(c, luPath = framenetPath+'/'+'lu'+'/')
    conn.commit()
    print "Parsing Frame files"
    parseFrameFiles(c, framePath =framenetPath+'/'+'frame'+'/')
    conn.commit()
    conn.close()
    print "Done"
    


if __name__ == "__main__":
    main()
