#!/user/bin/python
import os

DATABASE_NAME = os.environ.get('DATABASE_NAME')
DATABASE_USER = os.environ.get('DATABASE_USER')
DATABASE_PASS = os.environ.get('DATABASE_PASS') 
DATABASE_HOST = os.environ.get('DATABASE_HOST')

TABLE_NAME = os.environ.get('TABLE_NAME') 

'''
The database entries for blogs which are yet to get published, 
will get published using this script
This script does the following:

1. Access database using python.
2. Compare the time in database table field "published" 
   with present time
3. Run the query to update database table entry "published_state" as True 
   for dates in "published" which are before present
4. Close connection. 

'''
import MySQLdb

if __name__=="__main__":
	# Open database connection
	try:
		db = MySQLdb.connect(os.environ.get('DATABASE_HOST'),
								os.environ.get('DATABASE_USER'),
								os.environ.get('DATABASE_PASS'),
								os.environ.get('DATABASE_NAME'))
			
		# prepare a cursor object using cursor() method
		cursor = db.cursor()

		# execute SQL query using execute() method.
		cursor.execute("update ebs_blog set published_state=1, is_enable=1 where DATE(published)<=DATE(now()) and is_enable=0 and draft=0")
		db.commit()
		# Fetch a single row using fetchone() method.
		print "running script"
		# disconnect from server
		db.close()
	except Exception as e:
		print e