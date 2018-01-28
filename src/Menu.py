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


import webbrowser

from config.config import *
from src.Scores import *

__title__ = "Jogo da Velha"
__author__ = "Thalyson A. Rodrigues de Sousa"
__date__ = "2017-03-06"
__version__ = "1.0.0"
__source__ = "https://github.com/thalysonrodrigues"



class Menu:

    '''
    Janela inicial para entrada de dados, validação e inicio do jogo
    '''

    def __init__(self):
        self._attributesMenu()
        self._playerDB = PlayerDatabase(DATABASE)
        self._initWidgets()

    def _attributesMenu(self):
        self.namep1 = None
        self.namep2 = None
        self.difficulty = None
        self.quit = False

    def _initWidgets(self):
        # Propriedades da janela
        self._root = tk.Tk()
        functionCenter(self._root)
        self._root.geometry("335x235")
        self._root.title("Jogo da velha")
        self._root.resizable(False, False)
        self._root.protocol("WM_DELETE_WINDOW", self.evtQuit)

        # Criar menu
        self.menubar = tk.Menu(self._root)
        self.gamemenu = tk.Menu(self.menubar, tearoff=0)
        self.gamemenu.add_command(label="Recordes", font=functionFontTk(9), command=self.evtLoadScores)
        self.gamemenu.add_command(label="Sair", font=functionFontTk(9), command=self.evtQuit)
        self.menubar.add_cascade(label="Jogo", menu=self.gamemenu)
        self.helpmenu = tk.Menu(self.menubar, tearoff=0)
        self.helpmenu.add_command(label="Sobre J.V", font=functionFontTk(9), command=self.evtAbout)
        self.menubar.add_cascade(label="Ajuda", menu=self.helpmenu)
        self._root.config(menu=self.menubar)

        # Carregar imagens
        self.imgBackground  = tk.PhotoImage(file=load.IMG['tic_tac_toe'])
        self.imgPlayerVsPC  = tk.PhotoImage(file=load.IMG['player1'])
        self.imgTwoPlayers  = tk.PhotoImage(file=load.IMG['player2'])
        self.imgSelect      = tk.PhotoImage(file=load.IMG['select'])
        self.imgPlayers     = tk.PhotoImage(file=load.IMG['xo'])

        # Frame para imagem de fundo
        self.frame = tk.Frame(self._root, width=335, height=285)
        self.frame.pack_propagate(0)
        self.frame.pack()

        # Botões e labels
        self.btnPlayerVsPC = tk.Button(self._root, image=self.imgPlayerVsPC)
        self.btnPlayerVsPC.config(bd=0, command=self._evtOnePlayer, cursor="hand2")
        self.btnPlayerVsPC.config(width=140, height=15)
        self.btnPlayerVsPC.focus()
        self.btnTwoPlayers = tk.Button(self._root, image=self.imgTwoPlayers)
        self.btnTwoPlayers.config(bd=0, command=self._evtTwoPlayers, cursor="hand2")
        self.btnTwoPlayers.config(width=160, height=15)
        self.lblSelect = tk.Label(self._root, image=self.imgSelect)
        self.lblSelect.config(width=10, height=10)
        self.lblSelect.place(relx=0.15, rely=0.51)

        varselect = [False]
        height = [0.51]

        def callbackselect(label, x, y, var):
            label.place(relx=x, rely=y)
            if y == 0.51:
                var[0] = True
            else:
                var[0] = False

        def callbackenter(height):
            if height[0] == 0.51:
                self._evtOnePlayer()
            else:
                self._evtTwoPlayers()

        def callbacktab(label, height):
            if height[0] == 0.51:
                label.place(relx=0.15, rely=0.65)
                height[0] = 0.65
            else:
                label.place(relx=0.15, rely=0.51)
                height[0] = 0.51

        self.btnPlayerVsPC.bind("<Enter>", lambda event: callbackselect(self.lblSelect, 0.15, 0.51, varselect))
        self.btnTwoPlayers.bind("<Enter>", lambda event: callbackselect(self.lblSelect, 0.15, 0.65, varselect))

        self._root.bind("<Up>", lambda event: callbackselect(self.lblSelect, 0.15, 0.51, varselect))
        self._root.bind("<Down>", lambda event: callbackselect(self.lblSelect, 0.15, 0.65, varselect))
        self._root.bind("<Return>", lambda event: callbackenter(height))
        self._root.bind("<Tab>", lambda event: callbacktab(self.lblSelect, height))

        self.btnPlayerVsPC.place(relx=0.22, rely=0.50)
        self.btnTwoPlayers.place(relx=0.23, rely=0.64)

        self.lblBackground = tk.Label(self.frame, image=self.imgBackground).pack()

    def initForm(self):
        self._root.mainloop()

    def newGame(self, cmd):
        form = functionDialog("Novo jogo", self._root, "210x130")
        form.transient(self._root)
        form.grab_set()
        form.config(bg="white")

        def selected(event):
            if self.forminput.focus_get() is btnok:
                cmd()
            elif self.forminput.focus_get() is btncancel:
                self.forminput.destroy()

        form.bind("<Return>", selected)

        btnok = ttk.Button(form, text="Confirmar", cursor="hand2")
        btnok.config(style=functionFontTtk(9), width=10, command=cmd)
        btncancel = ttk.Button(form, text="Cancelar", cursor="hand2")
        btncancel.config(style=functionFontTtk(9), width=10, command=form.destroy)

        btnok.place(relx=0.1, rely=0.65)
        btncancel.place(relx=0.52, rely=0.65)
        return form

    # Eventos
    def _evtOnePlayer(self):
        self.forminput = self.newGame(self._evtButtonOk1)

        lblinf = tk.Label(self.forminput, text="Nome do jogador")
        lblinf.config(font=functionFontTk(8), bg="white")
        lblinf.pack(fill=tk.X)

        sv1 = tk.StringVar()
        sv1.trace("w", lambda name, index, mode, sv=sv1: Menu.limitChar(sv1, 25))

        self.iptplayer1 = ttk.Entry(self.forminput, textvariable=sv1, width=27)
        self.iptplayer1.focus()
        self.iptplayer1.place(relx=0.1, rely=0.15)

        lbldif = tk.Label(self.forminput, text="Dificuldade:", bg="white")
        lbldif.place(relx=0.08, rely=0.4)

        self.cmbdif = ttk.Combobox(self.forminput)
        self.cmbdif.config(values=["Fácil", "Difícil"])
        self.cmbdif.config(state="readonly", width=13)
        self.cmbdif.current(0)
        self.cmbdif.place(relx=0.42, rely=0.4)

    def _evtTwoPlayers(self):
        self.forminput = self.newGame(self._evtButtonOk2)

        sv1 = tk.StringVar()
        sv2 = tk.StringVar()
        sv1.trace("w", lambda name, index, mode, sv=sv1: Menu.limitChar(sv1, 25))
        sv2.trace("w", lambda name, index, mode, sv=sv2: Menu.limitChar(sv2, 25))

        self.iptplayer1 = ttk.Entry(self.forminput, textvariable=sv1, width=25)
        self.iptPlayer2 = ttk.Entry(self.forminput, textvariable=sv2, width=25)

        lblinf = tk.Label(self.forminput, text="Entre com os nomes dos jogadores")
        lblinf.config(font=functionFontTk(8), bg="white")
        lblplayers = tk.Label(self.forminput, image=self.imgPlayers)
        lblplayers.config(width=25, height=55, bg="white")

        lblinf.pack(fill=tk.X)
        lblplayers.place(x=3, y=23)
        self.iptplayer1.place(x=35, y=28)
        self.iptPlayer2.place(x=35, y=55)
        self.iptplayer1.focus()

    def _evtButtonOk1(self, event=None):
        error = None

        if not self.iptplayer1.get().strip():
            error = "Preencha o campo 'jogador'."

        elif len(self.iptplayer1.get().strip()) < 5:
            error = "O minímo de caracteres é 5."

        self.difficulty = self.cmbdif.current() + 1
        self._evtCheck(error, self.iptplayer1.get().strip(), "CPU")

    def _evtButtonOk2(self, event=None):
        error = None

        if not self.iptplayer1.get().strip() or not self.iptPlayer2.get().strip():
            error = "Preencha todos os campos!         "

        elif len(self.iptplayer1.get().strip()) < 5 or len(self.iptPlayer2.get().strip()) < 5:
            error = "O minímo de caracteres é 5.       "

        elif self.iptplayer1.get().lower().strip().replace(' ', '') == \
                self.iptPlayer2.get().lower().strip().replace(' ', ''):
            error = "Os jogadores devem ser diferentes!"

        self._evtCheck(error, self.iptplayer1.get().strip(), self.iptPlayer2.get().strip())

    def _evtCheck(self, error, ipt1=None, ipt2=None):
        if error is None:
            self.namep1 = Player(ipt1)
            self.namep2 = Player(ipt2)
            self.forminput.destroy()
            self._root.destroy()
        else:
            lblerror = tk.Label(self.forminput, text=error)
            lblerror.config(font=functionFontTk(8), bg="white", fg="red")
            lblerror.place(relx=0.10, rely=0.85)

    def evtQuit(self):
        self.quit = True
        self._root.destroy()

    def evtLoadScores(self):
        lstbox = Scores(self._root, "Recordes", self._playerDB.loadRecords(), ['Jogador', 'Pontos'])
        lstbox.loadListBox("Sem recordes registrados.")

    def evtAbout(self):

        self.about = functionDialog("Sobre", self._root, "300x170", False)

        def callback1(event):
            webbrowser.open_new(event.widget.cget("text"))

        lbltitle = tk.Label(self.about, text=__title__)
        lbltitle.config(font=functionFontTk(9, "bold"))
        lbltitle.pack(side=tk.TOP, pady=10)

        lblauthor = tk.Label(self.about, text=("Autor: " + __author__))
        lblauthor.config(font=functionFontTk(9))
        lblauthor.place(relx=0.05, rely=0.20)

        lbldate = tk.Label(self.about, text=("Data: " + __date__))
        lbldate.config(font=functionFontTk(9))
        lbldate.place(relx=0.05, rely=0.32)

        lblversion = tk.Label(self.about, text=("Versão: " + __version__))
        lblversion.config(font=functionFontTk(9))
        lblversion.place(relx=0.05, rely=0.44)

        lblsource = tk.Label(self.about, text="Source: ")
        lblsource.config(font=functionFontTk(9))
        lblsource.place(relx=0.05, rely=0.56)

        lblgit = tk.Label(self.about, text=__source__, fg="blue")
        lblgit.config(cursor="hand2", font=functionFontTk(9))
        lblgit.bind("<Button-1>", callback1)
        lblgit.place(relx=0.2, rely=0.56)

        self.imgPython = tk.PhotoImage(file=load.IMG['python_png'])
        lblpython = tk.Label(self.about, text="Copyright PSF [US] ")
        lblpython.config(compound=tk.RIGHT, image=self.imgPython)
        lblpython.config(font=functionFontTk(9))
        lblpython.place(relx=0.05, rely=0.66)

    # Limita a quantidade de caracteres de entrada
    @staticmethod
    def limitChar(sv, tam):
        c = sv.get()[0:tam]
        sv.set(c)
