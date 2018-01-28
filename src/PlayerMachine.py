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


import src.TicTacToe as TicTacToe
from random import choice
from src.MiniMax import *


class PlayerMachine:

    '''
    Classe Jogador Máquina
    ----------------------
    Aqui é implementado as decisões de jogadas da
    máquina de acordo com as jogadas do player e a
    dificuldade selecionada
    '''

    def __init__(self, level, game):
        self._levels()
        self.level = self.checkLevel(level)
        self.game = PlayerMachine.checkType(game)
        self.CPU = MiniMax(self.game)

    def _levels(self):
        self.EASY = 1
        self.MEDIUM = 2
        self.HARD = 3

    def checkLevel(self, level):
        if not isinstance(level, int):
            raise TypeError("The level must be type integer")

        elif level < self.EASY or level > self.HARD:
            raise AttributeError("Between 1 and 3")
        return level

    # Verifica o nível selecionado e
    # retorna a jogada da CPU
    def getMove(self):

        if self.level == self.EASY:
            # Retorna uma jogada aleatória
            aleatory = []
            for position, e in enumerate(self.game.gameState):
                if e == 0:
                    aleatory.append(position)

            return choice(aleatory)

        elif self.level == self.MEDIUM:
            return self.CPU.decisionMinMax()

    @staticmethod
    def checkType(value):
            if isinstance(value, TicTacToe.TicTacToe):
                return value
            raise TypeError('Invalid type passed in parameter of function {CheckType}')
