
from threading import Thread
import wget
import time

ini = time.time()
class Multidownload(Thread):
    def __init__(self, link, DOWNLOAD_DATABASE):
        Thread.__init__(self)
        self.link = link
        self.DOWNLOAD_DATABASE = DOWNLOAD_DATABASE
        ...

    def run(self):

        wget.download(self.link, out= self.DOWNLOAD_DATABASE)
        ...

# link = 'https://datasets.imdbws.com/name.basics.tsv.gz'
# DOWNLOAD_DATABASE = "./download"
# a = Multidownload(link, DOWNLOAD_DATABASE)
# a.start()
# a.join()
# fim = time.time()
# print(fim - ini)