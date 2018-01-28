import tkinter as tk
import tkinter.font as tkfont
import tkinter.ttk as ttk


def functionCenter(window, parent=None, dialog=False):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()

    x = int(window.winfo_screenwidth() / 2) - int(width / 2)
    y = int(window.winfo_screenheight() / 2) - int(height / 2)

    if dialog:
        fx = int(parent.winfo_width() / 2) - int(width / 2)
        fy = int(parent.winfo_height() / 4)
        x += fx
        y += fy

    window.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    window.deiconify()


def functionDialog(title, window, geometry, center=True):
    dialog = tk.Toplevel(window)
    dialog.transient(window)
    dialog.grab_set()
    dialog.title(title)
    dialog.resizable(False, False)
    functionCenter(dialog, window, center)
    dialog.focus()
    dialog.geometry(geometry)
    return dialog


def functionSplit(string, mx=10):
    if len(string) > mx:
        l = list(string)
        l[mx-2] = ";"
        new = "".join(l)
        return new.split(";")[0] + "..."
    else:
        return string


def functionFontTk(length, weight="normal", family="Arial"):
    return tkfont.Font(family=family, size=length, weight=weight, overstrike=0, slant="roman")


def functionFontTtk(length, family="Arial"):
    s = ttk.Style()
    s.configure("my.TButton", font=(family, length))
    return "my.TButton"
