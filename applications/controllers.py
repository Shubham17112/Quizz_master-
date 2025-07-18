from flask import Flask,render_template,redirect,request,url_for
from flask import current_app as app #current_app refers to app.py and imports it as alias app
from datetime import datetime
from .models import * #.models since both reside inside the same folder
from sqlalchemy import String

@app.route('/', methods=['GET','POST'])
def home():
    if request.method == 'POST':
        uname = request.form.get('username')
        pwd = request.form.get('password')
        usr = User.query.filter_by(email = uname, password = pwd).first()
        if usr and usr.type == 'admin': #if user exists and is admin
            return render_template('admin_dashboard.html') #redirect to admin dashboard, we don't need to write the whole path as it is automatically looked into the "templates" foler by default as convention
        elif usr and usr.type == 'general': #if user exists and is general
            return render_template('user_dashboard.html')
        else:
            return render_template('login.html', err_msg = "INVALID USER CREDENTIALS") 
    return render_template('login.html', msg = "")

@app.route('/login', methods=['GET','POST'])
def sigin():
    if request.method == 'POST':
        uname = request.form.get('username')
        pwd = request.form.get('password')
        usr = User.query.filter_by(email = uname, password = pwd).first()
        if usr and usr.type == 'admin': #if user exists and is admin
            return redirect(url_for('admin_dashboard'))#redirect to admin dashboard, we don't need to write the whole path as it is automatically looked into the "templates" foler by default as convention
        elif usr and usr.type == 'general': #if user exists and is general
            return redirect(url_for('user_dashboard', name = usr.username))
        else:
            return render_template('login.html', err_msg = "INVALID USER CREDENTIALS") 
    return render_template('login.html', succ_msg = "")

