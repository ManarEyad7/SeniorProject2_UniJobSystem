from flask import Flask, request, redirect , flash, url_for,render_template
import sqlite3
TEMPLATES_AUTO_RELOAD = True

app = Flask(__name__)


app.secret_key = 'random string'

# Defines the fist route for homepage
@app.route('/')
def index():
   return render_template('index.html')

# Defines the secound route for login
@app.route('/login' , methods=['GET','POST'])
def login():
    error = None
    if request.method =='POST':
           
        connection = sqlite3.connect("users_database.db")
        cursor = connection.cursor()

        id = request.form['id']
        password = request.form['password']

        print(id,password)

        query1 = "SELECT id,password FROM users where id='"+id+"' and password= '"+password+"' and position= 'employee'"
        cursor.execute(query1)
        result1 = cursor.fetchall()
          
        query2 = "SELECT id,password FROM users where id='"+id+"' and password= '"+password+"' and position= 'student'"
        cursor.execute(query2)
        result2 = cursor.fetchall()
        #Read
        con = sqlite3.connect("users_database.db")
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        query3 = "select name,email from users where id='"+id+"'"
        cur.execute(query3)
        rows = cur.fetchall()
       

        if len(result1) == 0 and len(result2) == 0:
            print("sorry , incorrect login")
            flash("sorry incorrect login Try again!", 'error')
            return redirect(url_for("login"))         
        elif len(result1) == 1:
            return render_template("employee.html" , rows=rows)
        else:
            return render_template("student.html" ,rows=rows)
                
    return render_template("login.html")

@app.route('/seekforjob')
def seekforjob():
    return render_template('seekforjob.html')

if __name__ == "__main__":
   app.run(debug = True)

@app.route('/post_job')
def post_job():
    return render_template('post_job.html')

if __name__ == "__main__":
   app.run(debug = True)