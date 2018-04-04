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

class Faker:
	domains = [ "hotmail.com", "gmail.com", "aol.com", "outlook.com", "yahoo.com"]
	gender = ["m", "f", "s", "c"]
	letters = string.ascii_lowercase[:26]
	symbols = '~!@#$%^&*()_+`-=,./;[]<>?:'
	numbers = '123456789'

	def get_random_domain(self, domains):
		return random.choice(self.domains)

	def get_random_string(self, letters, length, special_symbols=False):
		if not special_symbols:
			return ''.join(random.choice(letters) for i in range(length))
		return ''.join(random.choice(letters) for i in range(int(length/2)+1)).join(random.choice(self.symbols) for i in range(2)).join(random.choice(self.numbers) for i in range(2))

	def get_random_dob(self):
		return str(randint(1,12))+"-"+str(randint(1,28))+"-"+str(randint(1901, 2000))

	def get_random_gender(self):
		return random.choice(self.gender)

	def get_random_email(self, length):
		return self.get_random_string(self.letters, length) + '@' + self.get_random_domain(self.domains)

	def generate_random_emails(self, nb, length):
		return [self.get_random_string(self.letters, length) + '@' + self.get_random_domain(self.domains) for i in range(nb)]

	def generate_random_usernames(self, nb, length):
		return [self.get_random_string(self.letters, length) + '_' + self.get_random_string(self.letters, int(3)) for i in range(nb)]

	def main(self):
		print(self.generate_random_emails(10, 7))
		print("Username:"+ self.generate_random_usernames(10, 8))

	def generate_data(self, registration_limit):
		print("Generating random data for "+ str(registration_limit))
		return [{'username': self.get_random_string(self.letters, 10), 'password': self.get_random_string(self.letters+self.symbols+self.numbers, 12, True), 'email': self.get_random_email(9), 'dob': self.get_random_dob(), 'gender': self.get_random_gender()} for i in range(registration_limit)]
		