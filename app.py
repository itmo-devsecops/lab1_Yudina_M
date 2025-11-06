from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy.orm import Session
from database import Base, engine, SessionLocal
from models import Student

app = Flask(__name__)

# Создаём таблицу, если вдруг её нет
Base.metadata.create_all(bind=engine)

@app.route('/')
def index():
    db = SessionLocal()
    students = db.query(Student).all()
    db.close()
    return render_template('index.html', students=students)

@app.route('/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        db = SessionLocal()
        new_student = Student(
            surname=request.form['surname'],
            name=request.form['name'],
            patronymic=request.form['patronymic'],
            course=int(request.form['course']),
            group=request.form['group'],
            faculty=request.form['faculty']
        )
        db.add(new_student)
        db.commit()
        db.close()
        return redirect(url_for('index'))
    return render_template('add_student.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

