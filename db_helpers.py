import psycopg2
import psycopg2.extras

class DbConn:
	con = None
	host = "localhost"
	user = "postgres"
	password = "password"
	dbname = "chaturbate_bot"
	users_table = "users"

	def __init__(self):
		self.con = psycopg2.connect(user=self.user, password=self.password, host=self.host, database=self.dbname)

	def insert(self, table, dataset):
		cur = self.con.cursor()
		keys_set = [key for key in dataset]
		cols = ",".join(keys_set)
		values_set = ["\'"+dataset[key]+"\'" for key in dataset]
		values = ",".join(values_set)
		try:
			cur.execute("INSERT INTO %s(%s) VALUES(%s)" % (table, cols, values))
		except Exception as e:
			# incase of any db exception.
			print(e)
		self.con.commit()

	def update(self, table, dataset, condition):
		cur = self.con.cursor()
		# keys_set = [key for key in dataset]
		# cols = ",".join(keys_set)
		# values_set = ["\'"+dataset[key]+"\'" for key in dataset]
		# values = ",".join(dataset)
		try:
			cur.execute("UPDATE %s SET %s WHERE %s" % (table, dataset, condition))
		except Exception as e:
			# incase of any db exception.
			print(e)
		self.con.commit()

	def select(self, table, dict=False, condition=False):
		if dict:
			cur = self.con.cursor(cursor_factory=psycopg2.extras.DictCursor)
		else:
			cur = self.con.cursor()
		result = []
		try:
			if condition:
				cur.execute("SELECT * FROM %s WHERE %s LIMIT 5" % (table, condition))
			else:
				cur.execute("SELECT * FROM %s" % (table))
			for row in cur.fetchall():
				result.append({'id': row['id'], 'username': row['username'], 'password': row['password'], 'email': row['email'], 'dob': row['dob'], 'gender': row['gender']})
			return result
		except Exception as e:
			# incase of any db exception.
			print(e)
		return False