import sqlite3

def add_student():
    name = input("Enter the student's name: ")
    grade = input("Enter the student's grade: ")

    if not name or not grade:
        print("Error: Please add the Student name and grade.")
        return

    try:
        conn = sqlite3.connect("nouvelle_alliance.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO students (name, grade) VALUES (?, ?)", (name, grade))
        conn.commit()
        print("Student added successfully.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

def view_students():
    try:
        conn = sqlite3.connect("nouvelle_alliance.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students")
        students = cursor.fetchall()

        if not students:
            print("No students found.")
        else:
            print("\nList of all students:")
            for student in students:
                print(f"ID: {student[0]}, Name: {student[1]}, Grade: {student[2]}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

def update_student():
    student_id = input("Enter the student ID to update: ")
    new_name = input("Enter the new name: ")
    new_grade = input("Enter the new grade: ")

    try:
        conn = sqlite3.connect("nouvelle_alliance.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students WHERE id = ?", (student_id,))
        student = cursor.fetchone()

        if student:
            cursor.execute("UPDATE students SET name = ?, grade = ? WHERE id = ?", (new_name, new_grade, student_id))
            conn.commit()
            print("Student updated successfully.")
        else:
            print("No student found with that ID.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

def delete_student():
    student_id = input("Enter the student ID to delete: ")

    if not student_id.isdigit():
        print("Error: Please enter a valid numeric student ID.")
        return

    try:
        conn = sqlite3.connect("nouvelle_alliance.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students WHERE id = ?", (student_id,))
        student = cursor.fetchone()

        if student:
            cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))
            conn.commit()
            print("Student deleted successfully.")
        else:
            print("No student found with that ID.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

def record_attendance():
    student_id = input("Enter the student ID: ")
    date = input("Enter the date (YYYY-MM-DD): ")

    try:
        conn = sqlite3.connect("nouvelle_alliance.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students WHERE id = ?", (student_id,))
        student = cursor.fetchone()

        if student:
            while True:
                print("\n--- Attendance Menu ---")
                print("1. Present")
                print("2. Absent")
                print("3. Late")
                print("4. Exit")

                choice = input("Enter status: ")

                if choice == "4":
                    print("Exiting...")
                    break

                status_map = {"1": "Present", "2": "Absent", "3": "Late"}
                status = status_map.get(choice)

                if status:
                    cursor.execute("INSERT INTO attendance (student_id, date, status) VALUES (?, ?, ?)",
                                   (student_id, date, status))
                    conn.commit()
                    print(f"Recorded: {status}")
                    break
                else:
                    print("Invalid input.")
        else:
            print("Student not found.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

def view_attendance():
    conn = sqlite3.connect("nouvelle_alliance.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM attendance")
    for record in cursor.fetchall():
        print(f"ID: {record[0]}, Student ID: {record[1]}, Date: {record[2]}, Status: {record[3]}")
    conn.close()

def search_students():
    name = input("Enter the name to search: ")
    try:
        conn = sqlite3.connect("nouvelle_alliance.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students WHERE LOWER(name) LIKE LOWER(?)", ('%' + name + '%',))
        results = cursor.fetchall()

        if results:
            for s in results:
                print(f"ID: {s[0]}, Name: {s[1]}, Grade: {s[2]}")
        else:
            print("No students found.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()
