# import pyodbc

# conn = pyodbc.connect('DRIVER={SQL Server};SERVER=LAPTOP-4BMP64EE\\SQLEXPRESS;DATABASE=ipmsdb')
# print(conn)
# cursor = conn.cursor()
# cursor.execute("SELECT * from tbl_user")
# for i in cursor.fetchall():
#     print(i)

from werkzeug.security import generate_password_hash, check_password_hash
print(generate_password_hash('password'))