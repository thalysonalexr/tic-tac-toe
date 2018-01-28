# -*- coding: utf-8 -*-
#   This file is part of Jogo da velha.
#
#   Jogo da velha is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 2 of the License, or
#   (at your option) any later version.
#
#   Jogo da velha is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with Jogo da velha; if not, write to the Free Software
#   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA


from src.Player import *
from src.ConnectDB import *


class PlayerDatabase:

    def __init__(self, namedb):
        self._db = ConnectDB(namedb)
        self._namedb = namedb + '.db'
        self.__createTable()

    def __createTable(self):
        import os.path
        if not os.path.exists(self._namedb):
            try:
                self._db.createConnection()
                self._db.cursor.execute('''
                    CREATE TABLE players(
                      key_player VARCHAR (25) PRIMARY KEY,
                      pla_name VARCHAR (25) NOT NULL UNIQUE,
                      pla_pontuation INTEGER NOT NULL)''')
            except:
                raise sqlite3.OperationalError('Error on create a table.')
            self._db.closeConnection()

    def playerExists(self, player):
        PlayerDatabase.checkType(player)
        self._db.createConnection()
        self._db.cursor.execute("SELECT pla_name FROM players WHERE key_player = ?", (player.key,))
        consult = self._db.cursor.fetchone()
        self._db.closeConnection()
        if consult is None:
            return False
        return True

    def registerPlayer(self, player):
        if not self.playerExists(player):
            self._db.createConnection()
            try:
                self._db.cursor.execute('''
                INSERT INTO players (key_player, pla_name, pla_pontuation)
                VALUES (?, ?, ?)''', (player.key, player.name, 0))
            except sqlite3.OperationalError:
                self._db.conn.rollback()
            else:
                self._db.conn.commit()
            self._db.closeConnection()

    def registerPoints(self, player, points):
        self._db.createConnection()
        try:
            self._db.cursor.execute("SELECT pla_pontuation FROM players WHERE key_player = ?", (player.key,))
            points = int(self._db.cursor.fetchone()[0]) + points
            self._db.cursor.execute("UPDATE players SET pla_pontuation = ? WHERE key_player = ?", (points, player.key))
        except sqlite3.OperationalError:
            self._db.conn.rollback()
        else:
            self._db.conn.commit()
        self._db.closeConnection()

    def loadRecords(self):
        registers = []
        self._db.createConnection()
        try:
            self._db.cursor.execute('''
            SELECT pla_name, pla_pontuation 
            FROM players ORDER BY pla_pontuation DESC''')

            while True:
                consult = self._db.cursor.fetchone()
                if consult is None:
                    break
                registers.append(consult)

        except sqlite3.OperationalError:
            self._db.conn.rollback()
        else:
            self._db.conn.commit()

        self._db.closeConnection()
        return registers

    @staticmethod
    def checkType(objectP):
        if not isinstance(objectP, Player):
            raise TypeError("Invalid type! The passed parameter must be of class <Player>")
