import mysql.connector
db = mysql.connector.connect(host='localhost',user='root',passwd='Joga@1406',database='deep')
cur = db.cursor()
cur.execute("show tables")
for i in cur:
    print(i)