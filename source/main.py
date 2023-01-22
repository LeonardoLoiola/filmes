import requests
from bs4 import BeautifulSoup
from thread_download import Multidownload
import os
import tarfile
import time

class Checkmovies():
    URL_DATABASE = "https://datasets.imdbws.com/"
    DOWNLOAD_DATABASE = "./download"

    def __init__(self):
        
        ...

    def donwload_html(self):
        os.makedirs(self.DOWNLOAD_DATABASE, exist_ok= True)
        lst_donwload = []
        # if not os.path.exists(self.DOWNLOAD_DATABASE):
        #     os.mkdir(self.DOWNLOAD_DATABASE)
        html_text = requests.get(self.URL_DATABASE).text
        soup = BeautifulSoup(html_text, 'html.parser')
        for link in soup.find_all('a'):
            link = link.get('href')
            if 'gz' in link:
                lst_donwload.append(Multidownload(link, self.DOWNLOAD_DATABASE))
                
        for th in lst_donwload:
            th.start()

        for th in lst_donwload:
            th.join()
        print("aqui")
