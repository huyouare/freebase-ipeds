import csv

from fuzzywuzzy import fuzz

outfile = open('output-debug-with-ratios', 'w')
writer = csv.writer(outfile)

with open('output-debug.tsv', 'rb') as f:
  reader = csv.reader(f, delimiter='\t')
  first_row = next(reader)
  first_row.append("fuzzywuzzy ratio")
  writer.write(first_row)
  for row in reader:
    ratio = fuzz.partial_ratio(row[3], row[4])
    row.append(ratio)
    writer.write(row)
