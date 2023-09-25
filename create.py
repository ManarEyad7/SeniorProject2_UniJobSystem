import sqlite3
connection = sqlite3.connect("users_database.db")

cursor = connection.cursor()


#cursor.execute("INSERT INTO users VALUES ('2005892', 'Aa@12345', 'Ranya Alghamdi', '2005892@uj.edu.sa', 'student')")
#cursor.execute("INSERT INTO users VALUES ('1905480', 'Aa@12346', 'Manar Eyad', '1905480@uj.edu.sa', 'student')")
#cursor.execute("INSERT INTO users VALUES ('1905453', 'Aa@12347', 'Sumaia Ahmed', '1905453@uj.edu.sa', 'student')")
#cursor.execute("INSERT INTO users VALUES ('2006786', 'Aa@12348', 'Raneem Aljadani', '2006786@uj.edu.sa', 'student')")
#cursor.execute("INSERT INTO users VALUES ('4514542', 'Aa@12349', 'ELHAM ALGAMDI', '4514542@uj.edu.sa', 'employee')")
#cursor.execute("INSERT INTO users VALUES ('4514534', 'Aa@12340', 'AHHLAM MOHAMMED', '4514534@uj.edu.sa', 'employee')")

#cursor.execute("""
#CREATE TABLE job_posts (
 #   job_id INTEGER PRIMARY KEY AUTOINCREMENT,
  #  user_id INTEGER,
   # job_title TEXT,
   # required_major TEXT,
    #min_gpa REAL,
#    skills TEXT,
 #   working_hours INTEGER,
  #  job_duration TEXT,
  #  positions_available INTEGER,
   # FOREIGN KEY (user_id) REFERENCES users(id)
#)
#""")

cursor.execute("""
CREATE TABLE seekers_form (
    form_id INTEGER PRIMARY KEY AUTOINCREMENT,
    form_submission INTEGER,
    user_id INTEGER,
    name TEXT,
    phoneNumber TEXT,
    major TEXT,
    gpa REAL,
    skills TEXT,
    experience TEXT,
    languages TEXT,
    sunday_periods INTEGER,
    sunday_start_interval TEXT,
    sunday_end_interval TEXT,
    monday_periods INTEGER,
    monday_start_interval TEXT,
    monday_end_interval TEXT,
    tuesdayـperiods INTEGER,
    tuesday_start_interval TEXT,
    tuesday_end_interval TEXT,
    wednesday_periods INTEGER,
    wednesday_start_interval TEXT,
    wednesday_end_interval TEXT,
    thursday_periods INTEGER,
    thursday_start_interval TEXT,
    thursday_end_interval TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id)
)
""")

cursor.execute("""
CREATE TABLE files (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    data BLOB,
    FOREIGN KEY (user_id) REFERENCES users(id)
)
""")

connection.commit()
