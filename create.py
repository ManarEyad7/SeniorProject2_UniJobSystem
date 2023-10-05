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

#cursor.execute("""
#CREATE TABLE seekers_form (
 #   form_id INTEGER PRIMARY KEY AUTOINCREMENT,
 #   form_submission INTEGER,
  #  user_id INTEGER,
 #   name TEXT,
 #   phoneNumber TEXT,
 #   major TEXT,
  #  gpa REAL,
 #   skills TEXT,
 #   experience TEXT,
 #   languages TEXT,
 #   sunday_periods INTEGER,
 #   sunday_start_interval TEXT,
 #   sunday_end_interval TEXT,
  #  monday_periods INTEGER,
 #   monday_start_interval TEXT,
 #   monday_end_interval TEXT,
 #   tuesdayـperiods INTEGER,
  #  tuesday_start_interval TEXT,
  #  tuesday_end_interval TEXT,
  #  wednesday_periods INTEGER,
  #  wednesday_start_interval TEXT,
 #  wednesday_end_interval TEXT,
  #  thursday_periods INTEGER,
 #  thursday_start_interval TEXT,
  #  thursday_end_interval TEXT,
  #  FOREIGN KEY (user_id) REFERENCES users(id)
#)""")

#cursor.execute("""
#CREATE TABLE files (
 #   id INTEGER PRIMARY KEY AUTOINCREMENT,
 #   user_id INTEGER,
 #   data BLOB,
 #   FOREIGN KEY (user_id) REFERENCES users(id)
#)
#""")

''' 
import random

# List of Arabic female first names in English
arabic_first_names = [
    "Sara", "Layla", "Fatima", "Aisha", "Zahra",
    "Noura", "Maha", "Samar", "Rana", "Salma",
    "Mariam", "Hala", "Yara", "Lina", "Rania",
    "Amira", "Dina", "Maya", "Hadeel", "Jana",
    "Farah", "Nadia", "Reem", "Joud", "Dalal",
    "Leila", "Noor", "Huda", "Safia", "Amina",
    "Riham", "Dalia", "Rima", "Mona", "Sawsan",
    "Wafa", "Najla", "Ghada", "Maha", "Laila",
    "Hayat", "Zainab", "Asma", "Hanan", "Amani",
    "Nada", "Saida", "Jawaher", "Rawan", "Maram",
    "Abeer", "Samira", "Rasha", "Razan", "Sahar",
    "Fatima", "Warda", "Shaima", "Hind", "Maha",
    "Raneem", "Manar"
    # Add more first names here
]

# List of Arabic female last names in English
arabic_last_names = [
    "Khaled", "Ahmed", "Hassan", "Mohammed", "Ali",
    "Abdullah", "Khalid", "Hassan", "Ahmed", "Mohammed",
    "Ibrahim", "Saleh", "Omar", "Mahmoud", "Hamza",
    "Saad", "Kamal", "Mahmoud", "Ali", "Hassan",
    "Abbas", "Jaber", "Rashid", "Saeed", "Tarabulsi",
    "Salem", "Rahman", "Nasser", "Sharif", "Farouk",
    "Hamid", "Hussein", "Saeed", "Hadi", "Khalifa",
    "Qasim", "Mansour", "Mahdi", "Karim", "Sultan"
    # Add more last names here
]

# Generate 200 records
for i in range(196):
    id = '2040' + str(i + 1).zfill(3)  # Generate unique ID with length 7
    password = ''.join(random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') for _ in range(8))  # Generate a random password
    first_name = random.choice(arabic_first_names)  # Select a random Arabic female first name
    last_name = random.choice(arabic_last_names)  # Select a random Arabic female last name
    name = first_name + " " + last_name  # Combine the first name and last name
    email = id + "@uj.edu.sa"  # Generate email based on the ID
    user_type = "student"  # Set the type of user
    
    query = "INSERT INTO users VALUES ('{}', '{}', '{}', '{}', '{}')".format(id, password, name, email, user_type)
    cursor.execute(query)
'''

connection.commit()
