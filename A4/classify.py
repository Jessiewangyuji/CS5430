from sets import Set
from entropy import *

def create_wordList():
    global words
    with open("dictionary.txt") as file:
        for line in file:
            words.add(line.strip())

words = Set()
create_wordList()

while True:
    weakC = 0
    password = raw_input("Enter password(Press <ENTER> to quit): ")
    if password == "":
        break

    # >8 char
    if len(password) < 8:
        weakC += 1

    # not only numbers:
    try:
        int(password)
        weakC += 1
    except:
        pass

    # contains numbers & special char:
    numbers = "1234567890"
    symbol = "~`!@#$%^&*()_-+={}[]:>;',</?*-+"
    numC = 0
    symC = 0
    for i in range(len(password)):
        if password[i] in numbers:
            numC += 1
        if password[i] in symbol:
            symC += 1

    if numC == 0 and symC == 0:
        weakC += 1

    # contains too many meaningful words
    meaningful = 0
    meaningfulChar = 0
    
    #qwerty...
    key_line1 = "qwertyuiop"
    key_line2 = "asdfghjkl"
    key_line3 = "zxcvbnm"
    
    contig_key = False
    meaningfulSet = Set()
    transformed = simple_transformation(password)
    for i in range(len(password)):
        for j in range(i + 4, len(password)):
            if transformed[i:j] in words:
                print transformed[i:j]
                for k in range(i, j):
                    meaningfulSet.add(k)
        
            if (password[i:j] in key_line1 or password[i:j] in key_line2 \
                or password[i:j] in key_line3) and (j - i) > 3:
                contig_key = True

    if len(meaningfulSet) > len(password) / 2: #Random number i m choosing
        print meaningfulSet
        weakC += 1
    
    if contig_key:
        weakC += 1

    # entropy
    prevInd = -1
    prevChar = 0
    prevDiff = 0
    prevIndDiff = 0
    count = 0
    for i in range(len(password)):
        if ord(password[i]) - prevChar == prevDiff and i - prevInd == prevIndDiff:
            count += 1
            if count > len(password) / 4:
                weakC += 1
        else:
            count = 0
        prevIndDiff = i - prevInd
        prevInd = i
        prevDiff = ord(password[i]) - prevChar
        prevChar = ord(password[i])

    if count > len(password) / 2:
        weakC += 1

    #repetition
    for length in range(1, len(password) / 2):
        i = 0
        j = i + length
        repetitionTable = {}
        while j < len(password):
            if password[i:j] in repetitionTable:
                repetitionTable[password[i:j]] += 1
            else:
                repetitionTable[password[i:j]] = 1
            i = j + 1
            j = i + length

        i = 0
        j = i + length
        while j < len(password):
            if repetitionTable[password[i:j]] > len(password) / (2 * length):
                weakC += 1
                print "weak repetition"
            i = j + 1
            j = i + length

    #predictable number? 19xx 20xx
    if weakC == 0:
        entropyC = entropy(password)
        print entropyC
        if entropyC > 25:
            print "strong"
        else:
            print "weak"
    else:
        print "weak"




