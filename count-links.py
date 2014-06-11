from __future__ import division
from bs4 import BeautifulSoup
import urllib2
import csv

# f = open('links.txt', 'r')
# content = f.readlines()

f = open('./diff-output/accred-vs-ipeds-with-names.csv', 'r')
reader = csv.reader(f)
next(reader)

outfile = open('accred-not-found.csv', 'w')
writer = csv.writer(outfile)
writer.writerow(['IPEDS ID', 'School Name', 'OPE ID'])

count = 0
total = 0

for row in reader:
  link = 'http://nces.ed.gov/collegenavigator/?id=' + str(row[0])

  print link
  response = urllib2.urlopen(link).read()
  soup = BeautifulSoup(response)
  print soup.title.string
  noresults = soup.find(class_='noresults')

  if noresults:
    writer.writerow(row)
    count = count + 1
    total = total + 1
  else:
    total = total + 1

  print count
  print total

print 'Count: ' + str(count)
print 'Total: ' + str(total)
print 'Ratio: ' + str(count / total)