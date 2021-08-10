import csv

name = input("what is your name?")
score = input("what is your score?")
time = input("what is your time?")
with open('test.csv', 'a', newline = '') as f:
    writer = csv.writer(f)
    writer.writerow([name,score,time])
    