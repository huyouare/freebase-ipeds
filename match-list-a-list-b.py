import csv
from fuzzywuzzy import fuzz

# List B
b_ipeds = set()
b_dict = dict()

# master
with open('master-with-sat-debt-and-default.csv', 'rU') as csvfile:
  reader = csv.reader(csvfile)
  master_header = next(reader)
  for row in reader:
    b_ipeds.add(int(row[0]))
    b_dict[int(row[0])] = row

outfile = open('a-vs-b.csv', 'w')
writer = csv.writer(outfile)

empty_row = [''] * 23

# vs output-final
with open('output-final.csv', 'rU') as csvfile:
  reader = csv.reader(csvfile)
  writer.writerow( ['u_id', 'IPEDS ID', 'Freebase id', 'Name', 'Median SAT', 'Graduation rate', 'Retention rate'] + master_header + ['Name Score', 'Reasonable SAT', 'Difference Graduation', 'Difference Retention'] )
  for row in reader:
    new_row = [ row[0], row[2], row[1], row[4], row[6], row[7], row[8] ]
    if (row[2] != '') and (int(row[2]) in b_ipeds):
      new_row = new_row + b_dict[int(row[2])]
    else:
      new_row = new_row + empty_row

    if row[2].isdigit():
      b_row = b_dict[int(row[2])]

      ratio = fuzz.token_sort_ratio(row[4], b_row[1])
      new_row = new_row + [ratio]

      if b_row[9].isdigit() and row[6]!='':
        total_25 = (int(b_row[9]) + int(b_row[11]))
        total_75 = (int(b_row[10]) + int(b_row[12]))
        print total_25
        print total_75
        print row[6]
        print (int(row[6]) >= total_25)
        print (int(row[6]) <= total_75)
        if (int(row[6]) >= total_25) and (int(row[6]) <= total_75):
          new_row = new_row + ['YES']
          print 'YES'
        else:
          new_row = new_row + ['NO']
          print 'NO'

      else:
        new_row = new_row + ['']

      if b_row[17].isdigit() and b_row[18].isdigit() and row[7].isdigit() and row[8].isdigit():
        new_row = new_row + [ str( abs(int(row[7]) - int(b_row[17])) ), str( abs(int(row[8]) - int(b_row[18])) ) ]
    writer.writerow(new_row)