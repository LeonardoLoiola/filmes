from tkinter import *
import pandas as pd
from movies import Checkmovies
from PIL import ImageTk, Image
import random as rd

movie = Checkmovies()
sql = """
        select distinct generos from genres
"""
movie.cursor.execute(sql)
lst = movie.cursor.fetchall()
lst = [a[0] for a in lst]
lst.sort()


class Tela(Checkmovies):
    D_GENEROS = {
        'mistério':  'mystery',
        'aventura':  'adventure',
        'musical':  'musical',
        'drama':  'drama',
        'romance':  'romance',
        'esporte':  'sport',
        'horror':  'horror',
        'guerra':  'war',
        'história':  'history',
        'western':  'western',
        'programa de entrevista':  'talk-show',
        'game-show':  'game-show',
        'ação':  'action',
        'adulto':  'adult',
        'film-noir':  'film-noir',
        'ficção científica':  'sci-fi',
        'short':  'short',
        'crime':  'crime',
        'fantasia':  'fantasy',
        'thriller':  'thriller',
        'experimental':  'experimental',
        'comédia':  'comedy',
        'música':  'music',
        'documentário':  'documentary',
        'biografia':  'biography',
        'família':  'family',
        'animação':  'animation',
        'reality-tv':  'reality-tv',
        'notícias':  'news',

    }

    def __init__(self) -> None:
        super().__init__()
        self.create_genrer_lst()
        self.color = "#cbd3d5"
        self.create_application()
        self.lst_not_use = []

    def create_application(self):
        self.root = Tk()
        self.root.geometry('510x500')
        self.root.configure(background=self.color)

    def create_genrer_lst(self):
        sql = """
        select distinct generos from genres
        """
        self.cursor.execute(sql)
        self.lst_genrer = self.cursor.fetchall()
        self.lst_genrer = [a[0] for a in self.lst_genrer]
        self.lst_genrer.sort()

    def create_genrer_suspense_lst(self, label_x, label_y):
        if label_y == 0:
            label = Label(self.frame_row1, text="Genero"                      # ,width=10
                          , font=("bold", 15), bg=self.color)
            variable = StringVar(self.frame_row1)

        else:
            label = Label(self.frame_row2, text="Genero"                      # ,width=10
                          , font=("bold", 15), bg=self.color)
            variable = StringVar(self.frame_row2)

        label.grid(column=label_y, row=label_x, sticky=NS, padx=5, pady=5)
        variable.set("")
        if label_y == 0:
            w = OptionMenu(self.frame_row1, variable, *self.lst_genrer)
        else:
            w = OptionMenu(self.frame_row2, variable, *self.lst_genrer)
        w.configure(width=30)
        w.grid(column=label_y, row=label_x+1, sticky=NS, padx=5, pady=5)
        return variable

    def create_entry(self, text, label_x, label_y):
        if label_y == 0:
            label = Label(self.frame_row1, text=text                      # ,width=10
                          , font=("bold", 15), bg=self.color)
            entry = Entry(self.frame_row1, width=40)

        else:
            label = Label(self.frame_row2, text=text                      # ,width=10
                          , font=("bold", 15), bg=self.color)
            entry = Entry(self.frame_row2, width=40)

        label.grid(column=label_y, row=label_x, sticky=NS, padx=5, pady=5)
        entry.grid(column=label_y, row=label_x+1, sticky=NS, padx=5, pady=5)
        return entry

    def get_value(self):
        self.genero_1_valor = self.genero_1_selector.get().lower()
        self.genero_2_valor = self.genero_2_selector.get().lower()
        self.diretor_valor = self.diretor_selector.get().lower()
        self.ator_valor = self.ator_selector.get().lower()
        self.ano_inicial_valor = self.ano_inicial_selector.get()
        self.ano_final_valor = self.ano_final_selector.get()
        self.rating_valor = self.rating_selector.get()
        self.votos_valor = self.votos_selector.get()

        print("Genero 1: ", self.genero_1_valor)
        print("Genero 2: ", self.genero_2_valor)
        self.where_clause()
        self.select_movie()
        print('proxima pagina')

        self.frame_row1.destroy()
        self.frame_row2.destroy()
        self.atualizar.destroy()
        self.pesquisar.destroy()
        # self.create_application()
        self.tela_pesquisa()
        # self.root.mainloop()

    def where_clause(self):
        self.where = []
        if self.genero_1_valor != "":
            self.genero_1_valor = self.D_GENEROS[self.genero_1_valor]
            self.where.append(f"""
            lower(genres) LIKE '%{self.genero_1_valor}%'
            """)

        if self.genero_2_valor != "":
            self.genero_2_valor = self.D_GENEROS[self.genero_2_valor]
            self.where.append(f"""
            lower(genres) LIKE '%{self.genero_2_valor}%'
            """)

        if self.ano_inicial_valor != "":
            self.where.append(f"""
            startYear >= {int(self.ano_inicial_valor)}
            """)

        if self.ano_final_valor != "":
            self.where.append(f"""
            startYear <= {int(self.ano_final_valor)}
            """)

        self.where = " AND ".join(self.where)
        if len(self.where) > 0:
            self.where = "WHERE " + self.where

        sql = f"""
        SELECT tconst,
		originalTitle
        FROM filmes.title_basics
        {self.where}
        """
        # print(sql)
        self.cursor.execute(sql)
        lst_title_basics = self.cursor.fetchall()
        df_title_basics = pd.DataFrame(lst_title_basics, columns=[
                                       'tconst', 'originalTitle'])

        self.where = []

        if self.diretor_valor != "":
            sql = f"""
                SELECT distinct tconst FROM filmes.title_principals A
                INNER JOIN (SELECT nconst
                FROM filmes.name_basics
                where lower(primaryName) like '%{self.diretor_valor}%'
                LIMIT 1) B
                ON A.nconst = B.nconst
            """
            # print(sql)
            self.cursor.execute(sql)
            lst_director = self.cursor.fetchall()
            df_director = pd.DataFrame(lst_director, columns=['tconst'])
            df_title_basics = df_title_basics.merge(
                df_director, how='right', on="tconst")

        # else:
        #     df_director = pd.DataFrame(columns=['nconst', 'primaryName'])

        if self.ator_valor != '':
            sql = f"""

                SELECT distinct tconst FROM filmes.title_principals A
                INNER JOIN (SELECT nconst
                FROM filmes.name_basics
                where lower(primaryName) like '%{self.ator_valor}%'
                LIMIT 1) B
                ON A.nconst = B.nconst
            """
            self.cursor.execute(sql)
            lst_ator = self.cursor.fetchall()
            df_ator = pd.DataFrame(lst_ator, columns=['tconst'])
            df_title_basics = df_title_basics.merge(
                df_ator, how='right', on="tconst")

        if self.rating_valor != "":
            self.where.append(f"""
            averageRating >= {float(self.rating_valor.replace(',','.'))}
            """)

        else:
            self.where.append(f"""
            averageRating >= 0
            """)

        if self.votos_valor != "":
            self.where.append(f"""
            numVotes >= {int(self.rating_valor)}
            """)

        else:
            self.where.append(f"""
            numVotes >= 0
            """)
        self.where = " AND ".join(self.where)

        sql = f"""
            SELECT tconst, averageRating, numVotes 
            FROM filmes.title_ratings
            WHERE tconst in {tuple(df_title_basics.tconst.to_list())}
            AND {self.where}
        """
        self.cursor.execute(sql)
        lst_rating = self.cursor.fetchall()
        df_rating = pd.DataFrame(lst_rating, columns=[
                                 'tconst', 'averageRating', 'numVotes'])
        self.df_title_basics = df_title_basics.merge(
            df_rating, how='right', on="tconst")

    def select_movie(self):
        print('aqui')
        # breakpoint()
        while True:
            self.df_title_basics = self.df_title_basics[~self.df_title_basics.tconst.isin(
                self.lst_not_use)]
            self.df_title_basics = self.df_title_basics.sort_values(
                by=['numVotes', 'averageRating'], ascending=False).reset_index(drop=True)
            self.df_title_basics = self.df_title_basics[self.df_title_basics.index <= 15]
            index_movie = rd.randint(0, self.df_title_basics.index.max())
            id_movie = self.df_title_basics[self.df_title_basics.index ==
                                            index_movie].tconst.values[0]
            self.lst_not_use.append(id_movie)
            print(id_movie)
            self.parar = self.request_file(id_movie)
            # breakpoint()
            if self.parar:
                break

    def tela_inicial(self):

        self.root.title('Movie Selector')
        self.root.resizable(0, 0)
        # self.root.columnconfigure(0, weight=2)
        # self.root.columnconfigure(1, weight=2)
        self.root.rowconfigure(2, minsize=30)
        self.root.rowconfigure(5, minsize=30)
        self.root.rowconfigure(8, minsize=30)
        self.root.rowconfigure(11, minsize=50)

        self.frame_row1 = Frame(self.root, width=250,
                                height=250, bg=self.color)
        self.frame_row1.grid(column=0, row=0)
        self.frame_row2 = Frame(self.root, width=250,
                                height=250, bg=self.color)
        self.frame_row2.grid(column=1, row=0)
        self.genero_1_selector = self.create_genrer_suspense_lst(0, 0)
        self.genero_2_selector = self.create_genrer_suspense_lst(0, 1)
        self.diretor_selector = self.create_entry('Diretor', 3, 0)
        self.ator_selector = self.create_entry('Ator', 3, 1)
        self.ano_inicial_selector = self.create_entry('Ano Inicial', 6, 0)
        self.ano_final_selector = self.create_entry('Ano Final', 6, 1)
        self.rating_selector = self.create_entry('Rating IMDB', 9, 0)
        self.votos_selector = self.create_entry('Votos IMBD', 9, 1)
        self.atualizar = Button(text="Atualizar BD",
                                width=20, command=self.run_update)
        self.atualizar.grid(row=12, column=0, sticky=NS, padx=5, pady=5)
        self.pesquisar = Button(text="Pesquisar Filme",
                                width=20, command=self.get_value)
        self.pesquisar.grid(row=12, column=1, sticky=NS, padx=5, pady=5)

    def return_init(self):
        self.frame_direito.destroy()
        self.frame_esquerdo.destroy()
        self.tela_inicial()

    def new_search(self):
        self.frame_direito.destroy()
        self.frame_esquerdo.destroy()
        self.select_movie()
        self.tela_pesquisa()

    def tela_pesquisa(self):
        # self.root.geometry('600x600')
        self.root.title('Movie Search')
        self.root.resizable(0, 0)
        self.root.columnconfigure(0, weight=3)
        self.root.columnconfigure(1, weight=2)

        self.frame_esquerdo = Frame(
            self.root, width=300, height=500, bg=self.color)
        self.frame_esquerdo.grid(row=0, column=0, sticky=NS, padx=5, pady=5)

        self.frame_direito = Frame(
            self.root, width=300, height=500, bg=self.color)
        self.frame_direito.grid(row=0, column=1, sticky=NS, padx=5, pady=5)
        self.frame_direito.rowconfigure(2, minsize=75)
        self.frame_direito.rowconfigure(4, minsize=23)
        self.frame_direito.rowconfigure(1, weight=3)

        im = Image.open(r"cache\{}.png".format(self.code))
        im_resize = im.resize((300, 440), Image.LANCZOS)
        self.im_tk = ImageTk.PhotoImage(im_resize)
        label = Label(self.frame_esquerdo, image=self.im_tk,
                      height=400, width=300, background=self.color)
        label.grid(row=0, column=0, sticky=NS, padx=5, pady=5)

        label_titulo = Label(
            self.frame_direito, text=self.name, bg=self.color, font=('bond', 15))
        # wraplengt=200
        label_titulo.grid(row=0, column=0, sticky=NS, padx=5, pady=5)
        label_overview = Label(self.frame_direito, text="Sinopse: \n" + self.overview,
                               wraplengt=170, bg=self.color, font=("Arial", 9))
        label_overview.grid(row=1, column=0, sticky=NS,
                            padx=5, pady=5, rowspan=2)

        button_nova_escolha = Button(
            self.frame_direito, text="Nova escolha de filme", width=30, command=self.new_search)
        button_nova_escolha.grid(row=3, column=0)
        button_voltar = Button(
            self.frame_direito, text="Tela inicial", width=30, command=self.return_init)
        button_voltar.grid(row=5, column=0)


if __name__ == '__main__':
    tela = Tela()

    tela.tela_inicial()
    tela.root.mainloop()
