# 
import csv

freebase_id_dict = dict()
freebase_name_dict = dict()

freebase_colleges = set()
with open('freebase-colleges-iped.csv', 'rU') as csvfile:
  reader = csv.reader(csvfile)
  next(reader)
  for row in reader:
    freebase_colleges.add(row[0])
    freebase_id_dict[row[0]] = row[1]
    freebase_name_dict[row[0]] = row[2]

union_dict = dict()

union_colleges = set()
with open('union.csv', 'rU') as csvfile:
  reader = csv.reader(csvfile)
  next(reader, None)
  for row in reader:
    union_colleges.add(row[0])
    union_dict[row[0]] = row

intersect = union_colleges.intersection(freebase_colleges)
union_diff = union_colleges - freebase_colleges
freebase_diff = freebase_colleges - union_colleges

# outfile = open('union-freebase.csv', 'w')
# union_writer = csv.writer(outfile)

# outfile = open('links.html', 'w')
# outfile2 = open('links.txt', 'w')

with open('union-freebase.csv', 'wb') as csvfile:
  writer = csv.writer(csvfile)
  writer.writerow(['IPEDS', 'ipeds_name', 'doe_id', 'doe_name', 'freebase_id', 'freebase_name'] + ['DRVIC2012.Percent admitted - total', 'DRVGR2012.Graduation rate - bachelor\'s degree within 6 years, total', 'IC2012.SAT Critical Reading 25th percentile score', 'IC2012.SAT Critical Reading 75th percentile score', 'IC2012.SAT Math 25th percentile score', 'IC2012.SAT Math 75th percentile score', 'IC2012.SAT Writing 25th percentile score', 'IC2012.SAT Writing 75th percentile score'])
  
  for x in intersect:
    writer.writerow([ x, union_dict[x][1], union_dict[x][2], union_dict[x][3], freebase_id_dict[x], freebase_name_dict[x] ] + union_dict[x][4:])
  for x in union_diff:
    writer.writerow([ x, union_dict[x][1], union_dict[x][2], union_dict[x][3], '', '' ] + union_dict[x][4:])
  for x in freebase_diff:
    writer.writerow([ x, '', '', '', freebase_id_dict[x], freebase_name_dict[x] ])