#!/usr/bin/python
# -*- coding: utf-8 -*-
# Jogo da velha
# Escrito por: Thalyson Alexandre Rodrigues de Sousa
# Data: 06 de Março de 2017
# Versão 1.0.0 - 11/04/2017

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

import sys
from src.GameBoard import *


class App:

    '''
    Classe Jogo da velha
    --------------------
    Controla a transição entre as janelas
    '''

    def __init__(self):
        self.menu = Menu()
        self.board = None
        self.start_game()

    def start_game(self):

        self.menu.initForm()

        if self.menu.namep1 is None:
            sys.exit(0)

        while True:

            self.board = GameBoard(self.menu.namep1, self.menu.namep2, self.menu.difficulty)
            self.board.initForm()

            if self.board.back:
                self.menu = Menu()
                self.menu.initForm()
                self.board = None

            elif self.board.restart:
                self.board = None

            if self.menu.quit:
                return

            if isinstance(self.board, GameBoard):
                if self.board.quit:
                    return


App()
