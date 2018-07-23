import csv

csv_reader = csv.reader(open('LinkShareItemscsv.csv'))
i = []
for row in csv_reader:
    i.extend(row)

print(i)