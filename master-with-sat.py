import csv

# IPEDS 2012
ipeds_colleges = set()
ipeds_dict = dict()

with open('ipeds-2012.csv', 'rU') as csvfile:
  reader = csv.reader(csvfile)
  next(reader, None)
  for row in reader:
    ipeds_colleges.add(int(row[0]))
    ipeds_dict[int(row[0])] = row[5:]

outfile = open('master-with-sat.csv', 'w')
writer = csv.writer(outfile)

empty_row = [''] * 12

# vs master-matching
with open('master-matching.csv', 'rU') as csvfile:
  reader = csv.reader(csvfile)
  row = next(reader)
  writer.writerow( row + ['Percent Submitting SAT', 'Percent Submitting ACT', 'SAT CR 25th', 'SAT CR 75th', 'SAT M 25th', 'SAT M 75th', 'SAT W 25th', 'SAT W 75th', 'ACT Composite 25th', 'ACT Composite 75th', 'Graduation Rate', 'Retention Rate'])
  for row in reader:
    new_row = row
    if (row[0] != '') and (int(row[0]) in ipeds_colleges):
      new_row = new_row + ipeds_dict[int(row[0])]
    else:
      new_row = new_row + empty_row
    writer.writerow(new_row)