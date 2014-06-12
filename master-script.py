#Master script

#0: IPEDS ID
#1: College Navigator name or "NOT FOUND"
#2: College name from source (Accred, Freebase, IPEDS)
#3: Name of source
#4: Accred ID
#5: Freebase MID
#6: OPE ID (from College Navigator)

import csv

from fuzzywuzzy import process

outfile = open('union-freebase-with-name-conflicts.csv', 'w')
writer = csv.writer(outfile)

with open('union-freebase.csv', 'rU') as f:
  reader = csv.reader(f)
  first_row = next(reader)
  new_first_row = ['fuzzy matching score'] + first_row
  writer.writerow(new_first_row)
  
  for row in reader:
    ratios = set()