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


import tkinter.messagebox as msgbox
from tkinter import filedialog

from config import load
from config.config import *
from src.PlayerDatabase import *
from src.functions import *


class Scores:

    '''
    Classe de pontuação
    -------------------
    Esta classe é responsável por carregar as pontuações
    dos jogadores salva no banco de dados sqlite3
    '''

    def __init__(self, root, title, rows, columns):
        self._list = rows
        self._initWidgets(root, title, columns)

    # Cria todos os elementos necessários para a janela e o listbox
    def _initWidgets(self, root, title, columns):
        if len(columns) != 2:
            raise AttributeError("The length of <columns> must be two.")

        # criar janela
        self._window = functionDialog(title, root, "335x290", False)

        # Imagens
        self.imgRefresh = tk.PhotoImage(file=load.IMG['refresh'])
        self.imgExport  = tk.PhotoImage(file=load.IMG['save'])

        # Labels
        lblnum = tk.Label(self._window, text='N°', font=functionFontTk(10))
        label1 = tk.Label(self._window, text=columns[0], font=functionFontTk(10))
        label2 = tk.Label(self._window, text=columns[1], font=functionFontTk(10))
        lblnum.place(x=26, y=15)
        label1.place(x=50, y=15)
        label2.place(x=245, y=15)

        # Botões
        self.btnExport = ttk.Button(self._window, text="Exportar")
        self.btnExport.config(compound=tk.LEFT, image=self.imgExport)
        self.btnExport.config(style=functionFontTtk(8), command=self.evtExportData)
        self.btnExport.place(relx=0.3, rely=0.91, anchor=tk.CENTER)

        self.btnRefresh = ttk.Button(self._window, text="Atualizar")
        self.btnRefresh.config(compound=tk.LEFT, image=self.imgRefresh)
        self.btnRefresh.config(style=functionFontTtk(8), command=self._evtRefreshList)
        self.btnRefresh.place(relx=0.7, rely=0.91, anchor=tk.CENTER)

        # Frame para carregar a listbox
        self.frame = tk.Frame(self._window, height=100, width=80)
        self.frame.place(x=25, y=40)

        # Barra de rolagem de  Y
        scrollbary = tk.Scrollbar(self.frame, orient=tk.VERTICAL)

        # Listbox
        self.listbox = tk.Listbox(self.frame)
        self.listbox.config(width=38, height=13)
        self.listbox.config(yscrollcommand=scrollbary.set)
        self.listbox.config(font=functionFontTk(8, "normal", "Courier new"))
        self.listbox.config(selectmode=tk.EXTENDED)

        # Setar configurações Scrolls bar (Y)
        scrollbary.config(command=self.listbox.yview)
        scrollbary.pack(side=tk.RIGHT, fill=tk.Y)

        self.listbox.pack()

    def _evtRefreshList(self):
        self._connDB = PlayerDatabase(DATABASE)
        self._list = self._connDB.loadRecords()
        self.loadListBox("Sem recordes registrados.")

    def evtExportData(self):
        if not self._list:
            msgbox.showinfo("Aviso", "Não existe nada a ser exportardo.")
        else:
            try:
                filetxt = filedialog.asksaveasfile(mode="w", defaultextension=".txt",
                                                   initialdir="/", title="Exportar",
                                                   filetypes=(("Text files", "*.txt"),
                                                              ("All files", "*.*")))
            except EOFError:
                return

            # Se caso não salvar então retorna
            if filetxt is None:
                return

            for idx, item in enumerate(self._list):
                filetxt.write('%02.d|{0:-<68}{1:->9}\n'.format(item[0], item[1]) % (idx + 1))
            filetxt.close()

    def loadListBox(self, empty="Vazio"):
        self.listbox.delete(0, tk.END)
        if not self._list:
            self.listbox.insert(tk.END, empty)

        elif len(self._list[0]) == 2:
            for idx, item in enumerate(self._list):
                self.listbox.insert(tk.END, '%02.d|{0:-<25}{1:->9}'.format(item[0], item[1]) % (idx + 1))
        else:
            raise AttributeError('The <list> passed must be tuples of length two.')
