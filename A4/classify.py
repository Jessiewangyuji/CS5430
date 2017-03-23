from sets import Set

def create_wordList():
    global words
    with open("dictionary.txt") as file:
        for line in file:
            words.add(line.strip())

words = Set()
create_wordList()

while True:
    weakC = 0
    password = raw_input("Enter password:")
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
    for i in range(len(password)):
        for j in range(i + 1, len(password)):
            if password[i:j] in words:
                meaningful += 1
                meaningfulChar += j - i
            if (password[i:j] in key_line1 or password[i:j] in key_line2 \
                or password[i:j] in key_line3) and (j - i) > 3:
                contig_key = True

    if meaningfulChar > len(password) / 2: #Ranfom number i m choosing
        weakC += 1
    
    if contig_key:
        weakC += 1

    # number entropy? 1234
    # char entropy? abc

    #predictable number? 19xx 20xx
    if weakC == 0:
        print "strong"
    else:
        print "weak"




