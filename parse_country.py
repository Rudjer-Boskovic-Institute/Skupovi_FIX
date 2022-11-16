import pandas as pd
import numpy as np
import re

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth', 100)
pd.options.mode.use_inf_as_na = True

def findCountry(loc, co):
  for countryVar in co:
    countryRegex = re.compile(countryVar, re.IGNORECASE)
    if countryRegex.search(str(loc), re.IGNORECASE):
      LOC_Resolve_Country = co[0]
      LOC_Resolve_Ostalo = loc.replace(countryVar, '')
      LOC_Resolve_Ostalo = re.sub('^[^a-zA-Z]*|[^a-zA-Z]*$','', LOC_Resolve_Ostalo)
      break
    else:
      LOC_Resolve_Country = "NEMA"
      pass
  if LOC_Resolve_Country == "NEMA":
    return False
  else:
    return LOC_Resolve_Country, LOC_Resolve_Ostalo

def findDate(data):
  dateRegex = re.compile(
    r'^'
    r'[\s.-]*'
    r'(\d+)'
    r'[\s.-]+'
    r'(\d+)'
    r'[\s.-]+'
    r'(\d+)'
    r'[\s.-]+'
    r'(\d+)'
    r'[\s.,]*'
    r'$'
    )
  dateFromTo_day = dateRegex.match(data)
  if dateFromTo_day:
    dateFixed = (''
      + 'OD '
      + dateFromTo_day.group(1).rjust(2, '0') + '.' + dateFromTo_day.group(3).rjust(2, '0') + '.'+ dateFromTo_day.group(4) + '.'
      + ' DO '
      + dateFromTo_day.group(2).rjust(2, '0') + '.' + dateFromTo_day.group(3).rjust(2, '0') + '.'+ dateFromTo_day.group(4) + '.'
      )
  else:
    dateFixed = "??.??.????."
  return dateFixed
  
def fixAll(data, co):
  LOC_Resolve_Country = ''
  LOC_Resolve_Ostalo = ""
  for idx, row in co.iterrows():
    country = row['COUNTRY'].split(',')
    findResult = findCountry(data["LOC"], country)
    if findResult == False:
      pass
    else:
      LOC_Resolve_Country = findResult[0]
      LOC_Resolve_Ostalo = findResult[1]
      break
  if str(data["DAT"]) !='nan':
    date = findDate(data["DAT"])
  else:
    date = "NONE"
  DAT_Resolve = date
  ret = pd.Series([DAT_Resolve, LOC_Resolve_Country, LOC_Resolve_Ostalo])
  #print (ret)
  return ret



# Import Skup list
df = pd.read_csv("DATA/skup.csv", nrows=1000, quotechar='~', sep=",")

# Import Country list
co = pd.read_csv("DATA/countries.txt", nrows=10000, quotechar='"', sep="~")


df[["DAT_Resolve", "LOC_Resolve_Country","LOC_Resolve_Ostalo"]] = df.apply(lambda x: fixAll(x, co), axis=1)

print (df[["ID", "DAT", "DAT_Resolve", "LOC", "LOC_Resolve_Country", "LOC_Resolve_Ostalo"]])
