from tkinter import *
import mysql.connector
import config
import pandas as pd
from movies import Checkmovies

movie = Checkmovies()
sql = """
        select distinct generos from genres
"""
movie.cursor.execute(sql)
lst = movie.cursor.fetchall()
lst = [a[0] for a in lst]
lst.sort()

class Tela():
    root = Tk()
    def __init__(self, lst) -> None:
        self.lst = lst

    def create_genrer_lst(self, label_x, label_y):
        label = Label(self.root, text="Genero"
                        # ,width=10
                        ,font=("bold", 15))
        # label.place(x=label_x,y=label_y)
        label.grid(column=label_y, row=label_x, sticky=NS, padx=5, pady=5)
        variable = StringVar(self.root)
        variable.set("") 

        w = OptionMenu(self.root, variable, *self.lst)
        # w.pack()
        w.configure(width=30)
        # w.place(x = label_x+20, y= label_y + 30)
        w.grid(column=label_y, row=label_x+1, sticky=NS, padx=5, pady=5)
        return variable

    def create_entry(self, text, label_x, label_y):
        label = Label(self.root, text=text
                        # ,width=10
                        ,font=("bold", 15))
        label.grid(column=label_y, row=label_x, sticky=NS, padx=5, pady=5)

        entry = Entry(self.root, width=40)
        entry.grid(column=label_y, row=label_x+1, sticky=NS, padx=5, pady=5)
        return entry


    def get_value(self):
        print("Genero 1: ", self.gen1.get())
        print("Genero 2: ", self.gen2.get())

    def tela_inicial(self):
        self.root.geometry('500x500')
        self.root.title('Movie Selector')
        self.root.resizable(0,0)
        self.root.columnconfigure(0, weight=2)
        self.root.columnconfigure(1, weight=2)
        self.root.rowconfigure(2, minsize=30)
        self.root.rowconfigure(5, minsize=30)
        self.root.rowconfigure(8, minsize=30)
        self.root.rowconfigure(11, minsize=50)



        self.gen1 = self.create_genrer_lst(0, 0)

        self.gen2 = self.create_genrer_lst( 0, 1)

        self.diretor = self.create_entry('Diretor', 3, 0)

        self.ator = self.create_entry('Ator', 3, 1)

        self.ano_inicial = self.create_entry('Ano Inicial', 6, 0)

        self.ano_final = self.create_entry('Ano Final', 6, 1)

        self.rating = self.create_entry('Rating IMDB', 9, 0)

        self.votos = self.create_entry('Votos IMBD', 9, 1)

        self.atualizar = Button(text = "Atualizar BD", width=40)
        self.atualizar.grid(row= 12, column= 0,sticky=NS, padx=5, pady=5)

        self.pesquisar = Button( text = "Pesquisar Filme", width=40, command=self.get_value)
        self.pesquisar.grid(row= 12, column= 1,sticky=NS, padx=5, pady=5)

tela = Tela(lst)
tela.tela_inicial()
tela.root.mainloop()



