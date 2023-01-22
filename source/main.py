import requests
from bs4 import BeautifulSoup
from thread_download import Multidownload
import os
import tarfile
import time
import shutil
from datetime import date


class Checkmovies():
    URL_DATABASE = "https://datasets.imdbws.com/"
    DOWNLOAD_DATABASE = "./download"

    def __init__(self):
        self.atualizar = True
        self.extract = True
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
            if date.fromisoformat(T_stamp) != today :
                shutil.rmtree(self.DOWNLOAD_DATABASE)
                self.atualizar = True
                return True

        self.atualizar = False
        return False

    def donwload_file(self):
        self.check_atualizacao()
        if not self.atualizar:
            self.extract = False
            return True
        os.makedirs(self.DOWNLOAD_DATABASE, exist_ok=True)
        lst_donwload = []
        # if not os.path.exists(self.DOWNLOAD_DATABASE):
        #     os.mkdir(self.DOWNLOAD_DATABASE)
        html_text = requests.get(self.URL_DATABASE).text
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


# path = r"E:\User\Leonardo\GIT\filme\download\name.basics.tsv.gz"
# ti_m = os.path.getmtime(path)
# m_ti = time.ctime(ti_m)
# t_obj = time.strptime(m_ti)
# T_stamp = time.strftime("%Y-%m-%d", t_obj)
# print(T_stamp)
a = Checkmovies()
print(a.donwload_file())