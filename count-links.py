from __future__ import division
from bs4 import BeautifulSoup
import urllib2
import csv

# f = open('links.txt', 'r')
# content = f.readlines()

f = open('./diff-output/ipeds-vs-accred.txt', 'r')
content = f.readlines()

count = 0
total = 0

for link in content:
  link = 'http://nces.ed.gov/collegenavigator/?id=' + str(link)

  print link
  response = urllib2.urlopen(link).read()
  soup = BeautifulSoup(response)
  print soup.title.string
  noresults = soup.find(class_='noresults')

  if noresults:
    count = count + 1
    total = total + 1
  else:
    total = total + 1

  print count
  print total

print 'Count: ' + str(count)
print 'Total: ' + str(total)
print 'Ratio: ' + str(count / total)