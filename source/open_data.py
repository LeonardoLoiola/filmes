
from threading import Thread
import wget
import time
import pandas as pd
from math import ceil

ini = time.time()


class Multiopen(Thread):
    def __init__(self, url, inicio, fim):
        Thread.__init__(self)
        self.url = url
        self.inicio = inicio
        self.fim = fim

    def run(self):
        self.df = pd.read_csv(self.url, sep='\t',
                              skiprows=self.inicio, nrows=self.fim)


url = r"E:\User\Leonardo\GIT\filme\extract\title.principals.tsv"
#
row_count = sum(1 for row in open(url, encoding="UTF-8"))
# print(row_count)

lst = []
for val in range(0, row_count+1000, ceil(row_count/4)):
    if val == 0:
        anterior = val
    else:
        lst.append(Multiopen(url, anterior, val))


ini = time.time()
# df1 = pd.read_csv(url, sep='\t', usecols=[
#                   'tconst',	'originalTitle',	'startYear',	'runtimeMinutes',	'genres',	'titleType'])

df_1 = pd.read_csv(url, sep='\t')
print(df_1.head(20))
print(time.time() - ini)
