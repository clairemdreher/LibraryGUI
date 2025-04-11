import sqlite3
import os

class Database:
    def __init__(root, db_name='library.db'):
        root.conn = sqlite3.connect(db_name)
        root.cursor = root.conn.cursor()
        root.initialize_db()
    
    def initialize_db(root):
        root.cursor.execute("""
            SELECT count(*) FROM sqlite_master
            WHERE type='table' AND name = 'Book_Inventory'
        """)

        if root.cursor.fetchone()[0] == 0:
            with open ('Database/create.sql', 'r') as f:
                root.cursor.executescript(f.read())

            with open('Database/insert.sql', 'r') as f:
                root.cursor.executescript(f.read())

        root.conn.commit()
    
    def execute_query(root, query, params=()):
        root.cursor.execute(query, params)
        root.conn.commit()
        return root.cursor
    
    def __del__(root):
        root.conn.close()