#Master script

# 0: IPEDS ID
# 1: College Navigator name or from source (Accred, Freebase, IPEDS) by longer name
# 2: Accred ID
# 3: Freebase MID
# 4: OPE ID (from College Navigator, else DoE)
# 5: 4 Year (YES) or (NO)

from __future__ import division
from bs4 import BeautifulSoup
import urllib2
import csv
import sys
#from fuzzywuzzy import process

def run(int_suffix):
  outfile = open('master-matching-' + str(int_suffix) + '.csv', 'w')
  writer = csv.writer(outfile)

  #Get OPE IDs from accredidation
  accred = set()
  accred_opeid = dict()

  with open('accredidation-ipeds.csv', 'rU') as f:
    reader = csv.reader(f)
    first_row = next(reader)
    for row in reader:
      if len(row[7])>0:
        accred.add(row[0])
        accred_opeid[row[0]] = row[7].split('"')[1]


  #Get postsecondary data from 2012 IPEDS
  ipeds_2012 = set()
  ipeds_2012_names = dict()
  ipeds_2012_opeid = dict()
  ipeds_2012_hloffer = dict() # Highest Level Offered
                              # where 5 = Batchelor's degree

  with open('hd2012_data_stata.csv', 'rU') as f:
    reader = csv.reader(f)
    first_row = next(reader)
    for row in reader:
      ipeds_2012.add(row[0])
      ipeds_2012_names[row[0]] = row[1]
      ipeds_2012_opeid[row[0]] = row[12]
      ipeds_2012_hloffer[row[0]] = int(row[22])


  #Start matching process
  with open('union-freebase-with-name-conflicts-sorted.csv', 'rU') as f:
    reader = csv.reader(f)
    first_row = next(reader)
    num_skip = int_suffix*2000
    for x in range(0, num_skip+1):
      next(reader)
    new_first_row = [ 'IPEDS ID', 'Name', 'DoE ID', 'Freebase mid', 'OPE ID', 'Four-Year' ]
    writer.writerow(new_first_row)
    
    for row in reader:
      ipeds = row[1]
      name = ''
      accred_id = ''
      mid = ''
      opeid = ''
      four_year = ''

      accred_id = row[3]
      mid = row[5]

      if ipeds in ipeds_2012:
        name = ipeds_2012_names[ipeds]
        opeid = ipeds_2012_opeid[ipeds]
        print "In ipeds_2012: " + name + " " + opeid + " HLOFFER: " + str(ipeds_2012_hloffer[ipeds])
        four_year = 'YES' if (ipeds_2012_hloffer[ipeds] >= 5) else 'NO'
        print "Four-Year: " + four_year

      else:
        link = 'http://nces.ed.gov/collegenavigator/?id=' + str(ipeds)
        print link
        response = urllib2.urlopen(link).read()
        soup = BeautifulSoup(response)
        print soup.title.string
        noresults = soup.find(class_='noresults')
        
        # Not found in college navigator
        if noresults:
          names = list()
          names.append(row[2])
          names.append(row[4])
          names.append(row[6])
          name = max(names, key=len)
          if ipeds in accred:
            opeid = accred_opeid[ipeds]

        # Found in college navigator
        else:
          name = soup.find(class_='headerlg').string
          ipeds_string = soup.find(class_='mapngo').find(class_='ipeds').text
          if "OPEID: " in ipeds_string:
            opeid = ipeds_string.split("OPE ID: ")[1]
            opeid = int(opeid)
            print "OPEID: " + str(opeid)
          elif ipeds in accred:
            opeid = accred_opeid[ipeds]
          navigator_rows = soup.find_all(class_='srb')
          print navigator_rows[2]
          four_year = 'YES' if ('4-year' in navigator_rows[2]) else 'NO'
          print "Four-Year: " + four_year

      writer.writerow([ ipeds, name, accred_id, mid, str(opeid), four_year ])

run(int(sys.argv[1]))
