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


class Player:

    def __init__(self, name=None):
        self.name = name

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value
        self.key = Player.create_key(self.__name)

    @staticmethod
    def create_key(name):
        return name.replace(' ', '').strip().lower()
