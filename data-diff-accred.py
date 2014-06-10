import csv

# Freebase
ipeds_colleges = set()

with open('./datasets/ipeds_data_for_production_database.csv', 'rU') as csvfile:
  reader = csv.reader(csvfile)
  next(reader, None)
  for row in reader:
    ipeds_colleges.add(row[0])

# vs accred
accred_colleges = set()
accred_rows = dict()

with open('accredidation-ipeds.csv', 'rU') as csvfile:
  reader = csv.reader(csvfile)
  for row in reader:
    accred_colleges.add(row[8])
    accred_rows[row[8]] = row

print len(ipeds_colleges)
print len(accred_colleges)

outfile = open('./diff-output/ipeds-vs-accred.txt', 'w')

diff = ipeds_colleges - accred_colleges
diff = list(diff)
diff.sort()
for x in diff:
  outfile.write( x + '\n' )

outfile = open('./diff-output/accred-vs-ipeds-with-names.txt', 'w')
writer = csv.writer(outfile)

diff = accred_colleges - ipeds_colleges
diff = list(diff)
diff.sort()
writer.writerow(['IPEDS ID', 'School Name', 'OPE ID'])
for x in diff:
  row = accred_rows[x]
  writer.writerow( [x, row[1], row[7]] )