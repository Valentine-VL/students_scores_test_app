import os
import csv


def table_exists(cursor, table_name):
    result = cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
    return result.fetchone() is not None


def populate_table_with_data(db):
    db_cursor = db.cursor()
    if not table_exists(db_cursor, 'students'):
        students_query = '''
        CREATE TABLE IF NOT EXISTS main.students (
            `id` INTEGER PRIMARY KEY AUTOINCREMENT,
            `name` VARCHAR(100) UNIQUE NOT NULL
        )
        '''

        class_query = '''
        CREATE TABLE IF NOT EXISTS main.classes (
            `id` INTEGER PRIMARY KEY AUTOINCREMENT,
            `name` VARCHAR(100) UNIQUE NOT NULL
        )
        '''

        students_classes_query = '''
        CREATE TABLE IF NOT EXISTS main.students_classes (
            `id` INTEGER PRIMARY KEY AUTOINCREMENT,
            `student_id` INTEGER NOT NULL,
            `class_id` INTEGER NOT NULL,
            UNIQUE(student_id, class_id),
            FOREIGN KEY (student_id) REFERENCES students(id),
            FOREIGN KEY (class_id) REFERENCES classes(id)
        )
        '''

        scores_query = '''
        CREATE TABLE IF NOT EXISTS main.scores (
           `id` INTEGER PRIMARY KEY AUTOINCREMENT,
            `student_id` INTEGER NOT NULL,
            `year` INT NOT NULL,
            `quarter` VARCAHR(2) NOT NULL,
            `discipline_id` INTEGER NOT NULL,
            `score` INTEGER NOT NULL,
            FOREIGN KEY (student_id) REFERENCES students(id)
            FOREIGN KEY (discipline_id) REFERENCES disciplines(id)
        )
        '''

        disciplines_query = '''
        CREATE TABLE IF NOT EXISTS main.disciplines (
            `id` INTEGER PRIMARY KEY AUTOINCREMENT,
            `name` VARCHAR(100) UNIQUE NOT NULL
        )
        '''
        db_cursor.execute(students_query)
        db_cursor.execute(class_query)
        db_cursor.execute(students_classes_query)
        db_cursor.execute(scores_query)
        db_cursor.execute(disciplines_query)

        insert_disciplines = '''
                       INSERT INTO main.disciplines (`name`)
                       VALUES ('Mathematics'),
                               ('Literature'),
                               ('Computer Science')
                       '''
        db_cursor.execute(insert_disciplines)

        with open('students_data.csv', 'r') as csvfile:
            csvreader = csv.DictReader(csvfile)
            result = db_cursor.execute("SELECT * FROM main.disciplines")
            disciplines = result.fetchall()
            for row in csvreader:
                row.pop("Date Of Birth")
                row.pop("Student ID")
                insert_student = '''
                       INSERT OR IGNORE INTO main.students (`name`)
                       VALUES (?)
                       '''
                student_name = row.get('Student Name')
                db_cursor.execute(insert_student, (student_name,))

                insert_class = '''
                       INSERT OR IGNORE INTO main.classes (`name`)
                       VALUES (?)
                       '''
                class_name = row.get('Student Class')
                db_cursor.execute(insert_class, (class_name,))

                insert_student_class = '''
                       INSERT OR IGNORE INTO main.students_classes (student_id, class_id)
                       SELECT s.id AS student_id, c.id AS class_id
                       FROM students s
                       JOIN classes c ON s.name = ? AND c.name = ?
                       LIMIT 1
                       '''
                db_cursor.execute(insert_student_class, (student_name, class_name))

                for discipline in disciplines:
                    insert_score = '''
                            INSERT INTO main.scores (student_id, year, quarter, score, discipline_id)
                            SELECT sc.id AS student_class_id, ? AS year, ? AS quarter, ? AS score, ? as discipline_id
                            FROM students_classes sc
                            JOIN students s ON s.id = sc.student_id AND s.name = ?
                            LIMIT 1
                            '''
                    db_cursor.execute(insert_score, (row.get('Year'), row.get('Quarter'), row.get(discipline[1]), discipline[0], student_name))

            db.commit()