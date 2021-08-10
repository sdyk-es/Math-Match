import csv, operator

# name = input("what is your name?")
# score = input("what is your score?")
# time = input("what is your time?")
# with open('test.csv', 'a', newline = '') as f:
#     writer = csv.writer(f)
#     writer.writerow([name,score,time])

with open('test.csv', 'r', newline = '') as f:
    reader = csv.reader(f)

    sortedlist = sorted(reader, key=operator.itemgetter(1))
    for line in sortedlist:
        print(line)
    