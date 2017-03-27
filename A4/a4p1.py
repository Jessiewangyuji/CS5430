from sets import Set
import hashlib
import random
import timeit
import struct
import itertools

def create_wordList():
    myspace_passwords = Set()
    with open("myspace.txt") as file:
        for line in file:
            myspace_passwords.add(line.strip())

    return myspace_passwords


def question1():
    words = create_wordList()

    print len(words)

    output = []

    start = timeit.default_timer()
    for count in range(10):
        salt = random.getrandbits(32)   
        for i in words:

            output.append((salt, hashlib.sha512(i + str(salt)).digest(),i))

        print count

    with open('a4p1output.txt','w') as file_out:
        for x in output:
            file_out.write('%s %s %s\n' % (struct.pack("I",x[0]),x[1],x[2]))
    end = timeit.default_timer()

    print end-start

#taken from here: http://stackoverflow.com/questions/2612648/reservoir-sampling 
#for randomly selecting K items from a list
def random_subset( iterator, K ):
    result = []
    N = 0

    for item in iterator:
        N += 1
        if len( result ) < K:
            result.append( item )
        else:
            s = int(random.random() * N)
            if s < K:
                result[ s ] = item

    return result

def question2():

    selection = '1234567890abcdefghijklmnopqrstuvwxyz'
    print len(selection)
    output = []
    list_of_passwords = [''.join(i) for i in list(itertools.product(selection,repeat=4))]
    print len(list_of_passwords)
    start = timeit.default_timer()

    for i in list_of_passwords:
        output.append((hashlib.sha512(i).digest(),i))

    with open('a4p1output2.txt','w') as file_out:
        for x in output:
            file_out.write('%s %s\n' % (x[0],x[1]))
    end = timeit.default_timer()

    print end-start

question1()
question2()


