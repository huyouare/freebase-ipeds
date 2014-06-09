# 
import csv

accred_id_dict = dict()
accred_name_dict = dict()

accred_colleges = set()
with open('accredidation-ipeds.csv', 'rU') as csvfile:
  reader = csv.reader(csvfile)
  for row in reader:
    accred_colleges.add(row[8])
    accred_id_dict[row[8]] = row[0]
    accred_name_dict[row[8]] = row[1]

ipeds_dict = dict()

ipeds_colleges = set()
with open('./datasets/ipeds_data_for_production_database.csv', 'rU') as csvfile:
  reader = csv.reader(csvfile)
  next(reader, None)
  for row in reader:
    ipeds_colleges.add(row[0])
    ipeds_dict[row[0]] = row

intersect = ipeds_colleges.intersection(accred_colleges)
ipeds_diff = ipeds_colleges - accred_colleges
accred_diff = accred_colleges - ipeds_colleges

outfile = open('union.csv', 'w')
union_writer = csv.writer(outfile)

outfile = open('links.html', 'w')
outfile2 = open('links.txt', 'w')

with open('join.csv', 'wb') as csvfile:
  writer = csv.writer(csvfile)
  writer.writerow(['IPEDS', 'ipeds_name', 'doe_id', 'doe_name'] + ['DRVIC2012.Percent admitted - total', 'DRVGR2012.Graduation rate - bachelor\'s degree within 6 years, total', 'IC2012.SAT Critical Reading 25th percentile score', 'IC2012.SAT Critical Reading 75th percentile score', 'IC2012.SAT Math 25th percentile score', 'IC2012.SAT Math 75th percentile score', 'IC2012.SAT Writing 25th percentile score', 'IC2012.SAT Writing 75th percentile score'])
  union_writer.writerow(['IPEDS', 'ipeds_name', 'doe_id', 'doe_name'] + ['DRVIC2012.Percent admitted - total', 'DRVGR2012.Graduation rate - bachelor\'s degree within 6 years, total', 'IC2012.SAT Critical Reading 25th percentile score', 'IC2012.SAT Critical Reading 75th percentile score', 'IC2012.SAT Math 25th percentile score', 'IC2012.SAT Math 75th percentile score', 'IC2012.SAT Writing 25th percentile score', 'IC2012.SAT Writing 75th percentile score'])
  for x in intersect:
    writer.writerow([ x, ipeds_dict[x][1], accred_id_dict[x], accred_name_dict[x] ] + ipeds_dict[x][2:])
    union_writer.writerow([ x, ipeds_dict[x][1], accred_id_dict[x], accred_name_dict[x] ] + ipeds_dict[x][2:])
  for x in ipeds_diff:
    union_writer.writerow([ x, ipeds_dict[x][1], '', '' ] + ipeds_dict[x][2:])
  for x in accred_diff:
    union_writer.writerow([ x, '', accred_id_dict[x], accred_name_dict[x] ])
  for x in accred_diff:
    outfile.write( '<a href="http://nces.ed.gov/collegenavigator/?id=' + x + '">' + x + '</a>' + '\n' )
    outfile2.write( 'http://nces.ed.gov/collegenavigator/?id=' + str(x) )