import sqlite3
import hashlib

def hash_password(password):
    """Hash a password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()


import sqlite3
import hashlib

# Hash the password using SHA-256
def hash_password(password):
    """Hash a password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def setup_database():
    conn = sqlite3.connect('nouvelle_alliance.db')
    cursor = conn.cursor()

    # Create the users table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL CHECK(role IN ('admin', 'professor'))
    )
    ''')

    # Create the students table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        grade TEXT NOT NULL
    )
    ''')

    # Create the attendance table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS attendance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER NOT NULL,
        date TEXT NOT NULL,
        status TEXT NOT NULL
    )
    ''')

    conn.commit()
    conn.close()

def login():
    print("Welcome to the Student Management System")
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    conn = sqlite3.connect('nouvelle_alliance.db')
    cursor = conn.cursor()

    try:
        # Hash the entered password and check if it matches the stored password
        hashed_password = hash_password(password)
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hashed_password))
        user = cursor.fetchone()

        if user:
            print(f"Welcome, {user[1]}! You are logged in as {user[3]}.")
            return user[3]  # Return the role (admin or professor)
        else:
            print("Invalid username or password.")
            return None  # Invalid login

    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

def update_user_password(username, new_password, logged_in_role):
    if logged_in_role != "admin":
        print("You do not have permission to update another user's password.")
        return 
    
    conn = sqlite3.connect('nouvelle_alliance.db')
    cursor = conn.cursor()

    try:
        hashed_new_password = hash_password(new_password)
        cursor.execute("UPDATE users SET password = ? WHERE username = ?", (hashed_new_password, username))
        conn.commit()
        print(f"Password for {username} updated successfully.")
    except Exception as e:
        print(f"Error: Unable to update password. ({e})")
    finally:
        conn.close()

def main_menu():
    # Call the login function first
    role = login()

    if role == "admin":
        print("Admin options: You can add, update, delete students, etc.")
        print("Admin: You can update professor's passwords.")
    elif role == "professor":
        print("Professor options: You can record attendance and view students.")

    # Continue to show the menu only after successful login
    while True:
        print("\n--- Student Management Menu ---")
        print("1. Add Student")
        print("2. View All Students")
        print("3. Update Student Info")
        print("4. Delete Student")
        print("5. Record Attendance")
        print("6. View Attendance")
        print("7. Search Students")
        print("8. Update Professor Password (Admin only)")
        print("9. Exit")

        choice = input("Enter your choice: ")
        if choice == "1":
            add_student()
        elif choice == "2":
            view_students()
        elif choice == "3":
            update_student()
        elif choice == "4":
            delete_student()
        elif choice == "5":
            record_attendance()
        elif choice == "6":
            view_attendance()
        elif choice == "7":
            search_students()
        elif choice == "8" and role == "admin":  # Only allow admins to update password
            username = input("Enter the username of the professor: ")
            new_password = input("Enter the new password: ")
            update_user_password(username, new_password, role)
        elif choice == "9":
            print("Au revoir")
            break
        else:
            print("Invalid choice, try again.")

# new student space 
def add_student():
    name = input("Enter the student's name: ")
    grade = input("Enter the student's grade: ")
    
    # check if the name or grade work arent empty 
    if not name or not grade:
        print("Error: Please add te Student name ad grade ")
        return 
    
    try:
        # Attempt to connect to the the database and add the student 
       conn = sqlite3.connect("nouvelle_alliance.db")
       cursor = conn.cursor()
       cursor.execute("INSERT INTO students (name, grade) VALUES (?, ?)", (name, grade))
       conn.commit() # Commit the changes 
       
       # will print this if only th inser is successfuly 
       print("Student added successfully.")
       
    except Exception as e:
        # print the erro is student haven't add 
            print(f"Error: Please add the student's name and grade and  try again. ({e})") 
            
    finally:  
        # To make sure the database connection is always close tho 
            conn.close()

def view_students():
    try:
        conn = sqlite3.connect("nouvelle_alliance.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students")
        students = cursor.fetchall()
        
        if not students: # check if the list is not empty 
           print("No students found. ")
        else:
            print("\nList of all students:")
            for student in students:
                print(f"ID: {student[0]}, Name: {student[1]}, Grade: {student[2]}")
        
    except Exception as e:
           print(f"error: Unable to fetch students from the database.({e})")
           
    finally:
        # to make sure the database close 
        conn.close()


def update_student():
    student_id = input("Enter the student ID to update: ")
    new_name = input("Enter the new name: ")
    new_grade = input("Enter the new grade: ")
    
    try:
        conn = sqlite3.connect("nouvelle_alliance.db")
        cursor = conn.cursor()
        
        # check if the student exist by student_id
        cursor.execute("Select * FROM students WHERE id = ?", (student_id,))
        student = cursor.fetchone()
        
        if student:
            # if the student exists, proced with updating the student
            cursor.execute("UPDATE students SET name = ?, grade = ? WHERE id = ?", (new_name, new_grade, student_id))
            conn.commit()
            print("Student updated successfully. ")
        else:
            print("No student found with that ID.") 
        
    except Exception as e:
        print(f"Error: unable to update in  the database.({e}) ")
    finally:
        conn.close()


def delete_student():
    student_id = input("Enter the student ID to delete: ")
    
    # check if student_id is a valid number 
    if not student_id.isdigit():
        print("Error: Please enter a valid numeric student ID from the list.")
       return
    
    try:
        conn = sqlite3.connect("nouvelle_alliance.db")
        cursor = conn.cursor()
        
        # Check if the student exists before trying 
        cursor.execute("SELECT * FROM students WHERE id = ?", (student_id,))
        student = cursor.fetchone()
        
        if student:
            cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))
            conn.commit()
            print(f"Student with ID {student_id} deleted successfully.")
        else:
            
            print(f"No student found with id {student_id}. Deletion aborted.")
    
    except Exception as e:
        print(f"Error: Unable to delete student. Please try again.({e})")
        
    finally:
        conn.close() # close the connection safely 
        
def record_attendance():
    student_id = input("Enter the student ID: ")
    date = input("Enter the date (YYYY-MM-DD): ")

    try:
        conn = sqlite3.connect("nouvelle_alliance.db")
        cursor = conn.cursor()

        # Check if the student exists by student_id
        cursor.execute("SELECT * FROM students WHERE id = ?", (student_id,))
        student = cursor.fetchone()

        if student:  # If the student exists, proceed with recording attendance
            while True:
                print("\n--- Attendance status Menu ---")
                print("1. Present")
                print("2. Absent")
                print("3. Late")
                print("4. Exit")

                choice = input("Enter the student status: ")

                if choice == "1":
                    status = "Present"
                    cursor.execute("INSERT INTO attendance (student_id, date, status) VALUES (?, ?, ?)", (student_id, date, status))
                    conn.commit()
                    print(f"\nRecorded: ID={student_id}, Date={date}, Status={status}")
                    break

                elif choice == "2":
                    status = "Absent"
                    cursor.execute("INSERT INTO attendance (student_id, date, status) VALUES (?, ?, ?)", (student_id, date, status))
                    conn.commit()
                    print(f"\nRecorded: ID={student_id}, Date={date}, Status={status}")
                    break

                elif choice == "3":
                    status = "Late"
                    cursor.execute("INSERT INTO attendance (student_id, date, status) VALUES (?, ?, ?)", (student_id, date, status))
                    conn.commit()
                    print(f"\nRecorded: ID={student_id}, Date={date}, Status={status}")
                    break

                elif choice == "4":
                    print("Exiting to main menu")
                    break

                else:
                    print("Invalid input, please try again.")
                    continue

        else:  # If no student is found with the entered ID
            print(f"No student found with ID {student_id}.")

    except Exception as e:
        print(f"Error: Unable to record attendance. ({e})")

    finally:
        conn.close()  # Always close the database connection



def view_attendance():
    conn = sqlite3.connect("nouvelle_alliance.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM attendance")
    attendance = cursor.fetchall()
    for record in attendance:
        print(f"ID: {record[0]}, Student ID: {record[1]}, Date: {record[2]}, Status: {record[3]}")
        

    conn.close()
    
def search_students():
    conn = sqlite3.connect("nouvelle_alliance.db")
    cursor = conn.cursor()
    
    # get the user input for the name to search 
    name = input("Enter the name to search: ")
    
    try:
        # Perfom the search using LIKE 
        cursor.execute("SELECT * FROM students WHERE LOWER(name) LIKE LOWER(?)", ('%' + name + '%' ,))
        students = cursor.fetchall()
        
        # if not student are found
        if not students:
            print(f"No students found with under that '{name}'.")
        else:
            print("\nList of students found: ")
            for student in students:
                print(f"ID:{student[0]}, Name:{student[1]}, Grade: {student[2]}")
                
    except Exception as e:
        print(f"Error: Unable to search for sutdents. ({e})")
        
    finally:
        conn.close()
        

if __name__=="__main__":
    setup_database()
    main_menu() 
    
    