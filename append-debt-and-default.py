import csv

# IPEDS 2012
test_scores = set()

with open('ipeds-2012.csv', 'rU') as csvfile:
  reader = csv.reader(csvfile)
  next(reader, None)
  for row in reader:
    if row[4] == "Required":
      test_scores.add(int(row[0]))

outfile = open('master-with-sat-debt-and-default.csv', 'w')
writer = csv.writer(outfile)

# Append debt rates with IPEDS
debt_ipeds = set()
debt_ipeds_dict = dict()

with open('debt.csv', 'rU') as csvfile:
  reader = csv.reader(csvfile)
  next(reader, None)
  for row in reader:
    if row[2] != "N/A":
      debt_ipeds.add(int(row[3]))
      debt_ipeds_dict[int(row[3])] = row # 2

# Append default rates with OPEID
default_opeid = set()
default_opeid_dict = dict()

with open('default_rates.csv', 'rU') as csvfile:
  reader = csv.reader(csvfile)
  next(reader, None)
  for row in reader:
    default_opeid.add(int(row[0] + '00'))
    default_opeid_dict[int(row[0] + '00')] = row # 11 and 12

with open('master-with-sat.csv', 'rU') as csvfile:
  reader = csv.reader(csvfile)
  row = next(reader)
  writer.writerow( row[0:6] + ['Test Scores Required'] + row[6:] + ['Avg Debt of Graduates', 'NBD 1', 'NBR 1', 'DRATE'] )
  for row in reader:
    new_row = row
    if (int(row[0]) in test_scores):
      new_row = new_row[0:6] + ['YES'] + new_row[6:]
    else:
      new_row = new_row[0:6] + ['NO'] + new_row[6:]
    if (int(row[0]) in debt_ipeds):
      new_row = new_row + [debt_ipeds_dict[int(row[0])][2]]
    else:
      new_row = new_row + ['']
    if row[4] and (row[4] != '') and (row[4].isdigit()) and (int(row[4]) in default_opeid):
      new_row = new_row + [default_opeid_dict[int(row[4])][11], default_opeid_dict[int(row[4])][12]]
      if (default_opeid_dict[int(row[4])][11] == '0.00' and default_opeid_dict[int(row[4])][12] == '0.00'):
        new_row = new_row + ['']
      else:
        new_row = new_row + [default_opeid_dict[int(row[4])][13]]
    else:
      new_row = new_row + ['']*3

    writer.writerow(new_row)