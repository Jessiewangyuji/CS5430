import sys

logpath = sys.argv[1]
print logpath

with open(logpath, "r") as log:
    while line in log:
        print line

