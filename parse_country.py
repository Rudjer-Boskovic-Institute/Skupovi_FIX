import pandas as pd
import numpy as np
import re
import ast
import logging as log

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth', 100)
pd.options.mode.use_inf_as_na = True

log.basicConfig(filename="debug.log")

def findCountry(loc, co):
  for countryVar in co:
    countryRegex = re.compile(countryVar, re.IGNORECASE)
    if countryRegex.search(str(loc), re.IGNORECASE):
      LOC_Resolve_Country = co[0]
      LOC_Resolve_Ostalo = loc.replace(countryVar, '')
      LOC_Resolve_Ostalo = re.sub('^[^a-zA-ZčćžšđČĆŽŠĐ]*|[^a-zA-ZčćžšđČĆŽŠĐ]*$','', LOC_Resolve_Ostalo)
      break
    else:
      LOC_Resolve_Country = "NEMA"
      pass
  if LOC_Resolve_Country == "NEMA":
    return False
  else:
    return LOC_Resolve_Country, LOC_Resolve_Ostalo

def findCity(loc, ci):
  LOC_Resolve_City = False
  for cityVar in ci:
    
#    log.warning(cityVar + "===" + loc)
    
    cityRegex = re.compile(cityVar, re.IGNORECASE)
    if cityRegex.search(str(loc)):
      LOC_Resolve_City = ci[0]
      break
    else:
      pass
  return LOC_Resolve_City

def findDate(data):
  # 12. - 14.9.1997
  dateRegex_1 = re.compile(
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
  # 1997
  dateRegex_2 = re.compile(
    r'^'
    r'[\s.-]*'
    r'(\d+)'
    r'[\s.,]*'
    r'$'
    )
  # 2.1997.
  dateRegex_3 = re.compile(
    r'^'
    r'[\s.-]*'
    r'(\d+)'
    r'[\s.-]+'
    r'(\d+)'
    r'[\s.,]*'
    r'$'
    )
   # 30.11. - 1.12.1997
  dateRegex_4 = re.compile(
    r'^'
    r'[\s.-]*'
    r'(\d+)'
    r'[\s.-]+'
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
  # 1.2.1997.
  dateRegex_5 = re.compile(
    r'^'
    r'[\s.-]*'
    r'(\d+)'
    r'[\s.-]+'
    r'(\d+)'
    r'[\s.-]+'
    r'(\d+)'
    r'[\s.,]*'
    r'$'
    )
  date_1 = dateRegex_1.match(data)
  date_2 = dateRegex_2.match(data)
  date_3 = dateRegex_3.match(data)
  date_4 = dateRegex_4.match(data)
  date_5 = dateRegex_5.match(data)
  if date_1:
    dateFixed = (''
      + 'OD '
      + date_1.group(1).rjust(2, '0') + '.' + date_1.group(3).rjust(2, '0') + '.'+ date_1.group(4) + '.'
      + ' DO '
      + date_1.group(2).rjust(2, '0') + '.' + date_1.group(3).rjust(2, '0') + '.'+ date_1.group(4) + '.'
      )
  elif date_4:
    dateFixed = (''
      + 'OD '
      + date_4.group(1).rjust(2, '0') + '.' + date_4.group(2).rjust(2, '0') + '.'+ date_4.group(5) + '.'
      + ' DO '
      + date_4.group(3).rjust(2, '0') + '.' + date_4.group(4).rjust(2, '0') + '.'+ date_4.group(5) + '.'
      )
  elif date_5:
    dateFixed = (''
      + 'OD '
      + date_5.group(1).rjust(2, '0') + '.' + date_5.group(2).rjust(2, '0') + '.'+ date_5.group(3) + '.'
      + ' DO '
      + date_5.group(1).rjust(2, '0') + '.' + date_5.group(2).rjust(2, '0') + '.'+ date_5.group(3) + '.'
      )
  elif date_3:
    dateFixed = (''
      + 'OD '
      + date_3.group(1).rjust(2, '0') + '.' + date_3.group(2) + '.'
      + ' DO '
      + date_3.group(1).rjust(2, '0') + '.' + date_3.group(2) + '.'
      )
  elif date_2:
    dateFixed = (''
      + 'OD '
      + date_2.group(1).rjust(4, '0') + '.'
      + 'DO '
      + date_2.group(1).rjust(4, '0') + '.'
      )
  else:
    dateFixed = "??.??.????."
  return dateFixed

def fixAll(data, co, ci):
  LOC_Resolve_Country = ''
  LOC_Resolve_Ostalo = ''
  LOC_Resolve_City = ''
  DAT_Resolve = ''
  
  for idx, row in co.iterrows():
    country = row['COUNTRY'].split(',')
    findResult = findCountry(data["LOC"], country)
    if findResult == False:
      pass
    else:
      LOC_Resolve_Country = findResult[0]
      LOC_Resolve_Ostalo = findResult[1]
      break
  
  # for idx2, row2 in ci.iterrows():
  #   city = row2['combined'].split(', ')
  #   findCiResult = findCity(data["LOC"], city)
  #   if findCiResult:
  #     LOC_Resolve_City = findCiResult
  #     break
  
  if str(data["DAT"]) !='nan':
    date = findDate(data["DAT"])
  else:
    date = "NONE"
  DAT_Resolve = date
  ret = pd.Series([DAT_Resolve, LOC_Resolve_Country, LOC_Resolve_Ostalo])
  return ret


ci = pd.read_csv("DATA/cities1000.txt", nrows=1000000, sep=r"\t", engine='python')
ci['combined'] = ci.iloc[:, 1:4].apply(lambda row: str(','.join( row.values.astype(str)).split(",", 7)[:7]), axis=1).filter(ci.iloc[:,7]=="HR")

ci['combined'].to_csv("/tmp/citiesHR.csv", sep="|", quotechar="~")

# Import Skup list
df = pd.read_csv("DATA/skup.csv", nrows=1000000, quotechar='~', sep=",")

# Import Country list
co = pd.read_csv("DATA/countries.txt", nrows=1000000, quotechar='"', sep="~")

# Import City list
#ci = pd.read_csv("DATA/cities.csv", nrows=1000, quotechar='"', sep="~")

#f = open("DATA/cities.csv", "r")

df[["DAT_Resolve", "LOC_Resolve_Country", "LOC_Resolve_Ostalo"]] = df.apply(lambda x: fixAll(x, co, ci), axis=1)

df.to_csv("/tmp/bla.csv", sep="|", quotechar="~")
