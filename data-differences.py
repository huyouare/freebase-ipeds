import csv

# Freebase
freebase_colleges = set()

with open('freebase-colleges-iped.csv', 'r') as csvfile:
  reader = csv.reader(csvfile)
  next(reader, None)
  for row in reader:
    freebase_colleges.add(row[0])

# vs debt
debt_colleges = set()

with open('./datasets/debt.csv', 'r') as csvfile:
  reader = csv.reader(csvfile)
  next(reader, None)
  for row in reader:
    debt_colleges.add(row[3])

print len(freebase_colleges)
print len(debt_colleges)

outfile = open('freebase-vs-debt.txt', 'w')

diff = freebase_colleges - debt_colleges
for x in diff:
  outfile.write( x + '\n' )

outfile = open('debt-vs-freebase.txt', 'w')

diff = debt_colleges - freebase_colleges
for x in diff:
  outfile.write( x + '\n' )

# vs ipeds
ipeds_colleges = set()

with open('./datasets/ipeds_data_for_production_database.csv', 'r') as csvfile:
  reader = csv.reader(csvfile)
  next(reader, None)
  for row in reader:
    ipeds_colleges.add(row[0])

print len(freebase_colleges)
print len(ipeds_colleges)

outfile = open('freebase-vs-ipeds.txt', 'w')

diff = freebase_colleges - ipeds_colleges
for x in diff:
  outfile.write( x + '\n' )

outfile = open('ipeds-vs-freebase.txt', 'w')

diff = ipeds_colleges - freebase_colleges
for x in diff:
  outfile.write( x + '\n' )

# Debt vs ipeds

outfile = open('debt-vs-ipeds.txt', 'w')

diff = debt_colleges - ipeds_colleges
for x in diff:
  outfile.write( x + '\n' )

# Ipeds vs debt

outfile = open('ipeds-vs-debt.txt', 'w')

diff = ipeds_colleges - debt_colleges
for x in diff:
  outfile.write( x + '\n' )

# colleges-for-jesse
colleges_jesse = set()