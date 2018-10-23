# QuizAPI

Do the following checklist:

1. Run pip install -r requirements.txt

2. Run sqlite3 database.db

3. Run python create_db.py

4. Change SQLALCHEMY_DATABASE_URI config in app.py to point to above created database location in local

5. Run python app.py

Inorder to create new questions:

1. Add questions and answers to original_questions dictionary like below:
	new_entry = {question_id:[question, [option1, option2, option3]]}

2. Add new columns to UserTable db
