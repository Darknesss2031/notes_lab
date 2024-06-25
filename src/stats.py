import sqlite3
import os
from functools import cache


class StatsRepository:
    """Class to interact with statistics database"""

    def __init__(self):
        self.db_path = os.path.join("db", "storage.db")
        self.connection = sqlite3.connect(self.db_path)
    
    def setup(self):
        cur = self.connection.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS games_history (
                game_id INTEGER PRIMARY KEY AUTOINCREMENT,
                type TEXT,
                correct INTEGER DEFAULT 0,
                total INTEGER,
                timestamp TEXT
            );
        ''')
        cur.close()

    def get_games(self, offset, limit):
        cur = self.connection.cursor()
        cur.execute('''
            SELECT * FROM games_history WHERE game_id>=%d LIMIT %d;
        ''' % (offset+1, limit))
        result = cur.fetchall()
        cur.close()
        return result
    
    def add_game(self, type_, correct, total, timestamp):
        cur = self.connection.cursor()
        cur.execute('''
            INSERT INTO games_history (type, correct, total, timestamp) VALUES ('%s', %d, %d, '%s');
        ''' % (type_, correct, total, timestamp))
        cur.close()
        self.connection.commit()

    def daily_avg(self, timestamp):
        cur = self.connection.cursor()
        cur.execute('''
            SELECT avg(((correct * 1.0) / (total * 1.0)) * 100 FROM games_history WHERE timestamp=%s;
        ''' % (timestamp))
        result = cur.fetchone()
        cur.close()
        return result
    
    def number_of_games(self):
        cur = self.connection.cursor()
        cur.execute('''
            SELECT COUNT(*) FROM games_history;
        ''')
        result = cur.fetchone()
        cur.close()
        return result[0]
    
    def total_avg(self):
        cur = self.connection.cursor()
        cur.execute('''
            SELECT avg(((correct * 1.0) / (total * 1.0)) * 100 FROM games_history;
        ''')
        result = cur.fetchone()
        cur.close()
        return result