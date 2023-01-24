
import mysql.connector
import pandas as pd
from math import ceil
import pandas as pd
import time
import config as config

url = r"E:\User\Leonardo\GIT\filme\extract\title.principals.tsv"

def commit(ini, final, cursor, conn, tuples):
    sql = f"""INSERT INTO title_basics (tconst,titleType,originalTitle,startYear,runtimeMinutes,genres)
                VALUES {', '.join(tuples[ini:final])}"""


ini = time.time()
print(config.d_keys)
