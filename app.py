from flask import Flask, request, redirect , flash, url_for,render_template, session,abort

import sqlite3
TEMPLATES_AUTO_RELOAD = True

app = Flask(__name__)
app.secret_key = 'random string'


# Defines the fist route for homepage
@app.route('/')
def index():
   return render_template('index.html')

# Defines the secound route for login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        connection = sqlite3.connect("users_database.db")
        cursor = connection.cursor()
        
        user_id = request.form['id']
        password = request.form['password']

        cursor.execute("SELECT id, password, position, name, email FROM users WHERE id = ? AND password = ?", (user_id, password))
        user = cursor.fetchone()
        
        if user:
            session['user_id'] = user[0] # Save user_id in session
            if user[2] == 'employee':
                return redirect(url_for("employee"))
            elif user[2] == 'student':
                return redirect(url_for('student'))  # Redirect to the student route
            else:
                flash("Position not recognized. Please try again.", 'error')
        else:
            flash("Sorry, incorrect login. Try again!", 'error')
            return render_template("login.html")
        
        connection.close()

    return render_template("login.html")


@app.route('/find_job',methods=['GET', 'POST'])
def find_job():
    if 'user_id' not in session:
        flash("You are not logged in. Please log in first.", 'error')
        return redirect(url_for("login"))

    user_id = session['user_id']

    connection = sqlite3.connect("users_database.db")
    cursor = connection.cursor()
    
    if request.method == 'POST':

        name = request.form['name']
        phoneNumber = request.form['phoneNumber']
        languages = request.form.getlist('Languages')
        skills = request.form.getlist('skills')
        gpa = request.form['gpa']
        major = request.form['major']
        experience = request.form['experience']
        form_submission = True
        #--------------------------- Start interval data
        
        # Get the sunday interval data from the form
        sundayStarts = []
        sundayEnds = []
        sunday_periods = int(request.form.get('sunday-interval'))
        for i in range(sunday_periods):
            print("i== ",i)
            start_time = request.form.get('sunday-interval-start-time-' + str(i))
            end_time = request.form.get('sunday-interval-end-time-' + str(i))
            sundayStarts.append(start_time)
            sundayEnds.append(end_time)

        # Get the monday interval data from the form
        mondayStarts = []
        mondayEnds = []
        monday_periods = int(request.form.get('monday-interval'))
        for i in range(monday_periods):
            print("i== ",i)
            start_time = request.form.get('monday-interval-start-time-' + str(i))
            end_time = request.form.get('monday-interval-end-time-' + str(i))
            mondayStarts.append(start_time)
            mondayEnds.append(end_time)

        # Get the tuesday interval data from the form
        tuesdayStarts = []
        tuesdayEnds = []
        tuesdayـperiods = int(request.form.get('tuesday-interval'))
        for i in range(tuesdayـperiods):
            print("i== ",i)
            start_time = request.form.get('tuesday-interval-start-time-' + str(i))
            end_time = request.form.get('tuesday-interval-end-time-' + str(i))
            tuesdayStarts.append(start_time)
            tuesdayEnds.append(end_time)

        # Get the wednesday interval data from the form
        wednesdayStarts = []
        wednesdayEnds = []
        wednesday_periods = int(request.form.get('wednesday-interval'))
        for i in range(wednesday_periods):
            print("i== ",i)
            start_time = request.form.get('wednesday-interval-start-time-' + str(i))
            end_time = request.form.get('wednesday-interval-end-time-' + str(i))
            wednesdayStarts.append(start_time)
            wednesdayEnds.append(end_time)

        # Get the thursday interval data from the form
        thursdayStarts = []
        thursdayEnds = []
        thursday_periods = int(request.form.get('thursday-interval'))
        for i in range(thursday_periods):
            print("i== ",i)
            start_time = request.form.get('thursday-interval-start-time-' + str(i))
            end_time = request.form.get('thursday-interval-end-time-' + str(i))
            thursdayStarts.append(start_time)
            thursdayEnds.append(end_time)
        
        #--------------------------- End interval data


        cursor.execute("INSERT INTO seekers_form (user_id, form_submission, name, phoneNumber, languages, skills, gpa, major, experience,sunday_periods,monday_periods,tuesdayـperiods,wednesday_periods,thursday_periods,sunday_start_interval,sunday_end_interval,monday_start_interval,monday_end_interval,tuesday_start_interval,tuesday_end_interval,wednesday_start_interval,wednesday_end_interval,thursday_start_interval,thursday_end_interval) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                    (user_id, form_submission, name, phoneNumber, ','.join(languages), ','.join(skills), gpa, major, experience,sunday_periods,monday_periods,tuesdayـperiods,wednesday_periods,thursday_periods,','.join(map(str, sundayStarts)),','.join(map(str, sundayEnds)),','.join(map(str, mondayStarts)),','.join(map(str, mondayEnds)),','.join(map(str, tuesdayStarts)),','.join(map(str, tuesdayEnds)),','.join(map(str, wednesdayStarts)),','.join(map(str, wednesdayEnds)),','.join(map(str, thursdayStarts)),','.join(map(str, thursdayEnds)) ))
        
        connection.commit()
        connection.close()

        flash("Request was created successfully!", 'success')
        return redirect(url_for("student"))

    cursor.execute("SELECT id, password, position, name, email FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()

    if user:
        return render_template('find_job.html', user=user)
    else:
        flash("User not found. Please log in again.", 'error')
        return redirect(url_for("login"))


if __name__ == "__main__":
   app.run(debug = True)

@app.route('/post_job', methods=['GET', 'POST'])
def post_job():
    if 'user_id' not in session:
        flash("You are not logged in. Please log in first.", 'error')
        return redirect(url_for("login"))

    user_id = session['user_id']

    connection = sqlite3.connect("users_database.db")
    cursor = connection.cursor()
    
    if request.method == 'POST':

        job_title = request.form['job_title']
        print("***********************************")

        required_major = request.form['required_major']
        min_gpa = request.form['min_gpa']
        skills = request.form.getlist('skills')
        working_hours = request.form['working_hours']
        job_duration = request.form['job_duration']
        positions_available = request.form['positions_available']
        print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")

        cursor.execute("INSERT INTO job_posts (user_id, job_title, required_major, min_gpa, skills, working_hours, job_duration, positions_available) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", 
                    (user_id, job_title, required_major, min_gpa, ','.join(skills), working_hours, job_duration, positions_available))
        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        

        connection.commit()
        connection.close()

        flash("Job posted successfully!", 'success')
        print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^6")
        return redirect(url_for("employee"))

    cursor.execute("SELECT id, password, position, name, email FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()

    if user:
        return render_template('post_job.html', user=user)
    else:
        flash("User not found. Please log in again.", 'error')
        return redirect(url_for("login"))

@app.route('/employee')
def employee():
    if 'user_id' in session:
        user_id = session['user_id']
        
        try:
            connection = sqlite3.connect("users_database.db")
            cursor = connection.cursor()

            cursor.execute("SELECT id, password, position, name, email FROM users WHERE id = ?", (user_id,))
            user = cursor.fetchone()

            cursor.execute("SELECT * FROM job_posts WHERE user_id = ?", (user_id,))
            jobs = cursor.fetchall()
            #session['job_id'] = jobs[0]
            connection.close()

            return render_template('employee.html', jobs=jobs, user=user)


        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            flash("An error occurred while fetching the job posts. Please try again.", 'error')
            return redirect(url_for('index'))
    else:
        flash("You are not logged in. Please log in first.", 'error')
        return redirect(url_for("login"))

@app.route('/student')
def student():
    if 'user_id' in session:
        user_id = session['user_id']

        try:
            connection = sqlite3.connect("users_database.db")
            cursor = connection.cursor()

            cursor.execute("SELECT id, password, position, name, email FROM users WHERE id = ?", (user_id,))
            user = cursor.fetchone()

            cursor.execute("SELECT * FROM seekers_form WHERE user_id = ?", (user_id,))
            seekerForms = cursor.fetchall()
            connection.close()

            return render_template('student.html', seekerForms=seekerForms, user=user)


        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            flash("An error occurred while fetching the form. Please try again.", 'error')
            return redirect(url_for('index'))
    else:
        flash("You are not logged in. Please log in first.", 'error')
        return redirect(url_for("login"))
    
@app.route('/studentCancle')
def studentCancle():
    if 'user_id' not in session:
        flash("You are not logged in. Please log in first.", 'error')
        return redirect(url_for("login"))

    user_id = session['user_id']
    connection = sqlite3.connect("users_database.db")
    cursor = connection.cursor()
    cursor.execute("SELECT id, password, position, name, email FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    return render_template('student.html', user=user)


@app.route('/view_form/<id>')
def view_form(id):
    user_id = session['user_id']
    #job_id = session['job_id']
    connection = sqlite3.connect("users_database.db")
    cursor = connection.cursor()

    #cursor.execute("SELECT id, password, position, name, email FROM users WHERE id = ?", (user_id,))
    #user = cursor.fetchone()

    cursor.execute("SELECT * FROM seekers_form WHERE user_id = ? AND id =?", (user_id,id))
    form = cursor.fetchone()
    cursor.execute("SELECT id, password, position, name, email FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    #connection.close()

    return render_template('view_form.html', form=form,user=user)
 
@app.route('/view_jobs/<id>')
def view_jobs(id):
    user_id = session['user_id']
    #job_id = session['job_id']
    connection = sqlite3.connect("users_database.db")
    cursor = connection.cursor()

    #cursor.execute("SELECT id, password, position, name, email FROM users WHERE id = ?", (user_id,))
    #user = cursor.fetchone()

    cursor.execute("SELECT * FROM job_posts WHERE user_id = ? AND job_id =?", (user_id,id))
    jobs = cursor.fetchone()
    cursor.execute("SELECT id, password, position, name, email FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    #connection.close()

    return render_template('view_jobs.html', jobs=jobs,user=user)

@app.route('/update_post_job/<id>' , methods=['GET', 'POST'])
def update_post_job(id):
    
    if 'user_id' not in session:
        flash("You are not logged in. Please log in first.", 'error')
        return redirect(url_for("login"))

    user_id = session['user_id']
    #jobid = id
    connection = sqlite3.connect("users_database.db")
    cursor = connection.cursor()
    
    if request.method == 'POST':
        try:
            new_job_title = request.form['n_job_title']
            print("***********************************here")

            new_required_major = request.form['n_required_major']
            new_min_gpa = request.form['n_min_gpa']
            #new_skills = request.form.getlist('n_skills')
            new_working_hours = request.form['n_working_hours']
            new_job_duration = request.form['n_job_duration']
            new_positions_available = request.form['n_positions_available']

            cursor.execute("UPDATE job_posts SET job_title = '{}', required_major = '{}', min_gpa = '{}' ,working_hours= '{}', job_duration = '{}' , positions_available = '{}' WHERE job_id = '{}' ".format(new_job_title,new_required_major,new_min_gpa,new_working_hours,new_job_duration,new_positions_available,id))
            #cursor.execute("UPDATE job_posts SET job_title = '{}' WHERE job_id = '{}' ".format(new_job_title,id))
            connection.commit()
            connection.close()

            #flash("Job updated successfully!", 'success')
            print("Job updated successfully!")
            print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^6")
            return redirect(url_for("employee"))
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            #flash("An error occurred while fetching the form. Please try again.", 'error')
            #return redirect(url_for('index'))

        
    
    else:
        cursor.execute("SELECT id, password, position, name, email FROM users WHERE id = ?", (user_id,))
        user = cursor.fetchone()

        return render_template('update_post_job.html', user=user)
       


       




@app.route('/delete_form/<id>')
def delete_form(id):
    #user_id = session['user_id']
    #job_id = session['job_id']
    connection = sqlite3.connect("users_database.db")
    cursor = connection.cursor()

    cursor.execute("DELETE FROM seekers_form WHERE id = '{}' ".format(id))
    connection.commit()
    connection.close()

    return redirect(url_for("student"))


@app.route('/delete_jobs/<id>')
def delete_jobs(id):
    #user_id = session['user_id']
    #job_id = session['job_id']
    connection = sqlite3.connect("users_database.db")
    cursor = connection.cursor()

    cursor.execute("DELETE FROM job_posts WHERE job_id = '{}' ".format(id))
    connection.commit()
    connection.close()

    return redirect(url_for("employee"))


if __name__ == "__main__":
   app.run(debug = True)