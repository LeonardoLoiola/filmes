import requests
from bs4 import BeautifulSoup
import wget
import os
import gzip
import shutil

class Checkmovies():
    URL_DATABASE = "https://datasets.imdbws.com/"
    DOWNLOAD_DATABASE = "./download"
    EXTRACT_DATABASE = "./extract"

    def __init__(self):
        self.extract = True
        ...

    def exctract_files(self):
        if self.extract:
            shutil.rmtree(self.EXTRACT_DATABASE)
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

