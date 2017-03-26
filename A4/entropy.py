from sets import Set

def entropy(password):
	total_entropy = 0
	uppercase_exists = False
	non_alphabet_exists = False

	for i in range(len(password)):
		if i == 0:
			total_entropy += 4
		elif i in range(1,8):
			total_entropy += 2
		elif i in range(8,20):
			total_entropy += 1.5
		else:
			total_entropy += 1

		if password[i].isupper():
			uppercase_exists = True

		if not password[i].isalpha():
			non_alphabet_exists = True

	if uppercase_exists and non_alphabet_exists:
		total_entropy += 6



	return total_entropy


def simple_transformation(password):

	num_char = {}
	num_char['0'] = 'o'
	num_char['1'] = 'l'
	num_char['3'] = 'e'
	num_char['4'] = 'a'
	num_char['5'] = 's'
	num_char['7'] = 't'
	num_char['8'] = 'b'
	num_char['@'] = 'a'
	num_char['$'] = 's'


	transformed = password.lower()

	transformed = ''.join([num_char[i] if i in num_char else i for i in transformed])

	return transformed



def dictionary_without_vowels(dictionary):
	new_dictionary = Set()

	vowels = 'aeiou'

	for i in dictionary:
		new_string = i
		for v in vowels:
			new_string = new_string.replace(v,'')

		if new_string != '':
			new_dictionary.add(new_string)

	return new_dictionary



