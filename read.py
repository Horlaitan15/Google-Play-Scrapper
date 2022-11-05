import csv


with open('upwork.csv', 'r') as f:
    reader = csv.DictReader(f)
    for i in reader:
        print(list(i.values()))

print(list(reversed({'me': 'they'})))