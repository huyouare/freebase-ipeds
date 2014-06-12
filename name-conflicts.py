import csv

from fuzzywuzzy import fuzz

outfile = open('union-freebase-with-name-conflicts.csv', 'w')
writer = csv.writer(outfile)

with open('union-freebase.csv', 'rU') as f:
  reader = csv.reader(f)
  first_row = next(reader)
  new_first_row = ['fuzzy matching score'] + first_row
  writer.writerow(new_first_row)
  
  for row in reader:
    ratios = set()
    if row[1]!='' and row[3]!='':
      ratios.add(fuzz.token_sort_ratio(row[1], row[3]))
    if row[3]!='' and row[5]!='': 
      ratios.add(fuzz.token_sort_ratio(row[3], row[5]))
    if row[1]!='' and row[5]!='': 
      ratios.add(fuzz.token_sort_ratio(row[1], row[5]))
    if len(ratios) > 0:
      summ = 0
      for x in ratios:
        summ = summ + x
      ratio = summ / len(ratios)
    else:
      ratio = 0
    writer.writerow([ratio] + row)
