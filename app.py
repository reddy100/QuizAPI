from flask import Flask, render_template, url_for, request, redirect,session
from random import shuffle
from datetime import datetime, timedelta



app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

original_questions = {
1: ['What is my first name',['abishek', 'reddy' , 'wdaru']],
2: ['What is my doges name',['otto','nitro','pomodoro']],
3: ['What is my favoraite food',['chocolate','yes its chocolate','why are you still asking']]
}
questionIds=list(range(1, len(original_questions)+1))
shuffle(questionIds)

@app.route('/')
def homePage():
	return render_template('login.html')

@app.route('/login', methods = ['GET','POST'])
def login():
	if request.form.get('email') and request.form.get('firstname') and request.form.get('lastname'):
		email = request.form.get('email')
		fName = request.form.get('firstname')
		lName = request.form.get('lastname')
		return redirect(url_for('questions'))
	else:
		return redirect(url_for('login'))

@app.route('/questions', methods = ['GET','POST'])
def questions():
	if 'questionIds' not in session:
		session['questionIds'] = questionIds
		session['questionNumbers'] = list(range(len(questionIds),0,-1))

		#session.permanent=True
		session['startTime'] = datetime.now()
	localQuestionIds = session.get('questionIds')
	questionNumbers = session.get('questionNumbers')
	if localQuestionIds:
		questionId = localQuestionIds[-1]
		questionNumber = questionNumbers[-1]
		question, options = original_questions.get(questionId)
		session['lastQuestionId']=questionNumber
	
		timeElapsed = datetime.now() - session['startTime']
		return render_template('questions.html', n = questionNumber,q = question, o = options, t= timedelta(minutes=60) - timeElapsed)
	else:
		return '<h1>DONE</h1>'


if __name__ == '__main__':
	app.run(debug=False)