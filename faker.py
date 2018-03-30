import random
import string
from random import randint

"""
Fake credes generator v0.1

Fake creds include

1. username
- get_random_string(letters_set, length) or get_random_string(letters_set, length, True) 
	Send True as third param to use symbols as well.

2. password
- get_random_string(letters_set, length, True)

3. email
- get_random_email(length)

4. dob
- get_random_dob()

5. gender
- get_random_gender()

"""

domains = [ "hotmail.com", "gmail.com", "aol.com", "outlook.com", "yahoo.com"]
gender = ["m", "f", "s", "c"]
letters = string.ascii_lowercase[:26]

symbols = '~!@#$%^&*()_+`-=,./;[]<>?:'
numbers = '123456789'

def get_random_domain(domains):
    return random.choice(domains)

def get_random_string(letters, length, special_symbols=False):
	if not special_symbols:
		return ''.join(random.choice(letters) for i in range(length))
	return ''.join(random.choice(letters) for i in range(int(length/2)+1)).join(random.choice(symbols) for i in range(2)).join(random.choice(numbers) for i in range(2))

def get_random_dob():
	return str(randint(1,12))+"-"+str(randint(1,28))+"-"+str(randint(1901, 2000))
	
def get_random_gender():
	return get_random_domain(gender)

def get_random_email(length):
	return get_random_string(letters, length) + '@' + get_random_domain(domains)

def generate_random_emails(nb, length):
    return [get_random_string(letters, length) + '@' + get_random_domain(domains) for i in range(nb)]

def generate_random_usernames(nb, length):
    return [get_random_string(letters, length) + '_' + get_random_string(letters, int(3)) for i in range(nb)]

def main():
    print(generate_random_emails(10, 7))
    print("Username:"+ generate_random_usernames(10, 8))

def generate_data(registration_limit):
	print("Generating random data for "+ str(registration_limit))
	return [{'username': get_random_string(letters, 10), 'password': get_random_string(letters+symbols+numbers, 7, True), 'email': get_random_email(9), 'dob': get_random_dob(), 'gender': get_random_gender()} for i in range(registration_limit)]

if __name__ == "__main__":
    main()