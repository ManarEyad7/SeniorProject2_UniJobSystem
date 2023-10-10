from flask import Flask, request, redirect , flash, url_for,render_template, session,send_file,jsonify
import sqlite3
from io import BytesIO
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from datetime import datetime, timedelta


#to save pdf file
import os 

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
        work_duration = request.form['work_duration']
        work_preference = request.form['work_preference']
        form_submission = True
        uploaded_file = request.files['pdf_file']    # Get the uploaded file
        print(uploaded_file)

        if  uploaded_file:
            # Save the file to a temporary location
            temp_path = '/tmp/' + uploaded_file.filename
            uploaded_file.save(temp_path)

            # Read the file data as binary
            with open(temp_path, 'rb') as file:
                file_data = file.read()

            # Delete the temporary file
            os.remove(temp_path)

            
        #--------------------------- Start interval data
        
        # Get the sunday interval data from the form
        sundayStarts = []
        sundayEnds = []
        sunday_periods = int(request.form.get('sunday-interval'))
        totalDuration = 0 
        for i in range(sunday_periods):
            #print("i== ",i)
            start_time = request.form.get('sunday-interval-start-time-' + str(i))
            end_time = request.form.get('sunday-interval-end-time-' + str(i))
            duration = calculate_duration(start_time, end_time)
            totalDuration += duration
            print('sunday: ',totalDuration)
            sundayStarts.append(start_time)
            sundayEnds.append(end_time)

        # Get the monday interval data from the form
        mondayStarts = []
        mondayEnds = []
        monday_periods = int(request.form.get('monday-interval'))
        for i in range(monday_periods):
            #print("i== ",i)
            start_time = request.form.get('monday-interval-start-time-' + str(i))
            end_time = request.form.get('monday-interval-end-time-' + str(i))
            duration = calculate_duration(start_time, end_time)
            totalDuration += duration
            print('monday: ',totalDuration)
            mondayStarts.append(start_time)
            mondayEnds.append(end_time)

        # Get the tuesday interval data from the form
        tuesdayStarts = []
        tuesdayEnds = []
        tuesdayـperiods = int(request.form.get('tuesday-interval'))
        for i in range(tuesdayـperiods):
            #print("i== ",i)
            start_time = request.form.get('tuesday-interval-start-time-' + str(i))
            end_time = request.form.get('tuesday-interval-end-time-' + str(i))
            duration = calculate_duration(start_time, end_time)
            totalDuration += duration
            print('tuesday: ',totalDuration)
            tuesdayStarts.append(start_time)
            tuesdayEnds.append(end_time)

        # Get the wednesday interval data from the form
        wednesdayStarts = []
        wednesdayEnds = []
        wednesday_periods = int(request.form.get('wednesday-interval'))
        for i in range(wednesday_periods):
            #print("i== ",i)
            start_time = request.form.get('wednesday-interval-start-time-' + str(i))
            end_time = request.form.get('wednesday-interval-end-time-' + str(i))
            duration = calculate_duration(start_time, end_time)
            totalDuration += duration
            print('wednesday: ',totalDuration)
            wednesdayStarts.append(start_time)
            wednesdayEnds.append(end_time)

        # Get the thursday interval data from the form
        thursdayStarts = []
        thursdayEnds = []
        thursday_periods = int(request.form.get('thursday-interval'))
        for i in range(thursday_periods):
            #print("i== ",i)
            start_time = request.form.get('thursday-interval-start-time-' + str(i))
            end_time = request.form.get('thursday-interval-end-time-' + str(i))
            duration = calculate_duration(start_time, end_time)
            totalDuration += duration
            print('thursday: ',totalDuration)
            thursdayStarts.append(start_time)
            thursdayEnds.append(end_time)
        
        #--------------------------- End interval data
        print(totalDuration)
        totalHoursDuration = convert_minutes_to_hours(totalDuration)
        cursor.execute("INSERT INTO seekers_form (user_id, form_submission, name, phoneNumber, languages, skills, gpa, major, experience, totalHours, sunday_periods,monday_periods,tuesdayـperiods,wednesday_periods,thursday_periods,sunday_start_interval,sunday_end_interval,monday_start_interval,monday_end_interval,tuesday_start_interval,tuesday_end_interval,wednesday_start_interval,wednesday_end_interval,thursday_start_interval,thursday_end_interval,work_duration,work_preference) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                    (user_id, form_submission, name, phoneNumber, ','.join(languages), ','.join(skills), gpa, major, experience, totalHoursDuration, sunday_periods,monday_periods,tuesdayـperiods,wednesday_periods,thursday_periods,','.join(map(str, sundayStarts)),','.join(map(str, sundayEnds)),','.join(map(str, mondayStarts)),','.join(map(str, mondayEnds)),','.join(map(str, tuesdayStarts)),','.join(map(str, tuesdayEnds)),','.join(map(str, wednesdayStarts)),','.join(map(str, wednesdayEnds)),','.join(map(str, thursdayStarts)),','.join(map(str, thursdayEnds)),work_duration,work_preference ))
        #form_id = cursor.lastrowid

        if  uploaded_file:
            cursor.execute('INSERT INTO files (user_id, filename, data) VALUES (?, ?, ?)',
                    ( user_id,uploaded_file.filename, file_data))

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
    
def calculate_duration(start_time, end_time):
    # Step 1: Convert to 24-hour format
    start_time = convert_to_24_hour(start_time)
    end_time = convert_to_24_hour(end_time)

    # Step 2: Convert to minutes
    start_minutes = convert_to_minutes(start_time)
    end_minutes = convert_to_minutes(end_time)

    # Step 3: Calculate duration
    if end_minutes < start_minutes:
        end_minutes += 24 * 60  # Add 24 hours' worth of minutes

    duration_minutes = end_minutes - start_minutes

    return duration_minutes

def convert_to_24_hour(time_str):
    time_str = time_str.strip()  # Remove leading and trailing spaces
    hour, minute = map(int, time_str[:-3].split(':'))
    am_pm = time_str[-2:].lower()

    if am_pm == 'pm':
        hour += 12

    return f'{hour:02d}:{minute:02d}'

def convert_to_minutes(time_str):
    hour, minute = map(int, time_str.split(':'))
    return hour * 60 + minute

def convert_minutes_to_hours(duration_minutes):
    hours = duration_minutes // 60
    minutes = duration_minutes % 60
    return hours



# Handle file download
@app.route('/download/<int:file_id>')
def download(file_id):
    # Retrieve the file data from the database based on the form_id
    conn = sqlite3.connect('users_database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT filename, data FROM files WHERE file_id = ?', (file_id,))
    file = cursor.fetchone()
    conn.close()

    # Check if the file data exists
    if file is None:
        return 'File not found.'

    filename = file[0]
    file_data = file[1]
    file_obj = BytesIO(file_data)  # Create a file-like object from the file_data
    print(file_obj)

    # Send the file data as a response using send_file
    return send_file(file_obj, download_name=filename, as_attachment=True,mimetype='application/pdf')
    
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
        required_major = request.form['required_major']
        min_gpa = request.form['min_gpa']
        skills = request.form.getlist('skills')
        working_hours = request.form['working_hours']
        experience = request.form['experience']
        job_duration = request.form['job_duration']
        positions_available = request.form['positions_available']
        required_languages = request.form.getlist('required_languages')
        work_location = request.form['work_location']

        cursor.execute("INSERT INTO job_posts (user_id, job_title, required_major, min_gpa, skills, working_hours, experience, job_duration, positions_available, required_languages,work_location) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                    (user_id, job_title, required_major, min_gpa, ','.join(skills), working_hours, experience, job_duration, positions_available, ','.join(required_languages),work_location))
        connection.commit()
        connection.close()
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

    connection = sqlite3.connect("users_database.db")
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM seekers_form WHERE user_id = ? AND id =?", (user_id,id))
    form = cursor.fetchone()
    cursor.execute("SELECT id, password, position, name, email FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    cursor.execute("SELECT file_id,filename, data FROM files WHERE user_id = ?", (user_id,))
    file = cursor.fetchone()
   
    return render_template('view_form.html', form=form,user=user,file=file)
 
@app.route('/view_jobs/<id>')
def view_jobs(id):
    user_id = session['user_id']

    connection = sqlite3.connect("users_database.db")
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM job_posts WHERE user_id = ? AND job_id =?", (user_id,id))
    jobs = cursor.fetchone()
    cursor.execute("SELECT id, password, position, name, email FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()

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

            new_skill = request.form.getlist('n_skills')
            new_skills = ",".join(map(str, new_skill))

            new_job_title = request.form['n_job_title']
            print("***********************************here")
            new_required_languages = request.form.getlist('n_required_languages')
            new_required_languages = ",".join(map(str, new_required_languages))
            new_required_major = request.form['n_required_major']
            print("***********************************major")
            new_min_gpa = request.form['n_min_gpa']
            print("***********************************gpa")
            new_skills = new_skills
            print("***********************************skills")
            new_working_hours = request.form['n_working_hours']
            new_job_duration = request.form['n_job_duration']
            new_positions_available = request.form['n_positions_available']
            new_experience = request.form['n_experience'] 
            new_work_location = request.form['n_work_location'] 

            cursor.execute("UPDATE job_posts SET job_title = '{}', required_major = '{}', min_gpa = '{}' , skills = '{}',working_hours= '{}', job_duration = '{}' , experience = '{}' ,positions_available = '{}' ,required_languages= '{}',work_location='{}' WHERE job_id = '{}' ".format(new_job_title,new_required_major,new_min_gpa,new_skills,new_working_hours,new_job_duration,new_experience,new_positions_available,new_required_languages,new_work_location,id))
            connection.commit()
            connection.close()

            print("Job updated successfully!")
            print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
            return redirect(url_for("employee"))
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
              
    else:
        cursor.execute("SELECT id, password, position, name, email FROM users WHERE id = ?", (user_id,))
        user = cursor.fetchone()

        cursor.execute("SELECT * FROM job_posts WHERE user_id = ? AND job_id =?", (user_id,id))
        jobs = cursor.fetchone()

        return render_template('update_post_job.html', user=user ,jobs=jobs)

@app.route('/update_find_job/<id>' , methods=['GET', 'POST'])
def update_find_job(id):
    
    if 'user_id' not in session:
        flash("You are not logged in. Please log in first.", 'error')
        return redirect(url_for("login"))

    user_id = session['user_id']

    connection = sqlite3.connect("users_database.db")
    cursor = connection.cursor()
    
    if request.method == 'POST':
        
        try:

            new_skill = request.form.getlist('n_skills')
            new_skills = ",".join(map(str, new_skill))

            new_Language = request.form.getlist('n_Languages')
            new_Languages = ",".join(map(str, new_Language))

            new_name = request.form['n_name']
            new_phoneNumber = request.form['n_phoneNumber']
            new_Languages = new_Languages
            new_skills = new_skills
            new_gpa = request.form['n_gpa']
            new_major = request.form['n_major']
            new_experience = request.form['n_experience']
            new_work_duration = request.form['n_work_duration']
            work_preference = request.form['n_work_preference']
            new_uploaded_file = request.files['n_pdf_file']    # Get the uploaded file

            if new_uploaded_file:
                cursor.execute("DELETE FROM files WHERE user_id = '{}' ".format(user_id))

                # Save the file to a temporary location
                new_temp_path = '/tmp/' + new_uploaded_file.filename
                new_uploaded_file.save(new_temp_path)

                # Read the file data as binary
                with open(new_temp_path, 'rb') as file:
                    new_file_data = file.read()

                # Delete the temporary file
                os.remove(new_temp_path)

                cursor.execute('INSERT INTO files (user_id, filename, data) VALUES (?, ?, ?)',
                    ( user_id,new_uploaded_file.filename, new_file_data))

            #--------------------------- Start interval data
        
            # Get the sunday interval data from the form
            sundayStarts = []
            sundayEnds = []
            sunday_periods = int(request.form.get('sunday-interval2'))
            totalDuration = 0 
            for i in range(sunday_periods):
                print("i== ",i)
                start_time = request.form.get('sunday-interval2-start-time-' + str(i))
                end_time = request.form.get('sunday-interval2-end-time-' + str(i))
                duration = calculate_duration(start_time, end_time)
                totalDuration += duration
                sundayStarts.append(start_time)
                sundayEnds.append(end_time)

            # Get the monday interval data from the form
            mondayStarts = []
            mondayEnds = []
            monday_periods = int(request.form.get('monday-interval2'))
            for i in range(monday_periods):
                print("i== ",i)
                start_time = request.form.get('monday-interval2-start-time-' + str(i))
                end_time = request.form.get('monday-interval2-end-time-' + str(i))
                duration = calculate_duration(start_time, end_time)
                totalDuration += duration
                mondayStarts.append(start_time)
                mondayEnds.append(end_time)
  
            # Get the tuesday interval data from the form
            tuesdayStarts = []
            tuesdayEnds = []
            tuesdayـperiods = int(request.form.get('tuesday-interval2'))
            for i in range(tuesdayـperiods):
                print("i== ",i)
                start_time = request.form.get('tuesday-interval2-start-time-' + str(i))
                end_time = request.form.get('tuesday-interval2-end-time-' + str(i))
                duration = calculate_duration(start_time, end_time)
                totalDuration += duration
                tuesdayStarts.append(start_time)
                tuesdayEnds.append(end_time)
            
            # Get the wednesday interval data from the form
            wednesdayStarts = []
            wednesdayEnds = []
            wednesday_periods = int(request.form.get('wednesday-interval2'))
            for i in range(wednesday_periods):
                print("i== ",i)
                start_time = request.form.get('wednesday-interval2-start-time-' + str(i))
                end_time = request.form.get('wednesday-interval2-end-time-' + str(i))
                duration = calculate_duration(start_time, end_time)
                totalDuration += duration
                wednesdayStarts.append(start_time)
                wednesdayEnds.append(end_time)

            # Get the thursday interval data from the form
            thursdayStarts = []
            thursdayEnds = []
            thursday_periods = int(request.form.get('thursday-interval2'))
            for i in range(thursday_periods):
                print("i== ",i)
                start_time = request.form.get('thursday-interval2-start-time-' + str(i))
                end_time = request.form.get('thursday-interval2-end-time-' + str(i))
                duration = calculate_duration(start_time, end_time)
                totalDuration += duration
                thursdayStarts.append(start_time)
                thursdayEnds.append(end_time)
        
            #--------------------------- End interval data
            totalHoursDuration = convert_minutes_to_hours(totalDuration)

            cursor.execute("UPDATE seekers_form SET  name = '{}', phoneNumber = '{}', languages = '{}', skills = '{}', gpa = '{}', major = '{}', experience = '{}',totalHours = '{}',sunday_periods = '{}',monday_periods = '{}',tuesdayـperiods = '{}',wednesday_periods = '{}',thursday_periods= '{}',sunday_start_interval = '{}',sunday_end_interval = '{}',monday_start_interval = '{}',monday_end_interval = '{}',tuesday_start_interval = '{}',tuesday_end_interval = '{}',wednesday_start_interval = '{}',wednesday_end_interval = '{}',thursday_start_interval = '{}',thursday_end_interval = '{}',work_duration = '{}', work_preference = '{}'  WHERE id = '{}'".format 
                       (new_name, new_phoneNumber, new_Languages , new_skills, new_gpa, new_major, new_experience, totalHoursDuration, sunday_periods,monday_periods,tuesdayـperiods,wednesday_periods,thursday_periods,','.join(map(str, sundayStarts)),','.join(map(str, sundayEnds)),','.join(map(str, mondayStarts)),','.join(map(str, mondayEnds)),','.join(map(str, tuesdayStarts)),','.join(map(str, tuesdayEnds)),','.join(map(str, wednesdayStarts)),','.join(map(str, wednesdayEnds)),','.join(map(str, thursdayStarts)),','.join(map(str, thursdayEnds)),new_work_duration,work_preference,id ))
        
            connection.commit()
            connection.close()

            flash("Request was Updated successfully!", 'success')
            return redirect(url_for("student"))
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")    
    else:
        cursor.execute("SELECT id, password, position, name, email FROM users WHERE id = ?", (user_id,))
        user = cursor.fetchone()

        cursor.execute("SELECT * FROM seekers_form WHERE user_id = ? AND id = ?", (user_id,id))
        form = cursor.fetchone()

        cursor.execute("SELECT * FROM files WHERE user_id = ?", (user_id,))
        file = cursor.fetchone()


        return render_template('update_find_job.html', user=user , form = form, file=file)
       
''' 
            new_uploaded_file = request.files['n_pdf_file']    # Get the uploaded file

            # Save the file to a temporary location
            new_temp_path = '/tmp/' + new_uploaded_file.filename
            new_uploaded_file.save(new_temp_path)

            # Read the file data as binary
            with open(new_temp_path, 'rb') as file:
                new_file_data = file.read()

            # Delete the temporary file
            os.remove(new_temp_path)
'''


@app.route('/delete_form/<id>/<user_id>')
def delete_form(id,user_id):
    #user_id = session['user_id']
    #job_id = session['job_id']
    connection = sqlite3.connect("users_database.db")
    cursor = connection.cursor()

    cursor.execute("DELETE FROM seekers_form WHERE id = '{}' ".format(id))
    cursor.execute("DELETE FROM files WHERE user_id = '{}' ".format(user_id))

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

@app.route('/employeeCancle')
def employeeCancle():
    if 'user_id' not in session:
        flash("You are not logged in. Please log in first.", 'error')
        return redirect(url_for("login"))

    user_id = session['user_id']
    connection = sqlite3.connect("users_database.db")
    cursor = connection.cursor()
    cursor.execute("SELECT id, password, position, name, email FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()

    cursor.execute("SELECT * FROM job_posts WHERE user_id = ?", (user_id,))
    jobs = cursor.fetchall()

    return render_template('employee.html', jobs=jobs, user=user)

'''    ------------------------   recommendetion system trying   ------------------------    '''

#def seeker_satisfies_job(seeker, job_data):
    #job_data = [job_data]
    #print(job_data[0][0])
    #print(job_data[0][1])
    #print(job_data[0][2])
    #print(job_data[0][3])
    #print(job_data[0][4])
    #print(job_data[0][5])
    #print(job_data[0][6])

    #required_major = job_data[0][0]
    #min_gpa = job_data[0][1]
    #required_skills = job_data[0][2]
    #working_hours = job_data[0][3]
    #experience_required = job_data[0][4]
    #required_languages = job_data[0][5]
    #work_location = job_data[0][6]

    #seeker_major = seeker[0]
    #seeker_gpa = seeker[1]
    #seeker_skills = seeker[2]
    #seeker_total_hours = seeker[3]
    #seeker_experience = seeker[4]
    #seeker_languages = seeker[5]
    #seeker_work_preference = seeker[6]

    # Check if the seeker's major matches the required major or if the required major is "No Preference"
    #if required_major != 'No Preference' and seeker_major != required_major:
    #    return False

    # Check if the seeker's GPA is greater than or equal to the minimum GPA required
    #if seeker_gpa < min_gpa:
    #    return False

    # Check if the seeker has all the required skills
    #required_skills = set(required_skills.split(','))
    #seeker_skills = set(seeker_skills.split(','))
    #if not required_skills.issubset(seeker_skills):
    #    return False

    # Check if the seeker's total hours are greater than or equal to the working hours required
    #if seeker[3] < job_data[0][3]:
     #   return False

    # Check if the seeker's experience matches the experience requirement or if the requirement is "NO"
    #if experience_required != 'NO' and seeker_experience != experience_required:
    #    return False

    # Check if the seeker knows all the required languages
    #required_languages = set(required_languages.split(','))
    #seeker_languages = set(seeker_languages.split(','))
    #if not required_languages.issubset(seeker_languages):
    #    return False

    # Check if the seeker's work preference matches the work location or if the work location is "No Preference"
    #if work_location != 'No Preference' and seeker_work_preference != work_location:
    #    return False

    # All requirements are satisfied
#   return True

@app.route('/get_recommendations/<int:job_id>')
def get_recommendations(job_id):
    if 'user_id' not in session:
        flash("You are not logged in. Please log in first.", 'error')
        return redirect(url_for("login"))

    user_id = session['user_id']

    # Establish a connection to the SQLite database
    conn = sqlite3.connect('users_database.db')
    cursor = conn.cursor()
    ''' ------------------- Retrieve general data ------------------- '''
    cursor.execute("SELECT * FROM seekers_form")
    seekers_info = cursor.fetchall()

    cursor.execute("SELECT id, password, position, name, email FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    # Retrieve job title
    cursor.execute("SELECT job_title FROM job_posts WHERE job_id = ?", (job_id,))
    job_title = cursor.fetchone()

    ''' ------------------- Retrieve general data ------------------- '''
    # Retrieve data from SQL database
    cursor.execute("SELECT major, gpa, skills, totalHours, experience, languages, work_preference FROM seekers_form")
    seekers_data = cursor.fetchall()

    cursor.execute("SELECT required_major, min_gpa, skills, working_hours, experience, required_languages,work_location FROM job_posts WHERE job_id = ?", (job_id,))
    job_data = cursor.fetchone()
    job_data = [job_data]

    # Define a dictionary to map experience levels to weights
    experience_weights = {
    'No': 0,

    }
    
    # Filter out seekers whose total duration is less than the job's working hours
    filtered_seekers_data1 = []
    #unsatisfied_requirements = []
    for seeker in seekers_data:
        if seeker[3] >= job_data[0][3]:
            filtered_seeker = list(seeker[:3]) + list(seeker[4:]) # Drop the time-related columns from the seeker data
            filtered_seekers_data1.append(filtered_seeker)
        
    # Assign weights to experience feature values
    filtered_seekers_data = []
    for filtered_seekers_data1 in seekers_data:
        experience = filtered_seekers_data1[4]
        weight = experience_weights.get(experience, 1.0)  # Default weight is 1.0 if experience level is not specified in the dictionary
        filtered_seeker = list(filtered_seekers_data1[:4]) + [weight] + list(filtered_seekers_data1[5:])  # Include the weight in the filtered seeker data
        filtered_seekers_data.append(filtered_seeker)

    job_data = [job_data[0][:3] + job_data[0][4:]]    # Drop the time-related columns from the job data


    #print("1",job_data)
    # Check if required_major is set to "No Preference"
    #if job_data[0][0] == 'No Preference':
        # Drop the 'major' column from seekers_data and job_data
        #seekers_data = [seeker[1:3] + seeker[4:] for seeker in seekers_data]
        #job_data = [job_data[0][1:3] + job_data[0][4:]]
    # Function to fetch candidate information from the database


    # Drop the 'experience' column from seekers_data and job_data if job_data['experience'] is 'NO'
    #if job_data[0][4] == 'No':
    #    filtered_seekers_data = [seeker[:3] + seeker[4:] for seeker in filtered_seekers_data]
    #    job_data = [job_data[0][:3] + job_data[0][4:]]
    

    if not filtered_seekers_data:
        message = "No suitable seekers found."
        return render_template('recommendations.html', message=message)
    else:
        # Drop the time-related column from job_data
        #filtered_job_data = job_data[0][:3] + job_data[0][4:]

       
        # Perform recommendation process
        seekers_combined_features = [' '.join(str(item) for item in row) for row in filtered_seekers_data]
        job_combined_features = [' '.join(str(item) for item in job_data)]

        tfidf = TfidfVectorizer()
        seekers_tfidf_matrix = tfidf.fit_transform(seekers_combined_features)
        job_tfidf_matrix = tfidf.transform(job_combined_features)


        similarity_scores = cosine_similarity(seekers_tfidf_matrix, job_tfidf_matrix)
        top_seekers = np.argsort(similarity_scores, axis=0)[-9:][::-1].flatten()

        recommended_seekers = []
        
        for i in top_seekers:
            seeker = seekers_data[i]
            score = similarity_scores[i][0]  # Get the similarity score for the seeker
            info = seekers_info[i]
            recommended_seekers.append({'seeker': seeker, 'score': score, 'name':info})
            
        
        print("dd")
        print(type(recommended_seekers))
        cursor.close()
        conn.close()

        return render_template('recommendations.html', recommendations=recommended_seekers, job_id=job_id, job_title=job_title , user=user)


@app.route('/get_Unstaisfied_recommendations/<int:job_id>')
def get_Unstaisfied_recommendations(job_id):
    if 'user_id' not in session:
        flash("You are not logged in. Please log in first.", 'error')
        return redirect(url_for("login"))

    user_id = session['user_id']

    # Establish a connection to the SQLite database
    conn = sqlite3.connect('users_database.db')
    cursor = conn.cursor()
    ''' ------------------- Retrieve general data ------------------- '''
    cursor.execute("SELECT * FROM seekers_form")
    seekers_info = cursor.fetchall()

    cursor.execute("SELECT id, password, position, name, email FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    # Retrieve job title
    cursor.execute("SELECT job_title FROM job_posts WHERE job_id = ?", (job_id,))
    job_title = cursor.fetchone()

    ''' ------------------- Retrieve general data ------------------- '''
    # Retrieve data from SQL database
    cursor.execute("SELECT major, gpa, skills, totalHours, experience, languages, work_preference FROM seekers_form")
    seekers_data = cursor.fetchall()

    cursor.execute("SELECT required_major, min_gpa, skills, working_hours, experience, required_languages,work_location FROM job_posts WHERE job_id = ?", (job_id,))
    job_data = cursor.fetchone()
    job_data = [job_data]
    
    
    # Filter out seekers whose total duration is less than the job's working hours
    
    unsatisfied_requirements = []
    for seeker in seekers_data:
        if seeker[3] < job_data[0][3]:
            filtered_seeker = list(seeker[:3]) + list(seeker[4:]) # Drop the time-related columns from the seeker data
            unsatisfied_requirements.append(filtered_seeker)
        
    print(unsatisfied_requirements)
    print()

    job_data = [job_data[0][:3] + job_data[0][4:]]    # Drop the time-related columns from the job data

    # Drop the 'experience' column from seekers_data and job_data if job_data['experience'] is 'NO'
    if job_data[0][4] == 'No':
        unsatisfied_requirements = [seeker[:3] + seeker[4:] for seeker in unsatisfied_requirements]
        job_data = [job_data[0][:3] + job_data[0][4:]]
    

    if not unsatisfied_requirements:
        message = "No suitable seekers found."
        return render_template('recommendations2.html', message=message)
    else:
        # Drop the time-related column from job_data
        filtered_job_data = job_data[0][:3] + job_data[0][4:]

        # Perform recommendation process
        seekers_combined_features = [' '.join(str(item) for item in row) for row in unsatisfied_requirements]
        job_combined_features = [' '.join(str(item) for item in filtered_job_data)]

        tfidf = TfidfVectorizer()
        seekers_tfidf_matrix = tfidf.fit_transform(seekers_combined_features)
        job_tfidf_matrix = tfidf.transform(job_combined_features)

        # Update the weight of the experience feature in the job_tfidf_matrix
        experience_index = tfidf.vocabulary_.get('experience')
        if experience_index is not None:
            job_tfidf_matrix[0, experience_index] = 0.5 * job_tfidf_matrix[0, experience_index]

        # Update the weight of the experience feature in the similarity_scores
        experience_weight = 0.5
        similarity_scores = cosine_similarity(seekers_tfidf_matrix, job_tfidf_matrix)
        similarity_scores[:, experience_index] *= experience_weight

        top_seekers = np.argsort(similarity_scores, axis=0)[-9:][::-1].flatten()

        #recommended_seekers = []
        unsatisfied_recommendations = []
        for i in top_seekers:
            seeker = seekers_data[i]
            score = similarity_scores[i][0]  # Get the similarity score for the seeker
            info = seekers_info[i]
            unsatisfied_recommendations.append({'seeker': seeker, 'score': score, 'name':info})
            
    
        print("dd")
        
        cursor.close()
        conn.close()

        return render_template('recommendations2.html', recommendations=unsatisfied_recommendations, job_id=job_id, job_title=job_title , user=user)


def get_candidate_info(candidate_id):
    try:
        conn = sqlite3.connect('users_database.db')
        cursor = conn.cursor()

        # Fetch candidate data
        cursor.execute("SELECT * FROM seekers_form WHERE user_id=?", (candidate_id,))
        candidate_data = cursor.fetchone()

        # Fetch email
        cursor.execute("SELECT email FROM users WHERE id=?", (candidate_id,))
        email = cursor.fetchone()

        # Fetch CV information
        cursor.execute("SELECT file_id, filename, data FROM files WHERE user_id=?", (candidate_id,))
        file = cursor.fetchone()

        if candidate_data:
            return {
                
                            'id': candidate_data[2],
            'name': candidate_data[3],
            'major': candidate_data[5],
            'phone': candidate_data[4],
            'email': email,
            'gpa': candidate_data[6],
            'skills': candidate_data[7],
            'experience': candidate_data[8],
            'languages': candidate_data[9],
            'availability': candidate_data[10],
            'work_preference': candidate_data[27],

                'cv': file[0] if file else None  # Return CV if available, else None
            }
        else:
            return {}  # Return an empty dictionary if no data found
    except sqlite3.Error as e:
        # Handle database errors here
        print("Database error:", str(e))
        return None  # Return None to indicate an error
    finally:
        conn.close()


@app.route('/get_candidate/<int:candidate_id>')
def get_candidate(candidate_id):
    candidate_info = get_candidate_info(candidate_id)
    print(candidate_id)
    if candidate_info:
        return jsonify(candidate_info)
    else:
        return jsonify(error='Candidate not found'), 404
    

@app.route('/get_job_info/<int:id>')
def get_job_info(id):
    try:
        connection = sqlite3.connect("users_database.db")
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM job_posts WHERE job_id = ?", (id,))
        job = cursor.fetchone()
        print(job[5])
        connection.close()

        if job is None:
            abort(404)  # Job not found, return a 404 error

        # Return the job information as JSON
        return jsonify({
            'title': job[2],
            'major': job[3],
            'skills': job[5],
            'gpa' : job[4],
            'working_hours' : job[6],
            'job_duration' : job[7],
            'experience' : job[8],
            'positions_available' : job[9],
            'required_languages' : job[10],
            'work_location' : job[11]

        })
    except Exception as e:
        # Handle database errors or other exceptions
        return str(e)


if __name__ == "__main__":
   app.run(debug = True)

