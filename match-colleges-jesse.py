import csv
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

# Freebase
freebase_names = set()
freebase_dict = dict()

with open('freebase-colleges-iped.csv', 'r') as csvfile:
  reader = csv.reader(csvfile)
  next(reader, None) # Ignore headers
  for row in reader:
    freebase_names.add(row[2].decode('utf-8'))
    freebase_dict[row[2].decode('utf-8')] = row[0]

count = 0
names_list = list(freebase_names)
choices = names_list

with open('./college_data/colleges_for_jesse.tsv', 'rb') as f:
  reader = csv.reader(f, delimiter='\t')
  next(reader)
  for row in reader:
    if row[1] in freebase_names:
      print "IN: " + row[1]
      count = count + 1
    else:
      print "OUT: " + row[1].decode('utf-8')
      estimate = process.extract(row[1], choices)
      print "Estimate: " + str(estimate)
  print count