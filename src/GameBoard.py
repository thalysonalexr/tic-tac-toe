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


import time
import tkinter.messagebox as msgbox
from config import load
from config.config import *
from src.Menu import Menu
from src.PlayerDatabase import PlayerDatabase
from src.PlayerMachine import PlayerMachine
from src.TicTacToe import TicTacToe
from src.functions import *


class GameBoard(Menu):

    '''
    Classe Tabuleiro
    ----------------
    Janela principal onde é executado as jogadas,
    lógica e vencedor, podendo ser a máquina ou os
    jogadores dependendo do modo escolhido
    '''

    def __init__(self, p1, p2, diff=None):
        self.game = TicTacToe()
        self._attributesBoard(p1, p2, diff)
        self._playersDatabase()
        self._status()
        self._initWidgets()

    def _attributesBoard(self, p1, p2, diff):
        self.namep1 = p1
        self.namep2 = p2
        self.difficulty = diff
        self.addpointp1 = self.addpointp2 = 0

        if diff is not None:
            self.CPU = PlayerMachine(self.difficulty, self.game)

    def _joystick(self):

        def filterKeys(event):
            if event.char in '123456789':
                self.KEYS[event.char]()

        for i in range(1, 10):
            self._root.bind(str(i), filterKeys)
            self.KEYS[str(i)] = self.BUTTONS[i-1].invoke

    def _status(self):
        self.back = self.restart = self.save = self.quit = False

    def _initWidgets(self):
        # Propriedades da janela
        self._root = tk.Tk()
        functionCenter(self._root)
        self._root.config(bg="white")
        self._root.title("Jogo da velha")
        self._root.resizable(False, False)
        self._root.geometry("220x370")
        self._root.protocol("WM_DELETE_WINDOW", self.evtQuit)
        self.PLACE_FIRST = [(16, 146), (86, 146), (155, 146), (16, 80),
                            (86, 80), (155, 80), (16, 13), (86, 13), (155, 13)]
        self.PLACE_LAST = [(12, 143), (81, 143), (150, 143), (12, 79),
                           (81, 79), (150, 79), (12, 14), (81, 14), (150, 14)]
        self.BUTTONS = []
        self.KEYS = {}

        # Criar menu
        menubar = tk.Menu(self._root)
        gamemenu = tk.Menu(menubar, tearoff=0)
        gamemenu.add_command(label="Menu Principal", font=functionFontTk(9), command=self.evtBackToMenu)
        gamemenu.add_command(label="Recordes      ", font=functionFontTk(9), command=self.evtLoadScores)
        gamemenu.add_command(label="Reiniciar     ", font=functionFontTk(9), command=self.evtRestart)
        gamemenu.add_command(label="Salvar        ", font=functionFontTk(9), command=self.evtSaveForm)
        gamemenu.add_separator()
        gamemenu.add_command(label="Sair", font=functionFontTk(9), command=self.evtQuit)
        menubar.add_cascade(label="Jogo", menu=gamemenu)

        helpmenu = tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label='Sobre', font=functionFontTk(9), command=self.evtAbout)
        menubar.add_cascade(label="Ajuda", menu=helpmenu)
        self._root.config(menu=menubar)

        # Frame para imagem de fundo do tabuleiro
        board = tk.Frame(self._root, width=220, height=200)
        board.pack_propagate(0)

        # Carregar imagens
        self.imgBoard = tk.PhotoImage(file=load.IMG['board'])
        self.imgScore = tk.PhotoImage(file=load.IMG['score'])
        self.imgDivide = tk.PhotoImage(file=load.IMG['divide'])
        self.imgTurnOf = tk.PhotoImage(file=load.IMG['turn'])
        self.imgiconX = tk.PhotoImage(file=load.IMG['x_small'])
        self.imgiconO = tk.PhotoImage(file=load.IMG['o_small'])
        self.imgX = tk.PhotoImage(file=load.IMG['x_icon'])
        self.imgO = tk.PhotoImage(file=load.IMG['o_icon'])

        # Elementos do form
        self._createButtons()
        self._joystick()
        self.lblbackground = tk.Label(board, bg="white", image=self.imgBoard)
        self.lblbackground.pack()
        self.lblPoints1 = tk.Label(self._root, text=0, bg="white", fg="red")
        self.lblPoints2 = tk.Label(self._root, text=0, bg="white", fg="blue")
        self.lblPoints1.config(font=functionFontTk(25, "bold", "Arial Rounded MT Bold"))
        self.lblPoints2.config(font=functionFontTk(25, "bold", "Arial Rounded MT Bold"))
        self.lblicon = tk.Label(self._root, image=self.imgiconX)
        self.lblicon.config(width=25, height=25, bg="white")
        self.lblplayer = tk.Label(self._root, bg="white", fg="dim gray", font=functionFontTk(10, "bold"))
        self.lblplayer.config(text=functionSplit(self.namep1.name, 12))

        lblinf1 = tk.Label(self._root, image=self.imgScore, bg="white", width=85, height=25)
        lblinf2 = tk.Label(self._root, image=self.imgDivide, bg="white", width=10, height=100)
        lblinf3 = tk.Label(self._root, image=self.imgTurnOf, bg="white", width=85, height=25)
        lblname1 = tk.Label(self._root, bg="white", font=functionFontTk(11, "bold"))
        lblname2 = tk.Label(self._root, bg="white", font=functionFontTk(11, "bold"))
        lblname1.config(text=functionSplit(self.namep1.name, 13))
        lblname2.config(text=functionSplit(self.namep2.name, 13))

        self.lblPoints1.place(x=33, y=265)
        self.lblPoints2.place(x=150, y=265)
        self.lblicon.place(x=90, y=320)
        self.lblplayer.place(x=120, y=323)
        board.place(x=0, y=5)
        lblinf1.place(x=1, y=205)
        lblinf2.place(x=103, y=215)
        lblinf3.place(x=1, y=320)
        lblname1.place(x=1, y=235)
        lblname2.place(x=116, y=235)

    def _createButtons(self):

        for i in range(9):
            self.BUTTONS.append(tk.Button(self._root))
            self.BUTTONS[i].config(width=6, height=3, bd=0, bg="white", cursor="hand1")
            self.BUTTONS[i].place(x=self.PLACE_FIRST[i][0], y=self.PLACE_FIRST[i][1])

        self.BUTTONS[0].config(
            command=lambda: self.registerPlay(self.BUTTONS[0], 0, self.PLACE_LAST[0][0], self.PLACE_LAST[0][1]))
        self.BUTTONS[1].config(
            command=lambda: self.registerPlay(self.BUTTONS[1], 1, self.PLACE_LAST[1][0], self.PLACE_LAST[1][1]))
        self.BUTTONS[2].config(
            command=lambda: self.registerPlay(self.BUTTONS[2], 2, self.PLACE_LAST[2][0], self.PLACE_LAST[2][1]))
        self.BUTTONS[3].config(
            command=lambda: self.registerPlay(self.BUTTONS[3], 3, self.PLACE_LAST[3][0], self.PLACE_LAST[3][1]))
        self.BUTTONS[4].config(
            command=lambda: self.registerPlay(self.BUTTONS[4], 4, self.PLACE_LAST[4][0], self.PLACE_LAST[4][1]))
        self.BUTTONS[5].config(
            command=lambda: self.registerPlay(self.BUTTONS[5], 5, self.PLACE_LAST[5][0], self.PLACE_LAST[5][1]))
        self.BUTTONS[6].config(
            command=lambda: self.registerPlay(self.BUTTONS[6], 6, self.PLACE_LAST[6][0], self.PLACE_LAST[6][1]))
        self.BUTTONS[7].config(
            command=lambda: self.registerPlay(self.BUTTONS[7], 7, self.PLACE_LAST[7][0], self.PLACE_LAST[7][1]))
        self.BUTTONS[8].config(
            command=lambda: self.registerPlay(self.BUTTONS[8], 8, self.PLACE_LAST[8][0], self.PLACE_LAST[8][1]))

    def _destroyButtons(self):
        for button in self.BUTTONS:
            button.destroy()
        self.BUTTONS.clear()

    def _playersDatabase(self):
        self._playerDB = PlayerDatabase(DATABASE)
        self._playerDB.registerPlayer(self.namep1)
        if self.difficulty is None:
            self._playerDB.registerPlayer(self.namep2)

    def _turnUpdate(self, img, player):
        self.lblicon.config(image=img)
        self.lblplayer.config(text=functionSplit(player, 12))

    def restartBoard(self):
        self._destroyButtons()
        self._createButtons()
        self._joystick()
        self.game.restart()
        self._turnUpdate(self.imgiconX, self.namep1.name)

    def showOld(self):
        msgbox.showinfo("Empate", "Ops! Deu velha =(")
        self.restartBoard()

    def saved(self):
        if self.difficulty is None:
            self.save = False
        else:
            if self.addpointp1 == 0:
                self.save = True
            else:
                self.save = False

    def updatePoints(self):
        if self.save:
            self.addpointp1 = self.addpointp2 = 0

        if self.game.turn == 1:
            self.game.pointsp1 += 1
            self.addpointp1 += 1
            self.lblPoints1.config(text=str(self.game.pointsp1))
        else:
            self.game.pointsp2 += 1
            self.addpointp2 += 1
            self.lblPoints2.config(text=str(self.game.pointsp2))

    def showWinner(self):
        msgbox.showinfo("Ganhou!", "Jogador '{0}' ({1}) ganhou!".format(
            "X" if self.game.turn == 1 else "O", functionSplit(
                self.namep1.name if self.game.turn == 1 else self.namep2.name, 10)))

        self.updatePoints()
        self.saved()
        self.restartBoard()

    def saveForm(self, function1, function2):
        if not self.save and (self.game.pointsp1 > 0 or self.game.pointsp2 > 0):
            save = msgbox.askyesnocancel("Salvar", "Salvar pontuação atual?")
            if save is None:
                return False
            elif save:
                self.evtSaveForm()
                function1()
            elif not save:
                function1()
        else:
            function2()
        return True

    def registerPlay(self, button, position, x, y):

        if self.game.checkTurn(position):

            if self.game.turn == 1:
                button.config(image=self.imgX)
                self._turnUpdate(self.imgiconO, self.namep2.name)
            else:
                button.config(image=self.imgO)
                self._turnUpdate(self.imgiconX, self.namep1.name)

            button.config(width=56)
            button.config(height=54)
            button.place(x=x, y=y)

            if self.game.winner:
                self.showWinner()
                return
            elif 0 not in self.game.gameState:
                self.showOld()
                return

            self.game.changeTurn()

            if self.difficulty is not None and self.game.turn == 2:
                # Atualiza a jogada do player, aguarda meio segundo e
                # executa a jogada da máquina
                self._root.update()
                time.sleep(0.5)  # Delay opcional
                self.evtPlayerMachine()

    # Eventos

    def evtPlayerMachine(self):
        played = self.CPU.getMove()

        for i in range(9):
            if played == i:
                self.registerPlay(self.BUTTONS[i], i, self.PLACE_LAST[i][0], self.PLACE_LAST[i][1])
                break

    def evtSaveForm(self):
        if not self.save:
            self._playerDB.registerPoints(self.namep1, self.addpointp1)

            if self.difficulty is None:
                self._playerDB.registerPoints(self.namep2, self.addpointp2)

            self.save = True

        msgbox.showinfo("Jogo", "Jogo salvo!")

    def evtQuit(self):
        self.quit = self.saveForm(self._root.destroy, self.evtQuitForm)

    def evtQuitForm(self):
        if msgbox.askyesno("Sair", "Deseja realmente sair?"):
            self.quit = True
            self._root.destroy()

    def evtRestart(self):
        self.restart = self.saveForm(self._root.destroy, self.evtRestartForm)

    def evtRestartForm(self):
        if msgbox.askyesno("Reiniciar", "Tem certeza que deseja reiniciar?"):
            self.restart = True
            self._root.destroy()

    def evtBackToMenu(self):
        self.back = self.saveForm(self._root.destroy, self.evtBackToMenuForm)

    def evtBackToMenuForm(self):
        if msgbox.askyesno("Voltar", "Voltar ao menu?"):
            self.back = True
            self._root.destroy()
