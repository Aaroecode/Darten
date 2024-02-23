from app.utilities.dbSql import sqldb

db = sqldb()
cursor = db.cursor
connection = db.connection

cursor.execute("DELETE FROM `tickets`")
connection.commit()

