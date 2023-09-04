import sqlite3
connection = sqlite3.connect("users_database.db")

cursor = connection.cursor()


cursor.execute("INSERT INTO users VALUES ('2005892', 'Aa@12345', 'Ranya Alghamdi', '2005892@uj.edu.sa', 'student')")
cursor.execute("INSERT INTO users VALUES ('1905480', 'Aa@12346', 'Manar Eyad', '1905480@uj.edu.sa', 'student')")
cursor.execute("INSERT INTO users VALUES ('1905453', 'Aa@12347', 'Sumaia Ahmed', '1905453@uj.edu.sa', 'student')")
cursor.execute("INSERT INTO users VALUES ('2006786', 'Aa@12348', 'Raneem Aljadani', '2006786@uj.edu.sa', 'student')")
cursor.execute("INSERT INTO users VALUES ('4514542', 'Aa@12349', 'ELHAM ALGAMDI', '4514542@uj.edu.sa', 'employee')")

connection.commit()
