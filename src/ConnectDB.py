import sqlite3


class ConnectDB:

    def __init__(self, namedb):
        self.conn = None
        self.cursor = None
        self.namedb = namedb

    def createConnection(self):
        try:
            self.conn = sqlite3.connect((self.namedb + '.db') if '.db' not in self.namedb else self.namedb)
            self.cursor = self.conn.cursor()
        except sqlite3.Error:
            raise Exception('Error on connect to database.')

    def closeConnection(self):
        try:
            self.cursor.close()
            self.conn.close()
        except sqlite3.Error:
            raise Exception('Error on closed database.')
