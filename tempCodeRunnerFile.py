
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
    cursor.execute("SELECT major, gpa, skills, totalHours, experience, languages, work_preference,id FROM seekers_form")
    seekers_data = cursor.fetchall()

    cursor.execute("SELECT required_major, min_gpa, skills, working_hours, experience, required_languages,work_location FROM job_posts WHERE job_id = ?", (job_id,))
    job_data = cursor.fetchone()
    job_data = [job_data]

    # Define a dictionary to map experience levels to weights
    experience_weights = {
        'No': 0
    }

    # Assign weights to experience feature values
    filtered_seekers_data2 = []
    for seeker in seekers_data:
        experience = seeker[4]
        weight = experience_weights.get(experience, 1.0)  # Default weight is 1.0 if experience level is not specified in the dictionary
        filtered_seeker = list(seeker[:4]) + [weight] + list(seeker[5:])  # Include the weight in the filtered seeker data
        filtered_seekers_data2.append(filtered_seeker)
   
    # Filter out seekers whose total duration is less than the job's working hours
    filtered_seekers_data = []
    for seeker in filtered_seekers_data2:
        if seeker[3] >= job_data[0][3]:
            filtered_seeker = list(seeker[:3]) + list(seeker[4:]) # Drop the time-related columns from the seeker data
            filtered_seekers_data.append(filtered_seeker)
    print('filtered_seekers_data',len(filtered_seekers_data))


    job_data = [job_data[0][:3] + job_data[0][4:]]    # Drop the time-related columns from the job data
        

    if not filtered_seekers_data:
        message = "No suitable seekers found."
        return render_template('recommendations.html', message=message, job_id=job_id, job_title=job_title , user=user)
    else:
        # Perform recommendation process
        seekers_combined_features = [' '.join(str(item) for item in row) for row in filtered_seekers_data]
        job_combined_features = [' '.join(str(item) for item in job_data)]

        tfidf = TfidfVectorizer(
            sublinear_tf=True,
            use_idf=True,
            smooth_idf=True,
            norm=None,
            lowercase=True,
            stop_words='english',
            token_pattern=r'\b\w+\b',
            max_features=None,
            binary=False,
            decode_error='ignore',
            strip_accents='unicode',
            dtype=np.float32,
            vocabulary=None,
            ngram_range=(1, 1),
            max_df=1.0,
            min_df=1,
            analyzer='word',
            encoding='utf-8')
        seekers_tfidf_matrix = tfidf.fit_transform(seekers_combined_features)
        job_tfidf_matrix = tfidf.transform(job_combined_features)

        # Define the feature weights
        feature_weights = {
            'totalHours': 1.0,
            'skills': 1.0,
            'gpa': 0.7,
            'languages': 0.9,
            'work_preference': 0.9,
            'major': 0.8
        }
        feature_indices = {feature: tfidf.vocabulary_.get(feature) for feature in feature_weights}
        for feature, weight in feature_weights.items():
            feature_index = feature_indices.get(feature)
            if feature_index is not None:
                seekers_tfidf_matrix[:, feature_index] *= weight
                job_tfidf_matrix[:, feature_index] *= weight


        # Compute the cosine similarity
        similarity_scores = cosine_similarity(seekers_tfidf_matrix, job_tfidf_matrix)
        top_seekers = np.argsort(similarity_scores, axis=0)[-9:][::-1].flatten()
        recommended_seekers = []
        
        seekers_data_dict = {seeker[6]: seeker for seeker in filtered_seekers_data}
        seekers_info_dict ={seekers_info[0]: seekers_info for seekers_info in seekers_info}

        for i in top_seekers:
            seeker_id = filtered_seekers_data[i][6]  # Get the seeker ID
            seeker = seekers_data_dict.get(seeker_id)  # Retrieve the seeker information using the seeker ID
            score = similarity_scores[i][0]  # Get the similarity score for the seeker
            score = score * 100
            info = seekers_info_dict.get(seeker_id)
            recommended_seekers.append({'seeker': seeker, 'score': score, 'name': info})
            
        cursor.close()
        conn.close()

        return render_template('recommendations.html', recommendations=recommended_seekers, job_id=job_id, job_title=job_title , user=user)

