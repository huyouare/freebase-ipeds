from bs4 import BeautifulSoup
import csv

f = open('ipeds-full.html', 'r')
soup = BeautifulSoup(f)
rows = soup.find_all(class_='data-row')
print len(rows)
# print(row.find(class_='wrapper').text)
# for row in rows:
#   print row.find(class_='mid key-value').string
#   print row.find(class_='property-value key-namespace').string
#   print row.find(class_='name').string
#   print row.find(class_='date').string

with open('eggs.csv', 'wb') as csvfile:
  writer = csv.writer(csvfile)
  writer.writerow(['key', 'freebase ID', 'name', 'date'])
  for row in rows:
    key = row.find(class_='mid key-value').string
    freebase = row.find(class_='property-value key-namespace').string
    name = row.find(class_='name').string
    date = row.find(class_='date').string
    writer.writerow([key.encode('utf8'), freebase.encode('utf8'), name.encode('utf8'), date.encode('utf8')])