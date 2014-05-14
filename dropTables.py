import sqlite3 as db
import sys
import os

def dropTables(c):

    frameTable = """DROP TABLE IF EXISTS FRAME"""

    luTable = """DROP TABLE IF EXISTS LU"""

    feTable = """DROP TABLE IF EXISTS FE"""

    feAnnotationTable = """DROP TABLE IF EXISTS FEAnnotation"""
                                
    sentTable = """DROP TABLE IF EXISTS Sent"""

    c.execute(frameTable)
    c.execute(luTable)
    c.execute(feTable)
    c.execute(feAnnotationTable)
    c.execute(sentTable)

