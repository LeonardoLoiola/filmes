import requests
from bs4 import BeautifulSoup
import wget
import os
import tarfile

class Checkmovies():
    URL_DATABASE = "https://datasets.imdbws.com/"
    DOWNLOAD_DATABASE = "./download"

    def __init__(self):
        
        ...

    def donwload_html(self):
        os.makedirs(self.DOWNLOAD_DATABASE, exist_ok= True)
        # if not os.path.exists(self.DOWNLOAD_DATABASE):
        #     os.mkdir(self.DOWNLOAD_DATABASE)
        html_text = requests.get(self.URL_DATABASE).text
        soup = BeautifulSoup(html_text, 'html.parser')
        for link in soup.find_all('a'):
            if 'gz' in link.get('href'):
                print(link.get('href'))
                wget.download(link.get('href'), out= self.DOWNLOAD_DATABASE)
       