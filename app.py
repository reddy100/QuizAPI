from flask import Flask, render_template, request, redirect, url_for, flash, make_response, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from datetime import datetime, timedelta
from random import shuffle
import uuid

time_per_Session = 1

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/abishek/Code/QuizAPI/database.db'
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = '09134832084uriehfdsh!'
app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(minutes=time_per_Session)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = '/'

original_questions = {
1: ['What is my first name',['abishek', 'reddy' , 'wdaru']],
2: ['What is my doges name',['otto','nitro','pomodoro']],
3: ['What is my favoraite food',['chocolate','yes its chocolate','why are you still asking']]
}
questionIds=list(range(1, len(original_questions)+1))
shuffle(questionIds)

class UserTable(UserMixin, db.Model):
	id = db.Column(db.Integer, nullable=False, primary_key = True)
	firstname = db.Column(db.String(80))
	lastname = db.Column(db.String(80))
	email = db.Column(db.String(80))
	instance_id = db.Column(db.String(80), unique=True)
	answer1 = db.Column(db.Integer)
	answer2 = db.Column(db.Integer)
	answer3 = db.Column(db.Integer)

@login_manager.user_loader
def load_user(user_id):
    return UserTable.query.get(int(user_id))

@app.route('/')
def homePage():
	if 'loggedIn' in session:
		return redirect(url_for('questions', instance_id=current_user.instance_id))
	return render_template('login.html')

@app.route('/login', methods = ['GET','POST'])
def login():
	if request.form.get('email') and request.form.get('firstname') and request.form.get('lastname'): 
		email = request.form.get('email')
		fName = request.form.get('firstname')
		lName = request.form.get('lastname')
		instance_id = str(uuid.uuid4())
		new_user =  UserTable(firstname=fName, lastname=lName, email=email, instance_id=instance_id)
		db.session.add(new_user)
		db.session.commit()
		session['loggedIn'] = True
		login_user(new_user)

		return redirect(url_for('questions', instance_id=instance_id))
	else:
		return redirect(url_for('homePage'))

@app.route('/questions/<instance_id>', methods = ['GET','POST'])
@login_required
def questions(instance_id):
	#chekc if submit button has been pressed
	if request.method=='POST' and request.form.get('userChoice'):
		setattr(current_user, 'answer'+str(session['lastQuestionId']), request.form.get('userChoice'))
		db.session.commit()
		if len(session['questionIds'])>0:
			session['questionIds'].pop()
			session['questionNumbers'].pop()
	if 'questionIds' not in session:
		session['questionIds'] = questionIds
		session['questionNumbers'] = list(range(len(questionIds),0,-1))
		session.permanent=True
		session['startTime'] = datetime.now()
	localQuestionIds = session.get('questionIds')
	questionNumbers = session.get('questionNumbers')
	if localQuestionIds:
		questionId = localQuestionIds[-1]
		questionNumber = questionNumbers[-1]
		question, options = original_questions.get(questionId)
		session['lastQuestionId']=questionId
		timeElapsed = datetime.now() - session['startTime']
		return render_template('questions.html', n = questionNumber,q = question, o = options, t= timedelta(minutes=time_per_Session) - timeElapsed, i=current_user.instance_id)
	else:
		return redirect(url_for('confirmation'))

@app.route('/confirmation')
def confirmation():
	questions = [original_questions[i][0] for i in questionIds]
	answers = [getattr(current_user, 'answer'+str(j)) for j in questionIds]
	logout_user()
	session['loggedIn']=False
	return jsonify(dict(zip(questions, answers)))

if __name__ == '__main__':
	app.run()