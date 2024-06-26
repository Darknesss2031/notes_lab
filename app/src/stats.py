"""This file contains rules to work with the database."""

import sqlite3
import os


class StatsRepository:
    """Class to interact with statistics database."""

    def __init__(self):
        """Initialise function of stats repository class."""
        self.db_path = os.path.join(os.path.dirname(__file__),
                                    "..", "db", "storage.db")
        self.connection = sqlite3.connect(self.db_path)

    def setup(self):
        """Call to set up the database."""
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
        """Call to get games from database."""
        cur = self.connection.cursor()
        cur.execute('''
            SELECT * FROM games_history WHERE game_id>=%d LIMIT %d;
        ''' % (offset+1, limit))
        result = cur.fetchall()
        cur.close()
        return result

    def add_game(self, type_, correct, total, timestamp):
        """Call to add the game to database."""
        cur = self.connection.cursor()
        cur.execute('''
            INSERT INTO games_history (type, correct, total,
            timestamp) VALUES ('%s', %d, %d, '%s');
        ''' % (type_, correct, total, timestamp))
        cur.close()
        self.connection.commit()

    def daily_avg(self, timestamp):
        """Call to count the average score of the day."""
        cur = self.connection.cursor()
        cur.execute('''
            SELECT avg(((correct * 1.0) / (total * 1.0)) * 100 FROM
            games_history WHERE timestamp=%s;
        ''' % (timestamp))
        result = cur.fetchone()
        cur.close()
        return result

    def number_of_games(self):
        """Call to get the number of games."""
        cur = self.connection.cursor()
        cur.execute('''
            SELECT COUNT(*) FROM games_history;
        ''')
        result = cur.fetchone()
        cur.close()
        return result[0]

    def total_avg(self):
        """Call to count the average score of all time."""
        cur = self.connection.cursor()
        cur.execute('''
            SELECT avg(((correct * 1.0) / (total * 1.0)) *
            100 FROM games_history;
        ''')
        result = cur.fetchone()
        cur.close()
        return result
