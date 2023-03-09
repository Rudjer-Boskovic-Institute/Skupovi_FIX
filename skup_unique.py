import pandas as pd
import numpy as np
import re

pd.set_option('display.max_rows', none)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth', 1000)
pd.options.mode.use_inf_as_na = True

# Import Skup list
df = pd.read_csv("DATA/crosbi_skup_cisto_step1..txt", sep="\t", dtype='unicode')

#df[['count']] = df.groupby(['mjesto', "drzava", 'dd', 'mm', 'gggg', 'dd1', "mm1", "gggg1"], as_index=False).transform(len)

#df1 = df.groupby(['TIT','mjesto', "drzava", 'dd', 'mm', 'gggg', 'dd1', "mm1", "gggg1"], as_index=False).size()

df.insert(2, "COUNT", df.groupby(['TIT','mjesto', "drzava", 'dd', 'mm', 'gggg', 'dd1', "mm1", "gggg1"], as_index=False).size(), True)

#print (df[["ID", "DAT", "DAT_Resolve", "LOC", "LOC_Resolve_Country", "LOC_Resolve_Ostalo"]])


df1.to_csv("/tmp/bla.csv", sep="|", quotechar="~")
