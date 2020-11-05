from utils import *

pg_connection = get_pg_connection()
cursor = pg_connection.cursor()
sql_file = open("schema.sql", "r")
cursor.execute(sql_file.read())
cursor.close()
pg_connection.commit()