@app.route('/register', methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        uname = request.form.get('username')
        email = request.form.get('email')
        pwd = request.form.get('password')
        full_name = request.form.get('fullname')
        qualification = request.form.get('qualification')
        dob = request.form.get('dob')
        desc = request.form.get('description')
        check_usr = User.query.filter_by(email = email).first()
        if check_usr:
            return render_template('login.html', err_msg = "USER ALREADY EXISTS, TRY LOGGING IN")
        new_usr = User(username = uname, email = email, password = pwd, fullname = full_name, qualifcation = qualification, dob = dob, description = desc)
        db.session.add(new_usr)
        db.session.commit()
        return render_template('login.html', succ_msg = "USER REGISTERED SUCCESSFULLY")
    return render_template('register.html')

@app.route('/logout')


@app.route('/admin_dashboard')
def admin_dashboard():
    subject = Subject.query.all()
    return render_template('admin_dashboard.html', subjects = subject)

@app.route('/new_subject', methods=['GET','POST'])
def add_subject():
    if request.method == 'POST':
        name = request.form.get('name')
        desc = request.form.get('description')
        if name:
            new_sub = Subject(name = name, description = desc)
            db.session.add(new_sub)
            db.session.commit()
            return redirect(url_for('admin_dashboard'))
    return render_template('new_subject.html')


@app.route('/new_chapter/<int:subject_id>', methods=['GET', 'POST'])
def add_chapter(subject_id):
    subject = Subject.query.get(subject_id)
    if request.method == 'POST':
        name = request.form.get('name')
        desc = request.form.get('description')
        new_chap = Chapter(name=name, description=desc, subject_id=subject.id)
        db.session.add(new_chap)
        db.session.commit()
        return redirect(url_for('admin_dashboard'))  # Replace if needed
    return render_template('new_chapter.html', subject=subject)

@app.route('/delete_subject/<int:subject_id>', methods = ["GET"])
def delete_subject(subject_id):
    subject = Subject.query.get(subject_id)
    db.session.delete(subject)
    db.session.commit()
    return redirect(url_for('admin_dashboard'))

@app.route('/delete_chapter/<int:chapter_id>', methods = ["GET"])
def delete_chapter(chapter_id):
    chapter = Chapter.query.get(chapter_id)
    db.session.delete(chapter)
    db.session.commit()
    return redirect(url_for('admin_dashboard'))

@app.route('/edit_subject/<int:subject_id>', methods = ["GET", "POST"])
def edit_subject(subject_id):
    subject = Subject.query.get(subject_id)
    if request.method == 'POST':
        new_name = request.form.get('name')
        new_description = request.form.get('description')
        if new_name and new_description:
            subject.name = new_name
            subject.description = new_description
        elif new_name:
            subject.name = new_name
        elif new_description:
            subject.description = new_description
        else:
            return redirect(url_for('admin_dashboard'))
        db.session.commit()
        return redirect(url_for('admin_dashboard'))
    return render_template('edit_subject.html', subject = subject.id)

@app.route('/edit_chapter/<int:chapter_id>', methods = ["GET", "POST"])
def edit_chapter(chapter_id):
    chapter = Chapter.query.get(chapter_id)
    if request.method == 'POST':
        new_name = request.form.get('name')
        new_description = request.form.get('description')
        if new_name and new_description:
            chapter.name = new_name
            chapter.description = new_description
        elif new_name:
            chapter.name = new_name
        elif new_description:
            chapter.description = new_description
        else:
            return redirect(url_for('admin_dashboard'))
        db.session.commit()
        return redirect(url_for('admin_dashboard'))
    return render_template('edit_chapter.html', subject = chapter.id)

@app.route('/quiz_management')
def quiz_management():
    quizzes = Quiz.query.all()
    return render_template('quiz_management.html', quizzes=quizzes)


from datetime import datetime
@app.route('/new_quiz', methods=['GET', 'POST'])
def new_quiz():
    chapters = Chapter.query.all()

    if request.method == 'POST':
        name = request.form.get('name')
        date_str = request.form.get('date_of_quiz')
        duration = request.form.get('time_duration')
        remarks = request.form.get('remarks')
        chapter_id = request.form.get('chapter_id')

        if not all([name, date_str, duration, chapter_id]):
            return redirect(url_for('new_quiz'))

        try:
            date_of_quiz = datetime.datetime.strptime(date_str, "%Y-%m-%d")
            time_duration = datetime.datetime.strptime(duration, "%H:%M").time()
        except ValueError:
            return redirect(url_for('new_quiz'))

        quiz = Quiz(
            name=name,
            date_of_quiz=date_of_quiz,
            time_duration=time_duration,
            remarks=remarks,
            chapter_id=chapter_id
        )

        db.session.add(quiz)
        db.session.commit()
        return redirect(url_for('quiz_management'))

    return render_template('new_quiz.html', chapters=chapters)

@app.route('/new_question/<int:quiz_id>', methods=['GET', 'POST'])
def add_question(quiz_id):
    quiz = Quiz.query.get(quiz_id)

    if request.method == 'POST':
        question_statement = request.form.get('statement', '').strip()
        opt1 = request.form.get('opt1', '').strip()
        opt2 = request.form.get('opt2', '').strip()
        opt3 = request.form.get('opt3', '').strip()
        opt4 = request.form.get('opt4', '').strip()
        correct = request.form.get('correct', '').strip()

        # Validation: Check if any field is empty
        if not all([question_statement, opt1, opt2, opt3, opt4, correct]):
            return redirect(request.url)

        try:
            correct = int(correct)
            if correct not in [1, 2, 3, 4]:
                return redirect(request.url)
        except ValueError:
            return redirect(request.url)

        # Create and save question
        new_question = Question(
            question_statement=question_statement,
            option1=opt1,
            option2=opt2,
            option3=opt3,
            option4=opt4,
            correct_option=correct,
            quiz_id=quiz.id
        )

        db.session.add(new_question)
        db.session.commit()
        return redirect(url_for('quiz_management'))

    return render_template('new_question.html', quiz=quiz)

@app.route('/delete_quiz/<int:quiz_id>', methods=['GET'])
def delete_quiz(quiz_id):
    quiz = Quiz.query.get(quiz_id)
    db.session.delete(quiz)
    db.session.commit()
    return redirect(url_for('quiz_management'))

@app.route('/delete_question/<int:question_id>', methods=['GET'])
def delete_question(question_id):
    question = Question.query.get_or_404(question_id)
    db.session.delete(question)
    db.session.commit()
    return redirect(url_for('quiz_management'))

@app.route('/edit_quiz/<int:quiz_id>', methods = ["GET", "POST"])
def edit_quiz(quiz_id):
    quiz = Quiz.query.get(quiz_id)
    chapters = Chapter.query.all()

    if request.method == 'POST':
        new_name = request.form.get('name')
        new_doq = datetime.datetime.strptime(request.form['date_of_quiz'], "%Y-%m-%d")
        new_td = datetime.datetime.strptime(request.form['time_duration'], "%H:%M").time()
        new_remarks = request.form.get('remarks')
        new_chap = int(request.form.get('chapter_id'))
        if new_name and new_doq and new_td and new_remarks and new_chap:
            quiz.name = new_name
            quiz.date_of_quiz = new_doq
            quiz.time_duration = new_td
            quiz.remarks = new_remarks
            quiz.chapter_id = new_chap
        else:
            return redirect(url_for('edit_quiz', quiz_id = quiz_id))
        db.session.commit()
        return redirect(url_for('quiz_management'))
    return render_template('edit_quiz.html', quiz = quiz.id, chapters=chapters)

@app.route('/edit_question/<int:question_id>', methods = ["GET", "POST"])
def edit_question(question_id):
    ques = Question.query.get(question_id)
    if request.method == 'POST':
        new_statement = request.form.get('statement')
        new_opt1 = request.form.get('opt1')
        new_opt2 = request.form.get('opt2')
        new_opt3 = request.form.get('opt3')
        new_opt4 = request.form.get('opt4')
        new_correct = request.form.get('correct')
        if new_statement and new_opt1 and new_opt2 and new_opt3 and new_opt4 and new_correct:
            ques.question_statement = new_statement
            ques.option1 = new_opt1
            ques.option2 = new_opt2
            ques.option3 = new_opt3
            ques.option4 = new_opt4
            ques.correct_option = new_correct
        else:
            return redirect(url_for('edit_question', question_id = question_id))
        db.session.commit()
        return redirect(url_for('quiz_management'))
    return render_template('edit_question.html', question = ques)


#USER DASHBOARD ROUTES BELOW:

@app.route('/user_dashboard/<name>')
def user_dashboard(name):
    user = User.query.filter_by(username=name).first()
    quiz_list = Quiz.query.all()
    current_date = datetime.datetime.now()
    return render_template('user_dashboard.html', user = user, quizzes = quiz_list, current_date = current_date)

@app.route('/scores/<name>')
def scores(name):
    user = User.query.filter_by(username=name).first()
    return render_template('scores.html', user = user)

@app.route('/view_quiz/<int:quiz_id>/<name>')
def view_quiz(quiz_id, name):
    user = User.query.filter_by(username=name).first()
    quiz = Quiz.query.get(quiz_id)
    return render_template('view_quiz.html', quiz = quiz, user = user)

import datetime
@app.route('/start_quiz/<int:quiz_id>/<name>', methods=['GET', 'POST'])
def start_quiz(quiz_id, name):
    quiz = Quiz.query.get(quiz_id)
    current_date = datetime.datetime.now()
    questions = quiz.questions
    user = User.query.filter_by(username=name).first()

    if quiz.date_of_quiz < current_date:
        return redirect(url_for('user_dashboard', name=name))
    
    if not questions:
        return redirect(url_for('user_dashboard', name = user.username))

    current_index = int(request.args.get('q', 0))  # get ?q=0, 1, 2...
    score = int(request.args.get('score', 0))      # running score

    if request.method == 'POST':
        selected = int(request.form.get('option'))
        correct = questions[current_index - 1].correct_option  # previously shown question
        if selected == correct:
            score += 1

    if current_index >= len(questions):  # Save score
        user = User.query.filter_by(username=name).first()
        time = datetime.datetime.now()
        final_score = Score(user_id=user.id, quiz_id=quiz.id, total_scored=score, time_stamp_of_attempt=time)
        db.session.add(final_score)
        db.session.commit()
        return render_template('scores.html', score=score, total=len(questions), user = user)

    question = questions[current_index]
    return render_template('start_quiz.html', quiz=quiz, question=question, index=current_index, total=len(questions), score=score, user = user)    

#SUMMARY PAGE:

import matplotlib
matplotlib.use('Agg')  # Use the non-GUI backend before importing pyplot,matplotlib.use('Agg') forces Matplotlib to use a non-GUI backend that renders images in memory instead of trying to open a window.This is necessary when working with Flask because Flask runs in a web environment, not a desktop application.
import matplotlib.pyplot as plt
import os
import io
import base64
from flask import send_file
from collections import defaultdict

@app.route('/summary/<name>')
def summary(name):

    user = User.query.filter_by(username=name).first()

    scores = Score.query.filter_by(user_id=user.id).all()
    if not scores:
        return render_template('summary.html', user=user, message="No quiz data available.")

    # Data processing
    subject_counts = {}
    month_counts = {}
    all_scores = []

    for score in scores:
        subject = score.quiz.chapter.subject.name  # Get subject from the related quiz
        month = score.time_stamp_of_attempt.strftime("%b")  # Extract month (e.g., 'Jan')

        # Count quizzes per subject
        subject_counts[subject] = subject_counts.get(subject, 0) + 1
        # Count quizzes per month
        month_counts[month] = month_counts.get(month, 0) + 1
        # Collect scores for performance stats
        all_scores.append(score.total_scored)

    # Calculate performance stats
    best_score = max(all_scores)
    worst_score = min(all_scores)
    avg_score = round(sum(all_scores) / len(all_scores), 2)

    # --- Generate Subject-wise Quiz Chart ---
    fig1, ax1 = plt.subplots()
    ax1.bar(subject_counts.keys(), subject_counts.values(), color=['blue', 'green', 'red'])
    ax1.set_xlabel("Subjects")
    ax1.set_ylabel("No. of Quizzes")
    ax1.set_title("Subject-wise Number of Quizzes")
    plt.xticks(rotation=45)

    img1 = io.BytesIO()
    plt.savefig(img1, format='png')
    img1.seek(0)
    subject_chart = base64.b64encode(img1.getvalue()).decode('utf8')
    plt.close(fig1)

    # --- Generate Month-wise Quiz Chart ---
    fig2, ax2 = plt.subplots()
    ax2.pie(month_counts.values(), labels=month_counts.keys(), autopct='%1.1f%%', colors=['pink', 'orange', 'purple'])
    ax2.set_title("Month-wise Number of Quizzes Attempted")

    img2 = io.BytesIO()
    plt.savefig(img2, format='png')
    img2.seek(0)
    month_chart = base64.b64encode(img2.getvalue()).decode('utf8')
    plt.close(fig2)

    return render_template('summary.html', 
                           user=user, 
                           subject_chart=subject_chart, 
                           month_chart=month_chart,
                           best_score=best_score,
                           worst_score=worst_score,
                           avg_score=avg_score)


@app.route('/admin_summary')
def admin_summary():

    scores = Score.query.all()

    users = User.query.all()

    subjects = Subject.query.all()

    # Subject-wise top scores
    subject_scores = defaultdict(list)
    for score in scores:
        quiz = Quiz.query.get(score.quiz_id)
        chapter = quiz.chapter if quiz else None
        subject = chapter.subject if chapter else None
        if subject:
            subject_scores[subject.name].append(score.total_scored)

    subject_max_scores = {sub: max(scores) for sub, scores in subject_scores.items()}

    # Create subject-wise performance chart
    plt.figure(figsize=(6, 4))
    plt.bar(subject_max_scores.keys(), subject_max_scores.values(), color=['blue', 'red', 'green', 'yellow'])
    plt.xlabel("Subjects")
    plt.ylabel("Top Scores")
    plt.title("Subject-wise Top Scores")
    
    img_io = io.BytesIO()
    plt.savefig(img_io, format='png')
    img_io.seek(0)
    subject_chart = base64.b64encode(img_io.getvalue()).decode('utf-8')
    plt.close()

    # Subject-wise quiz attempts
    subject_attempts = defaultdict(int)
    for score in scores:
        quiz = Quiz.query.get(score.quiz_id)
        chapter = quiz.chapter if quiz else None
        subject = chapter.subject if chapter else None
        if subject:
            subject_attempts[subject.name] += 1

    # Create subject-wise attempt chart
    plt.figure(figsize=(6, 4))
    plt.pie(subject_attempts.values(), labels=subject_attempts.keys(), autopct='%1.1f%%')
    plt.title("Subject-wise Quiz Attempts")

    img_io = io.BytesIO()
    plt.savefig(img_io, format='png')
    img_io.seek(0)
    attempt_chart = base64.b64encode(img_io.getvalue()).decode('utf-8')
    plt.close()

    # Find most active user (user who attempted the most quizzes)
    user_attempts = defaultdict(int)
    for score in scores:
        user_attempts[score.user_id] += 1

    most_active_user_id = max(user_attempts, key=user_attempts.get, default=None)
    most_attempts = user_attempts[most_active_user_id] if most_active_user_id else 0
    most_active_user = User.query.get(most_active_user_id).fullname if most_active_user_id else "No attempts"

    return render_template('admin_summary.html',
                           subject_chart=subject_chart,
                           attempt_chart=attempt_chart,
                           most_active_user=most_active_user,
                           most_attempts=most_attempts)


#SEARCH FUNTIONALITY:

#USER's SEARCH:
@app.route('/search/<name>', methods=['GET'])
def search_quizzes(name):
    query = request.args.get('query', '').strip()
    chapter = Chapter.query.filter(Chapter.name.like(f"%{query}%")).first()
    chap_id = chapter.id if chapter else None #to avoid attribute error
    user = User.query.filter_by(username=name).first()
    if query:
        quizzes = Quiz.query.filter(
            (Quiz.name.like(f"%{query}%")) | (Quiz.chapter_id == chap_id)
        ).all()
    else:
        quizzes = []
    
    return render_template('search_results.html', quizzes=quizzes, query=query, user=user)


#ADMIN'S Subject Search:
@app.route('/search_admin', methods=['GET'])
def search_admin():
    query = request.args.get('query', '').strip()

    chapter = Chapter.query.filter(Chapter.name.like(f"%{query}%")).first()

    if query:
        subjects = Subject.query.filter(
            (Subject.name.like(f"%{query}%")) | (Subject.chapters.any(Chapter.name.like(f"%{query}%")))
        ).all()
    else:
        subjects = []

    return render_template('search_admin.html', subjects=subjects, query=query)

#Admin's Quiz Search:
@app.route('/search_admin_quiz', methods=['GET'])
def search_admin_quiz():
    query = request.args.get('query', '').strip()

    chapter = Chapter.query.filter(Chapter.name.like(f"%{query}%")).first()
    chap_id = chapter.id if chapter else None  # Avoid AttributeError

    if query:
        quizzes = Quiz.query.filter(
            (Quiz.name.like(f"%{query}%")) |  (Quiz.chapter_id == chap_id)
        ).all()
    else:
        quizzes = []

    return render_template('search_admin_quiz.html', quizzes=quizzes, query=query)
