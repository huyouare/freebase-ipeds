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

with open('accredidation-ipeds.csv', 'rU') as csvfile:
  reader = csv.reader(csvfile)
  for row in reader:
    accred_colleges.add(row[8])

print len(ipeds_colleges)
print len(accred_colleges)

outfile = open('./diff-output/ipeds-vs-accred.txt', 'w')

diff = ipeds_colleges - accred_colleges
diff = list(diff)
diff.sort()
for x in diff:
  outfile.write( x + '\n' )

outfile = open('./diff-output/accred-vs-ipeds.txt', 'w')

diff = accred_colleges - ipeds_colleges
diff = list(diff)
diff.sort()
for x in diff:
  outfile.write( x + '\n' )