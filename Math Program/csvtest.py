import csv

name = "Sam"
score = 363
time = 17
with open('test.csv', 'w', newline = '') as f:
    writer = csv.writer(f)
    