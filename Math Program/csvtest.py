import csv

# name = input("what is your name?")
# score = input("what is your score?")
# time = input("what is your time?")
# with open('test.csv', 'a', newline = '') as f:
#     writer = csv.writer(f)
#     writer.writerow([name,score,time])

with open('test.csv', 'r', newline = '') as f:
    reader = csv.reader(f)
    sortedlist = sorted(reader, key = lambda elem: int(elem[1]), reverse = True) 
    for line in sortedlist:
        print(line[0] + " reached " + line[1] + " points in " + line[2] + " seconds!")
    