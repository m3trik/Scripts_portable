from __future__ import print_function
import sqlite3
from sqlite3 import Error



class Database():
	'''
	Create and/or connect to an SQLite database.
	'''
	def __init__(self, database):
		'''
		args:
			database (str) = An absoute path to the database file. 
							':memory:' will create a new database that resides in RAM instead of a file on disk.
							If you just give a filename, the program will create the database file in the current working directory.
		'''
		try:
			self.conn = sqlite3.connect(database)
			if self.conn:
				self.cur = self.conn.cursor()
			else:
				print("Error: Cannot create the database connection.")

		except Error as e:
			print (e)


	def create_tables(self, tables):
		'''
		Create a table.

		args:
			tables (str)(list) = SQL create table statement(s).
		'''
		if not isinstance(tables, (set, tuple, list)):
			tables = [tables]

		# create tables
		for table in tables:
			try:
				self.cur.execute(table)
			except Exception as e:
				print(e)


	def insert(self, table, *args, **kwargs):
		'''
		Insert values into a table.

		args:
			table (str) = table.
			args (list) = column values.
			kwargs (dict) = column:value pairs for assigning values to specific columns.

		returns:
			(int) the value generated for a column during the last INSERT or, UPDATE operation.
		'''
		columns = '' #omit the columns argument if no columns are given.
		if kwargs.keys():
			columns = '('+', '.join(str(i) for i in kwargs.keys())+')'

		values  = ', '.join('"'+str(i)+'"' for i in kwargs.values()+list(args))

		sql = '''
			INSERT INTO {table} {columns}
			VALUES ({values});
			'''.format(table=table, columns=columns, values=values)

		self.cur.execute(sql)
		self.conn.commit()

		return self.cur.lastrowid


	def update(self, table, condition=None, *args, **kwargs):
		'''
		Update all values of a table, or those matching a given condition.

		args:
			table (str) = table. 
			condition (str) = SQL condition statement. You can combine any number of conditions using AND or OR operators.
			kwargs (dict) = column:value pairs for assigning values to specific columns.
		'''
		kw_item_value_pairs = ('{}={}'.format(k,v) for k,v in kwargs.items())

		formatted_kwargs = ', '.join('"'+str(i)+'"' for i in kw_item_value_pairs)
		formatted_args = ', '.join('"'+str(i)+'"' for i in args)

		values = formatted_args+', '+formatted_kwargs if args else formatted_kwargs

		if condition:
			sql = '''
				UPDATE {table}
				SET ({values})
				WHERE {condition}
				'''.format(table=table, values=values, condition=condition)
		else:
			sql = '''
				UPDATE {table}
				SET ({values})
				'''.format(table=table, values=values)

		self.cur.execute(sql)
		self.conn.commit()


	def select(self, table, condition=None):
		'''
		Select all of a table's content, or those matching a given condition.

		args:
			table (str) = The table in which to perform the selection.
			condition (str) = SQL condition statement. You can combine any number of conditions using AND or OR operators.
		'''
		if condition:
			sql = 'SELECT * FROM {table} WHERE {condition}'.format(table=table, condition=condition)
		else:
			sql = 'SELECT * FROM {table}'.format(table=table)

		self.cur.execute(sql)

		rows = self.cur.fetchall()
		for row in rows:
			print (row)


	def delete(self, table, condition=None):
		'''
		Delete all rows, or those matching a given condition.

		args:
			table (str) = The table in which to perform the delete operation.
			condition (str) = SQL condition statement. You can combine any number of conditions using AND or OR operators.
		'''
		if condition:
			sql = 'DELETE FROM {table} WHERE {condition}'.format(table=table, condition=condition)
		else:
			sql = 'DELETE FROM {table}'.format(table=table)

		self.cur.execute(sql)
		self.conn.commit()






if __name__ == '__main__':

	db = Database("prefs.db")

	tables = ['''
		CREATE TABLE IF NOT EXISTS projects (
			id integer PRIMARY KEY,
			name text NOT NULL,
			begin_date text,
			end_date text
		);''',

		'''
		CREATE TABLE IF NOT EXISTS tasks (
			id integer PRIMARY KEY,
			name text NOT NULL,
			priority integer,
			status_id integer NOT NULL,
			project_id integer NOT NULL,
			begin_date text NOT NULL,
			end_date text NOT NULL,
			FOREIGN KEY (project_id) REFERENCES projects (id)
		);''']

	db.create_tables(tables)

	# create a new project
	project_id = db.insert('projects', name='Project_Name', begin_date='2020-01-01', end_date='2020-01-30')
	# project_id = db.insert('projects', 0, 'Project_Name', '2020-01-01', '2020-01-30')

	# create tasks
	task1_id = db.insert('tasks', name='Analyze the requirements of the app', priority=1, status_id=1, project_id=project_id, begin_date='2020-01-01', end_date='2020-01-02')
	task2_id = db.insert('tasks', name='Confirm with user about the top requirements', priority=1, status_id=1, project_id=project_id, begin_date='2020-01-03', end_date='2020-01-05')


	# db.select('tasks')
	# db.delete('projects')

	print (project_id, task1_id, task2_id)