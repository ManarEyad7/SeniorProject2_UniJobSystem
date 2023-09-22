from flask import Flask, request, redirect , flash, url_for,render_template, session,abort,jsonify
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import sqlite3
import numpy as np
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

            new_skill = request.form.getlist('n_skills')
            new_skills = ",".join(map(str, new_skill))

            new_job_title = request.form['n_job_title']
            print("***********************************here")
            new_required_major = request.form['n_required_major']
            print("***********************************major")
            new_min_gpa = request.form['n_min_gpa']
            print("***********************************gpa")
            new_skills = new_skills
            print("***********************************skills")
            new_working_hours = request.form['n_working_hours']
            new_job_duration = request.form['n_job_duration']
            new_positions_available = request.form['n_positions_available']

            cursor.execute("UPDATE job_posts SET job_title = '{}', required_major = '{}', min_gpa = '{}' , skills = '{}', working_hours= '{}', job_duration = '{}' , positions_available = '{}' WHERE job_id = '{}' ".format(new_job_title,new_required_major,new_min_gpa,new_skills,new_working_hours,new_job_duration,new_positions_available,id))
            #cursor.execute("UPDATE job_posts SET job_title = '{}', required_major = '{}', min_gpa = '{}' , working_hours= '{}', job_duration = '{}' , positions_available = '{}' WHERE job_id = '{}' ".format(new_job_title,new_required_major,new_min_gpa,new_working_hours,new_job_duration,new_positions_available,id))
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
            form_submission = True
            #--------------------------- Start interval data
        
            # Get the sunday interval data from the form
            sundayStarts = []
            sundayEnds = []
            sunday_periods = int(request.form.get('sunday-interval2'))
            for i in range(sunday_periods):
                print("i== ",i)
                start_time = request.form.get('sunday-interval2-start-time-' + str(i))
                end_time = request.form.get('sunday-interval2-end-time-' + str(i))
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
                thursdayStarts.append(start_time)
                thursdayEnds.append(end_time)
        
            #--------------------------- End interval data


            cursor.execute("UPDATE seekers_form SET  name = '{}', phoneNumber = '{}', languages = '{}', skills = '{}', gpa = '{}', major = '{}', experience = '{}',sunday_periods = '{}',monday_periods = '{}',tuesdayـperiods = '{}',wednesday_periods = '{}',thursday_periods= '{}',sunday_start_interval = '{}',sunday_end_interval = '{}',monday_start_interval = '{}',monday_end_interval = '{}',tuesday_start_interval = '{}',tuesday_end_interval = '{}',wednesday_start_interval = '{}',wednesday_end_interval = '{}',thursday_start_interval = '{}',thursday_end_interval = '{}' WHERE id = '{}'".format 
                       (new_name, new_phoneNumber, new_Languages , new_skills, new_gpa, new_major, new_experience,sunday_periods,monday_periods,tuesdayـperiods,wednesday_periods,thursday_periods,','.join(map(str, sundayStarts)),','.join(map(str, sundayEnds)),','.join(map(str, mondayStarts)),','.join(map(str, mondayEnds)),','.join(map(str, tuesdayStarts)),','.join(map(str, tuesdayEnds)),','.join(map(str, wednesdayStarts)),','.join(map(str, wednesdayEnds)),','.join(map(str, thursdayStarts)),','.join(map(str, thursdayEnds)),id ))
        
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

        return render_template('update_find_job.html', user=user , form = form)

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
''' 


# Route for recommending seekers for a specific job
@app.route('/recommend/<int:job_id>', methods=['GET'])
def recommend(job_id):
   # SQLite database connection
    connection = sqlite3.connect('users_database.db')
    cursor = connection.cursor()
    # Fetch job posts and seekers' forms data
    cursor.execute("SELECT required_major, min_gpa, skills FROM job_posts WHERE job_id=?", (job_id,))
    job_posts_data = cursor.fetchall()
    cursor.execute("SELECT major, gpa, skills FROM seekers_form")
    seekers_form_data = cursor.fetchall()
    
    # Preprocess and convert non-numeric features using TF-IDF
    tfidf_vectorizer = TfidfVectorizer()
    job_skills_numeric = tfidf_vectorizer.fit_transform(job_posts_data[0][2].split(','))
    seeker_skills_numeric = tfidf_vectorizer.transform(seekers_form_data[0][2].split(','))
    job_required_major_numeric = tfidf_vectorizer.transform(job_posts_data[0][0].split(','))
    seeker_major_numeric = tfidf_vectorizer.transform(seekers_form_data[0][0].split(','))


     Ensure the job and seeker arrays have the same number of rows
    num_job_samples = job_skills_numeric.shape[0]
    num_seeker_samples = seeker_skills_numeric.shape[0]

    if num_job_samples < num_seeker_samples:
        seeker_skills_numeric = seeker_skills_numeric[:num_job_samples]
        seeker_major_numeric = seeker_major_numeric[:num_job_samples]
    elif num_job_samples > num_seeker_samples:
        job_skills_numeric = job_skills_numeric[:num_seeker_samples]
        job_required_major_numeric = job_required_major_numeric[:num_seeker_samples]
    
    # Combine numerical and converted features
    job_features = np.column_stack((job_posts_data[0][1], job_skills_numeric.toarray(), job_required_major_numeric.toarray()))
    seeker_features = np.column_stack((seekers_form_data[0][1], seeker_skills_numeric.toarray(), seeker_major_numeric.toarray()))

    # Calculate similarity scores
    similarity_scores = cosine_similarity(job_features, seeker_features)

    # Recommendation function
    def recommend_seekers_for_job(job_id):
        num_jobs = len(similarity_scores)
        if job_id < 1 or job_id > num_jobs:
            return []  # Return an empty list for invalid job IDs

        job_index = job_id - 1
        similarities = similarity_scores[job_index]
        recommended_seekers_indices = np.argsort(similarities)[::-1][:5]  # Top 5 recommendations
        recommended_seekers = [seekers_form_data[i] for i in recommended_seekers_indices]
        return recommended_seekers

    recommendations = recommend_seekers_for_job(job_id)
    print('***********************************')
    return render_template('recommendations.html', recommendations=recommendations)

def compute_similarity(job_post_data, seekers_form_data):
    # Implement your similarity measure logic here
    # Calculate the similarity score between the job post and each seeker's form
    # Return a similarity score array

    # For demonstration purposes, let's assume a simple similarity score based on exact match of skills and major
    skill_similarity = [len(set(job_post_data[2].split()).intersection(set(seeker_form[2].split()))) / len(set(job_post_data[2].split() + seeker_form[2].split())) for seeker_form in seekers_form_data]
    major_similarity = [1 if job_post_data[0] == seeker_form[0] else 0 for seeker_form in seekers_form_data]

    # Combine the similarity scores using weights if needed
    similarity_scores = (0.7 * np.array(skill_similarity)) + (0.3 * np.array(major_similarity))
    return similarity_scores

    ------------------------   recommendetion system trying   ------------------------    
'''
if __name__ == "__main__":
   app.run(debug = True)

