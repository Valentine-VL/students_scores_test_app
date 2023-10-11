import json
from bottle import route, run, template, get, post, request, HTTPError, app
import sqlite3
from db_init import populate_table_with_data
from bottle_cors_plugin import cors_plugin

app = app()
app.install(cors_plugin('*'))


db = sqlite3.connect('students.db')
db_cursor = db.cursor()

populate_table_with_data(db)

def get_from_db_by_query(query, values=()):
    db_cursor.execute(query, values)
    results = db_cursor.fetchall()
    return results

@route('/')
def index(name='Valentyn'):
    return template('<b>Hello {{name}}</b>!', name=name)

# STUDENTS
@get('/students')
def get_all_students():
    results = get_from_db_by_query( "SELECT * FROM main.students")
    columns = [column[0] for column in db_cursor.description]
    data = [dict(zip(columns, row)) for row in results]

    return json.dumps(data)

@post('/students')
def create_student():
    try:
        data = request.json
        student_name = data.get('student_name')

        if not student_name:
            return HTTPError(400, "Invalid input data")

        query = "INSERT INTO students (student_name,) VALUES (?)"
        db_cursor.execute(query, student_name)
        db.commit()

        return json.dumps({'message': 'Student created successfully'})
    except Exception as e:
        return HTTPError(500, str(e))

@get('/students/<id:int>')
def get_student(id):
    query = "SELECT * FROM main.students WHERE id = ?"
    db_cursor.execute(query, (id,))
    row = db_cursor.fetchone()
    if row:
        columns = [column[0] for column in db_cursor.description]
        data = dict(zip(columns, row))
        return json.dumps(data)
    else:
        return HTTPError(404, "Student association not found")

# SCORES
@get('/scores')
def get_all_students_scores():
    query = '''
        SELECT 
        s.name AS student_name, 
        c.name AS class_name,
        sc.year,
        sc.quarter,
        sc.score,
        FROM students_classes sc
        JOIN students s ON sc.student_id = s.id
        JOIN classes c ON sc.class_id = c.id
        '''
    db_cursor.execute(query)
    results = db_cursor.fetchall()

    columns = [column[0] for column in db_cursor.description]
    data = [dict(zip(columns, row)) for row in results]

    return json.dumps(data)

@get('/scores/<id:int>')
def get_student_scores(id):
    query = '''
        SELECT
            d.name,
            s.quarter,
            s.score,
            s.year
        FROM main.scores s 
        INNER JOIN main.disciplines d on s.discipline_id=d.id
        WHERE student_id = ?'''
    db_cursor.execute(query, (id,))
    row = db_cursor.fetchall()
    if row:
        columns = [column[0] for column in db_cursor.description]
        data = dict([zip(columns, _) for _ in row])
        return json.dumps(data)
    else:
        return HTTPError(404, "Student association not found")

@post('/scores')
def insert_score():
    try:
        data = request.json
        student_name = data.get('student_name')

        if not student_name:
            return HTTPError(400, "Invalid input data")

        query = "INSERT INTO students (student_name,) VALUES (?)"
        db_cursor.execute(query, student_name)
        db.commit()

        return json.dumps({'message': 'Student created successfully'})
    except Exception as e:
        return HTTPError(500, str(e))

run(host='0.0.0.0', port=8080)