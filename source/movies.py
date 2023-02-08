from bs4 import BeautifulSoup
from thread_download import Multidownload
import os
import time
import shutil
from datetime import date
import gzip
import pandas as pd
from math import ceil
from httpx import get, stream
import config
from googletrans import Translator


class Checkmovies():
    URL_DATABASE = "https://datasets.imdbws.com/"
    DOWNLOAD_DATABASE = "./download"
    EXTRACT_DATABASE = "./extract"
    D_COLUMNS = {
        "title_basics": ('tconst', 'titleType', 'originalTitle', 'startYear', 'runtimeMinutes', 'genres'),
        "title_crew": ('tconst', 'directors'),
        "title_principals": ('tconst', 'nconst', 'job'),
        "name_basics": ('nconst', 'primaryName', 'knownForTitles'),
        "title_ratings": ('tconst', 'averageRating', 'numVotes'),
        # "genres": ('genres', 'generos')
    }
    API_URL = 'https://api.themoviedb.org/3/movie/'
    POSTER_URL = "https://image.tmdb.org/t/p/w500"
    translator = Translator(service_urls=['translate.googleapis.com'])

    def __init__(self):
        self.atualizar = True
        self.extract = True
        self.open_connection()
        ...

    def check_atualizacao(self):
        if not os.path.exists(self.DOWNLOAD_DATABASE):
            return True

        today = date.today()
        files = [os.path.join(self.DOWNLOAD_DATABASE, f) for f in os.listdir(self.DOWNLOAD_DATABASE) if
                 os.path.isfile(os.path.join(self.DOWNLOAD_DATABASE, f))]
        if not files:
            shutil.rmtree(self.DOWNLOAD_DATABASE)
            self.atualizar = True
            return True

        for path in files:
            ti_m = os.path.getmtime(path)
            m_ti = time.ctime(ti_m)
            t_obj = time.strptime(m_ti)
            T_stamp = time.strftime("%Y-%m-%d", t_obj)
            if date.fromisoformat(T_stamp) != today:
                shutil.rmtree(self.DOWNLOAD_DATABASE)
                self.atualizar = True
                return True

        self.atualizar = False
        return False

    def donwload_file(self):
        # self.check_atualizacao()
        if not self.atualizar:
            self.extract = False
            return True
        os.makedirs(self.DOWNLOAD_DATABASE, exist_ok=True)
        lst_donwload = []
        # if not os.path.exists(self.DOWNLOAD_DATABASE):
        #     os.mkdir(self.DOWNLOAD_DATABASE)
        html_text = get(self.URL_DATABASE).text
        soup = BeautifulSoup(html_text, 'html.parser')
        for link in soup.find_all('a'):
            link = link.get('href')
            if 'gz' in link:
                lst_donwload.append(Multidownload(
                    link, self.DOWNLOAD_DATABASE))

        for th in lst_donwload:
            th.start()

        for th in lst_donwload:
            th.join()

        self.extract = True
        return True

    def exctract_files(self):
        try:
            os.makedirs(self.EXTRACT_DATABASE, exist_ok=True)
            onlyfiles = [os.path.join(self.DOWNLOAD_DATABASE, f) for f in os.listdir(self.DOWNLOAD_DATABASE) if
                         os.path.isfile(os.path.join(self.DOWNLOAD_DATABASE, f))]

            for path in onlyfiles:

                file = path.split('\\')[1]
                file = file[: file.find('.gz')]
                # my_tar = tarfile.open(file)
                # my_tar.extractall(self.EXTRACT_DATABASE)
                with gzip.open(path, 'rb') as f:
                    file_content = f.read()
                    extract_file = os.path.join(self.EXTRACT_DATABASE, file)
                    with open(extract_file, 'wb') as w:
                        w.write(file_content)

            return True
        except:
            return False

    def open_connection(self):
        import mysql.connector
        import config
        self.conn = mysql.connector.connect(
            host=config.d_keys['host'],
            user=config.d_keys['user'],
            password=config.d_keys['password'],
            database=config.d_keys['database'])

        self.cursor = self.conn.cursor()

    def close_connection(self):
        self.cursor.close()
        self.conn.close()

    def id_movies(self):
        sql = """
        select tconst from title_basics
        """
        self.cursor.execute(sql)
        lst = self.cursor.fetchall()
        self.df_movies = pd.DataFrame(lst, columns=['tconst'])

    def id_person(self):
        sql = """
        select DISTINCT nconst from title_principals
        """
        self.cursor.execute(sql)
        lst = self.cursor.fetchall()
        self.df_person = pd.DataFrame(lst, columns=['nconst'])

    # def genres(self):
    #     sql = """
    #     select distinct genres from title_basics
    #     WHERE genres <> "\\N"
    #     """
    #     self.cursor.execute(sql)
    #     lst = self.cursor.fetchall()
    #     df_movies = pd.DataFrame(lst, columns=['genres'])
    #     df_movies = df_movies[df_movies.genres != "\\N"]
    #     lst = [b  for a in df_movies.genres.tolist() for b in a.split(',')]
    #     df = pd.DataFrame(data = {"genres":list(set(lst))})
    #     df['genero'] = df.genres.apply(lambda x: self.translator.translate(x, dest = 'pt').text)
    #     lst = ['Thriller', 'Short', 'Film-Noir', 'Western']
    #     df.loc[df.genres.isin(lst), 'genero'] = df.loc[df.genres.isin(lst), 'genres']
    #     self.df_genrer = df

    def create_database(self):
        try:
            for key, value in self.D_COLUMNS.items():
                # if key =='genres':
                #     df = self.df_genrer
                # else:
                df = pd.read_csv(os.path.join(self.EXTRACT_DATABASE, key.replace('_', '.') + '.tsv'),
                                 sep='\t',
                                 usecols=value)

                if key == "title_basics":
                    df = df[df.titleType == 'movie']
                    df = df.fillna("").drop(columns="titleType")

                    df.originalTitle = df.originalTitle.apply(
                        lambda x: str(x)[:255])

                elif key == "title_crew":
                    df = df[df.tconst.isin(self.df_movies.tconst)]
                    df.directors = df.directors.apply(lambda x: str(x)[:255])

                elif key == 'title_principals':
                    df = df[df.tconst.isin(self.df_movies.tconst)]

                elif key == "name_basics":
                    df = df[df.nconst.isin(self.df_person.nconst)]
                    # df['knownForTitles'] = df.knownForTitles.apply(lambda x: str(x).replace("\\N","").split(','))

                elif key == "title_ratings":
                    df = df[df.tconst.isin(self.df_movies.tconst)]
                    df.averageRating = df.averageRating.astype('float64')
                    df.numVotes = df.numVotes.astype('int64')

                tuples = [str(tuple(x)) for x in df.to_numpy()]
                self.commit(tuples, key, value)
                del df, tuples
            return True

        except Exception as e:
            print(e)
            return False

    def commit(self, tuples, key, value):
        print(key)
        for val in range(0, len(tuples) + 1000, ceil(len(tuples)/100)):
            if val == 0:
                ini = val
            else:
                sql = f"""INSERT INTO {key} {str(value).replace("'","").replace("titleType,","")}
                    VALUES {', '.join(tuples[ini:val])}"""
                self.cursor.execute(sql)
                self.conn.commit()
                ini = val
                print(f'Linhas subidas: {val}')

        if key == "title_basics":
            self.id_movies()
        elif key == "title_principals":
            self.id_person()

    def delete_data(self):
        try:
            self.id_movies()
            self.id_person()
            for key in self.D_COLUMNS.keys():
                if key != "name_basics":
                    sql = f"""
                        DELETE FROM {key}
                        WHERE tconst in {str(tuple(self.df_movies.tconst.to_list()))}
                    """
                else:
                    sql = f"""
                        DELETE FROM {key}
                        WHERE nconst in {str(tuple(self.df_person.nconst.to_list()))}
                    """
                # print(sql)
                self.cursor.execute(sql)
                self.conn.commit()

            return True

        except Exception as e:
            print(e)
            return False

    def run_update(self):
        try:
            print("REMOVENDO DIRETORIOS")
            shutil.rmtree(self.EXTRACT_DATABASE)
            shutil.rmtree(self.DOWNLOAD_DATABASE)
        except:
            pass

        print("INICIANDO DOWNLOADS")
        check_download = self.donwload_file()
        if check_download:
            print("INICIANDO EXTRAÇÃO")
            check_extract = self.exctract_files()
            if check_extract:
                print("APAGANDO OS DADOS EXISTENTES")
                check_delete = self.delete_data()
                del self.df_movies, self.df_person
                if check_delete:
                    print("FAZENDO O NOVO UPLOAD")
                    check_upload = self.create_database()
                    if check_upload:
                        return True

        return False

    def request_file(self, code):

        # code = "tt0816692"
        params = {
            "api_key": config.api_key,
        }
        self.code = code
        req = get(self.API_URL+code, params=params)
        if req.status_code == 200:
            json_file = req.json()
            # breakpoint()
            poster_path = json_file['poster_path']
            self.image_path = os.path.join(config.cache_path, self.code + '.png')
            self.name = json_file["original_title"]
            if os.path.isfile(self.image_path):
                sql = f"""
                select DISTINCT overview from overview
                WHERE tconst = '{self.code}'
                """
                self.cursor.execute(sql)
                self.overview = self.cursor.fetchall()[0][0]

            else:
                if poster_path == None:                    
                    shutil.copyfile(os.path.join(config.cache_path, 'not_found.png'), self.image_path)

                else:
                    with open(self.image_path, 'wb') as w:
                        with stream("GET", self.POSTER_URL+poster_path) as download_image:
                            for chunck in download_image.iter_bytes():
                                w.write(chunck)

                self.overview = self.translator.translate(
                    json_file["overview"], dest='pt').text
                

                sql = f"""INSERT INTO overview (tconst, overview)
                        VALUES ('{self.code}', '''{self.overview}''')"""
                # breakpoint()
                self.cursor.execute(sql)
                self.conn.commit()

            return True
        else:
            return False

if __name__ == '__main__':

    app = Checkmovies()
    # val = app.run_update()
    print(app.request_file("tt0871860"))
    # print(app.overview)
