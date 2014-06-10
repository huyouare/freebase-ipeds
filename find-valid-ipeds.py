from __future__ import division
from bs4 import BeautifulSoup
import urllib2
import csv

f = open('valid-ipeds.txt', 'w')
count = 0
total = 0

for x in range(999999):
  link = 'http://nces.ed.gov/collegenavigator/?id=' + str(x)
  response = urllib2.urlopen(link).read()
  soup = BeautifulSoup(response)
  print soup.title.string
  noresults = soup.find(class_='noresults')

  if noresults:
    f.write(str(x) + '\n')
  else:
    total = total + 1

  print total
