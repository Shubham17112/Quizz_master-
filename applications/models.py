from .database import db #.database means to look for this file inside the folder you are existing, not in the root folder
#if we import like application.databse then models.py will look to import database from another folder named 'applications' inside the applications folder

from flask import current_app


class User(db.Model): #class named User with the following attributes, and the finctions we make make here will be its methods
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), unique=False, nullable=False)
    type = db.Column(db.String(20), default='general')
    description = db.Column(db.String(300), unique=False, nullable=False)
    fullname = db.Column(db.String(200), unique=False, nullable=False)
    qualifcation = db.Column(db.String(200), unique=False, nullable=False)
    dob = db.Column(db.String(50), unique=False, nullable=False)
    __table_args__ = {'extend_existing': True}

    #relationships
    scores = db.relationship('Score', backref='user', lazy=True, cascade = "all, delete")


# class Admin(db.Model):
#     __tablename__ = 'admin'
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True, nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     __table_args__ = {'extend_existing': True}


class Subject(db.Model):
    __tablename__ = 'subject'  #NOTE: if we don't mention the tablename its by default the name of the class in lowercase
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(300), unique=False, nullable=True)
    # admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))
    # admin = db.relationship('Admin', backref=db.backref('subjects', lazy=True))
    __table_args__ = {'extend_existing': True}

    #relationships
    chapters = db.relationship('Chapter', backref='subject', lazy=True, cascade = "all, delete")


class Chapter(db.Model):
    __tablename__ = 'chapter'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(300), unique=False, nullable=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable = False)
    __table_args__ = {'extend_existing': True}

    #relationships
    quizzes = db.relationship('Quiz', backref='chapter', lazy=True, cascade = "all, delete")

class Quiz(db.Model):
    __tablename__ = 'quiz'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    date_of_quiz = db.Column(db.DateTime, nullable=False)
    #time_duration = db.Column(db.Integer, nullable=False) #in minutes
    time_duration = db.Column(db.Time, nullable=False) #in hh:mm format
    remarks = db.Column(db.String(300), unique=False, nullable=True)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.id'), nullable = False)
    __table_args__ = {'extend_existing': True}

    #relationships
    questions = db.relationship('Question', backref='quiz', lazy=True, cascade = "all, delete-orphan")
    scores = db.relationship('Score', backref='quiz', lazy=True, cascade = "all, delete")


class Question(db.Model):
    __tablename__ = 'question'
    id = db.Column(db.Integer, primary_key=True)
    question_statement = db.Column(db.String(520), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    option1 = db.Column(db.String(220), nullable=False)
    option2 = db.Column(db.String(220), nullable=False)
    option3 = db.Column(db.String(220), nullable=False)
    option4 = db.Column(db.String(220), nullable=False)
    correct_option = db.Column(db.Integer, nullable=False)
    __table_args__ = {'extend_existing': True}



class Score(db.Model):
    __tablename__ = 'score'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable = False)
    total_scored = db.Column(db.Float, nullable=False)
    time_stamp_of_attempt = db.Column(db.DateTime, nullable=False)
    __table_args__ = {'extend_existing': True}
