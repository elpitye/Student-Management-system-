from setup_database import setup_database, hash_password
from attendance_tuition import (
    add_student, view_students, update_student,
    delete_student, record_attendance, view_attendance,
    search_students
)
import sqlite3

def login():
    print("Welcome to the Student Management System")
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    conn = sqlite3.connect('nouvelle_alliance.db')
    cursor = conn.cursor()
    try:
        hashed = hash_password(password)
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hashed))
        user = cursor.fetchone()
        if user:
            print(f"Welcome, {user[1]}! You are logged in as {user[3]}.")
            return user[3]
        else:
            print("Invalid login.")
            return None
    finally:
        conn.close()

def update_user_password(username, new_password, role):
    if role != "admin":
        print("Only admin can update passwords.")
        return
    conn = sqlite3.connect('nouvelle_alliance.db')
    cursor = conn.cursor()
    try:
        hashed = hash_password(new_password)
        cursor.execute("UPDATE users SET password = ? WHERE username = ?", (hashed, username))
        conn.commit()
        print("Password updated.")
    finally:
        conn.close()

def main_menu():
    role = login()
    if not role:
        return

    while True:
        print("\n--- Menu ---")
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
        elif choice == "8" and role == "admin":
            user = input("Enter username: ")
            new_pass = input("Enter new password: ")
            update_user_password(user, new_pass, role)
        elif choice == "9":
            print("Goodbye.")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    setup_database()
    main_menu()
