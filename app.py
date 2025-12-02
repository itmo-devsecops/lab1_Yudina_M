from flask import Flask, render_template, request, redirect, url_for, jsonify
from database import Base, engine, SessionLocal
from models import Student

app = Flask(__name__)

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
            surname=request.form.get('surname'),
            name=request.form.get('name'),
            patronymic=request.form.get('patronymic'),
            course=int(request.form.get('course', 0)),
            group=request.form.get('group'),
            faculty=request.form.get('faculty')
        )
        db.add(new_student)
        db.commit()
        db.close()
        return redirect(url_for('index'))
    return render_template('add_student.html')


@app.route('/delete/<int:student_id>', methods=['GET'])
def delete_student(student_id):
    db = SessionLocal()
    student = db.query(Student).filter_by(id=student_id).first()
    if student:
        db.delete(student)
        db.commit()
    db.close()
    return redirect(url_for('index'))


@app.route("/healthcheck")
def healthcheck():
    return jsonify({"status": "ok"}), 200