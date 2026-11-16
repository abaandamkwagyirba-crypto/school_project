from dotenv import load_dotenv
import os

load_dotenv()
from flask import Flask, render_template, request, redirect, session, flash
import mysql.connector
from datetime import date

app = Flask(__name__)

app.secret_key = "my-secrete-key"

db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Blackoff0594600005,,,",
        database="university_db",
        use_pure=True
    )

@app.route("/")
def homehome():
    return render_template("homehome.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username_input = request.form["username"]  
        password_input = request.form["password"]

        cursor = db.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT id, password
            FROM students
            WHERE username = %s AND password = %s
            """,
            [username_input, password_input]
        )

        student = cursor.fetchone()
        
        cursor.close()
        if student and student["password"] == password_input:
            session["student_id"] = student["id"]
            return redirect("/student_dashboard")

        
        else:
            return "Incorrect credentials!"

    return render_template("login.html")




@app.route("/student_dashboard")
def student_dashboard():
    if "student_id" not in session:
        return redirect("/login")

    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT id, first_name, last_name, username, date_of_birth, age
        FROM students
        WHERE id = %s
    """,
    (session["student_id"],)
    ) 

    student = cursor.fetchone()
    cursor.close()

    if students:
        return render_template("student_dashboard.html", student=student)

    return"Your student record could not be found."

    
@app.route("/logout")
def logout():
    session.pop("student_id", None)
    flash("You have been successfully logged out.")
    return redirect("/login")


@app.route("/form")
def form():
    return render_template("form.html")

from flask import flash, redirect, render_template, url_for


@app.route("/submit", methods=["POST"])
def submit():
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    username = request.form["username"]
    date_of_birth = request.form["date_of_birth"]
    password = request.form["password"]

    dob = date.fromisoformat(date_of_birth)
    today = date.today()
    age = today.year - dob.year

    if (today.month, today.day) < (dob.month, dob.day):
        age -= 1

    cursor = db.cursor()

    check_sql = "SELECT username FROM students WHERE username = %s"
    cursor.execute(check_sql, (username,))
    existing_user = cursor.fetchone()

    if existing_user:
        cursor.close()
        flash("This username is already taken. Please choose another one.", "error")
        return redirect(
            url_for("form")
        ) 


    sql = """
    INSERT INTO students 
    (first_name, last_name, username, date_of_birth, age, password)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    cursor.execute(
        sql, (first_name, last_name, username, date_of_birth, age, password)
    )
    db.commit()
    cursor.close()

    flash("Registration successful!", "success")


    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>STUDENT SAVED SUCCESSFULLY</title>

        <style>
            /* Base Page Setup */
            body {{
                background-color: #0c0b4b; /* Sleek dark background matching your system */
                color: #f2f3f5;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                margin: 0;
                min-height: 100vh;
                display: flex;
                justify-content: center; 
                align-items: center;     
            }}

            /* Centered Record Card Panel */
            #card_div {{
                background: ##0c0b4b; /* Card container matching dashboard boxes */
                padding: 2.5rem;
                border-radius: 12px;
                box-shadow: 0 8px 24px rgba(0, 0, 0, 0.25);
                max-width: 440px;
                width: 90%;
                text-align: center;
                border-top: 4px solid #248046; /* Clean creation green accent line */
                animation: fadeIn 0.6s ease-out;
            }}

            /* Heading Styling */
            h2 {{
                color: #ffffff;
                font-size: 1.75rem;
                font-weight: 700;
                letter-spacing: 0.5px;
                margin-top: 0;
                margin-bottom: 1.75rem;
            }}

            /* Registration Meta Row Items Group */
            .data-group {{
                background-color: #1e1f22;
                border: 1px solid #3f4147;
                border-radius: 6px;
                padding: 0.85rem 1rem;
                margin-bottom: 0.75rem;
                display: flex;
                justify-content: space-between;
                align-items: center;
                font-size: 0.95rem;
            }}

            .data-label {{
                color: #b5bac1;
                text-transform: uppercase;
                font-size: 0.8rem;
                font-weight: 600;
                letter-spacing: 0.5px;
            }}

            .data-value {{
                color: #ffffff;
                font-weight: 500;
            }}

            /* Masked Security Tag Styling */
            .password-masked {{
                font-family: monospace;
                letter-spacing: 2px;
                color: #10b981; /* Accent green to confirm capture */
                font-size: 1.1rem;
            }}

            /* Modern Navigation Link CTA Button */
            .back-button {{
                display: block;
                text-decoration: none;
                color: #ffffff;
                background-color: #5865f2; /* Invite user forward using main action blue */
                padding: 0.85rem;
                margin-top: 1.75rem;
                font-size: 1rem;
                font-weight: 600;
                letter-spacing: 0.5px;
                border-radius: 6px;
                transition: all 0.2s ease-in-out;
            }}

            .back-button:hover {{
                background-color: #4752c4;
                transform: translateY(-1px);
                box-shadow: 0 4px 12px rgba(88, 101, 242, 0.2);
            }}

            .back-button:active {{
                transform: translateY(0);
            }}

            /* Smooth Entry Animation */
            @keyframes fadeIn {{
                from {{
                    opacity: 0;
                    transform: translateY(15px);
                }}
                to {{
                    opacity: 1;
                    transform: translateY(0);
                }}
            }}
        </style>
    </head>
    <body>

        <div id="card_div">
            <h2>STUDENT REGISTRATION COMPLETED</h2>

            <div class="data-group">
                <span class="data-label">First Name</span>
                <span class="data-value">{first_name}</span>
            </div>

            <div class="data-group">
                <span class="data-label">Last Name</span>
                <span class="data-value">{last_name}</span>
            </div>

            <div class="data-group">
                <span class="data-label">Date of Birth</span>
                <span class="data-value">{date_of_birth}</span>
            </div>

            <div class="data-group">
                <span class="data-label">Calculated Age</span>
                <span class="data-value">{age} years old</span>
            </div>

            <div class="data-group">
                <span class="data-label">Security Credentials</span>
                <!-- Displays bullet indicators to preserve security interface looks -->
                <span class="data-value password-masked">••••••••</span>
            </div>

            <a class="back-button" href="/login">
                Back To Login Page
            </a>
        </div>

    </body>
    </html>
    """


@app.route("/staff_reg")
def staff_reg():
    return render_template("staff_reg.html")

@app.route("/login_submit", methods=["POST"])
def login_submit():

    role = request.form.get("role")
    username = request.form.get("username")
    password = request.form.get("password")

    cursor = db.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT * FROM account
        WHERE username = %s AND password = %s
        """,
        (username, password)
    )

    account = cursor.fetchone()

    cursor.close()

    print("database row found:", account)

        
    if not account:
        return f"""<!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>STUDENT UPDATED</title>
        
                <style>
                    body {{
                        background-color: #0c0b4b; 
                        color: rgb(185, 37, 11);
                        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                        margin: 0;
                        min-height: 100vh;
                        display: flex;
                        justify-content: center; 
                        align-items: center;     
                    }}
                    h1 {{
                        background: #0c0b4b; 
                        padding: 3rem 2.5rem;
                        border-radius: 12px;
                        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
                        text-align: center;
                        max-width: 400px;
                        width: 90%;
                        animation: fadeIn 1s ease-out;
                    
                    }}
                </style>
                </head>
                <body>
                    <h1>incorrect data</h1>

                    <a href="/staff_reg">Back</a>
                </body>    
                """
    
    db_role = str(account["role"]).strip().upper()
    role_to_check = str(role).strip().upper()

    if db_role != role_to_check:
        return f"""<!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>STUDENT UPDATED</title>
        
                <style>
                    body {{
                        background-color: #0c0b4b; 
                        color: rgb(185, 37, 11);
                        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                        margin: 0;
                        min-height: 100vh;
                        display: flex;
                        justify-content: center; 
                        align-items: center;     
                    }}
                    h1 {{
                        background: #0c0b4b; 
                        padding: 3rem 2.5rem;
                        border-radius: 12px;
                        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
                        text-align: center;
                        max-width: 400px;
                        width: 90%;
                        animation: fadeIn 1s ease-out;
                    
                    }}
                </style>
                </head>
                <body>
                    <h1>incorrect option: form sent '{role}' but database has '{db_role}'</h1>
                    <a href="/staff_reg">Back</a>
                </body>
                """

    
    if db_role == "HEAD TEACHER/PRINCIPAL":
        return render_template("/head_office.html")
    
    elif db_role == "LECTURER":
        return render_template("/lecturer.html")

    elif db_role == "ACCOUNTANT":
        return render_template("/accountant.html")    
        
    
    return f"""<!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>STUDENT UPDATED</title>
        
                <style>
                    body {{
                        background-color: #0c0b4b; 
                        color: rgb(185, 37, 11);
                        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                        margin: 0;
                        min-height: 100vh;
                        display: flex;
                        justify-content: center; 
                        align-items: center;     
                    }}
                    h1 {{
                        background: #0c0b4b; 
                        padding: 3rem 2.5rem;
                        border-radius: 12px;
                        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
                        text-align: center;
                        max-width: 400px;
                        width: 90%;
                        animation: fadeIn 1s ease-out;
                    
                    }}
                </style>
                </head>
                <body>
                    <h1>incorrect option</h1>
                    <a href="/staff_reg">Back</a>
                </body>
                """

@app.route("/students")
def students():
    cursor = db.cursor(dictionary=True)

    query = """
        SELECT
            s.id, s.username, s.first_name, s.last_name, s.date_of_birth, s.age,
            m.subject, m.marks, m.assigned_classroom
        FROM students s
        LEFT JOIN marks m ON s.id = m.student_id
        """  

    cursor.execute(query)

    all_student = cursor.fetchall()
    
    cursor.close()

    return render_template("see.html",
    students=all_student)




@app.route("/search")
def search():
    name = request.args.get("name", "")

    cursor = db.cursor()

    cursor.execute(
        """
        SELECT * FROM students
        WHERE first_name LIKE %s
        OR last_name LIKE %s
        """,
        (f"%{name}%", f"%{name}%")
    )

    students = cursor.fetchall()
    cursor.close()

    return render_template("see.html", students=students)

@app.route("/marks")
def marks():
    return render_template("marks.html")


@app.route("/edit/<int:id>")
def edit(id):
    cursor = db.cursor(dictionary=True)

    query = """
        SELECT
            s.id,                                  -- student[0]
            s.username,                            -- student[1]
            s.first_name,                          -- student[2]
            s.last_name,                           -- student[3]
            s.date_of_birth,                       -- student[4]
            s.age,                                 -- student[5]
            m.subject,                             -- student[6]
            m.marks,                               -- student[7]
            m.assigned_classroom                   -- student[8]
        FROM students s
        LEFT JOIN marks m ON s.id = m.student_id
        WHERE s.id = %s
        """  
    
    cursor.execute(query, (id,))
    
    student_data = cursor.fetchall()
        
    cursor.close()

    if not student_data:
        return redirect("/students")
        

    return render_template("edit.html",
    student=student_data)


@app.route("/delete/<int:id>")
def delete(id):
    cursor = db.cursor()

    cursor.execute(
        "DELETE FROM students WHERE id = %s",
        (id,)
    )

    db.commit()
    cursor.close()

    flash("student updated")
    return redirect("/students")


@app.route("/update/<int:id>", methods=["POST"])
def update(id):
    first_name = request.form.get["first_name"]
    last_name = request.form.get["last_name"]
    username = request.form.get["username"]
    date_of_birth = request.form.get["date_of_birth"]

    subject = request.form.get["subject"]
    marks = request.form.get["marks"]
    assigned_classroom = request.form.get["assigned_classroom"]

    dob = date.fromisoformat(date_of_birth)
    today = date.today()
    age = today.year - dob.year

    if (today.month, today.day) < (dob.month, dob.day):
        age -= 1

    cursor = db.cursor()
    student_query="""
        UPDATE students
        SET first_name = %s,
            last_name = %s,
            username = %s,
            date_of_birth = %s,
            age = %s
        WHERE id = %s
    """,
    cursor.execute(student_query, first_name, last_name, username, date_of_birth, age, id)

    cursor.execute("SELECT id FROM marks WHERE student_id = %s", (id,))
    marks_row_exists = cursor.fetchone()

    if marks_row_exists:
        marks_query = """
            UPDATE marks
            SET subject = %s, marks = %s, assigned_classroom = %s
            WHERE student_id = %s
        """
        cursor.execute(marks_query, (subject, marks, assigned_classroom, id))
    else:
        marks_query = """
            INSERT INTO marks (student_id, subject, marks, assigned_classroom)
            VALUES (%s, %s, %s, %s)
        """

        cursor.execute(marks_query, (id, subject, marks, assigned_classroom))

    db.commit()
    cursor.close()

    flash("STUDENT UPDATED")

    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>STUDENT UPDATED</title>

        <style>
            body {{
                background-color: #1e1f22; /* Sleek dark background matching your system */
                color: #f2f3f5;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                margin: 0;
                min-height: 100vh;
                display: flex;
                justify-content: center; 
                align-items: center;     
            }}
            #card_div {{
                background: #2b2d31; /* Card container matching dashboard boxes */
                padding: 2.5rem;
                border-radius: 12px;
                box-shadow: 0 8px 24px rgba(0, 0, 0, 0.25);
                max-width: 440px;
                width: 90%;
                text-align: center;
                border-top: 4px solid #248046; /* Clean success green accent line */
                animation: fadeIn 0.6s ease-out;
            }}
            h2 {{
                color: #ffffff;
                font-size: 1.75rem;
                font-weight: 700;
                letter-spacing: 0.5px;
                margin-top: 0;
                margin-bottom: 1.75rem;
            }}
            .data-group {{
                background-color: #1e1f22;
                border: 1px solid #3f4147;
                border-radius: 6px;
                padding: 0.85rem 1rem;
                margin-bottom: 0.75rem;
                display: flex;
                justify-content: space-between;
                align-items: center;
                font-size: 0.95rem;
            }}

            .data-label {{
                color: #b5bac1;
                text-transform: uppercase;
                font-size: 0.8rem;
                font-weight: 600;
                letter-spacing: 0.5px;
            }}

            .data-value {{
                color: #ffffff;
                font-weight: 500;
            }}
            .back-button {{
                display: block;
                text-decoration: none;
                color: #ffffff;
                background-color: #4e5058; /* Balanced neutral action background */
                padding: 0.85rem;
                margin-top: 1.75rem;
                font-size: 1rem;
                font-weight: 600;
                letter-spacing: 0.5px;
                border-radius: 6px;
                transition: all 0.2s ease-in-out;
            }}

            .back-button:hover {{
                background-color: #6d6f78;
                transform: translateY(-1px);
            }}

            .back-button:active {{
                transform: translateY(0);
            }}

            @keyframes fadeIn {{
                from {{
                    opacity: 0;
                    transform: translateY(15px);
                }}
                to {{
                    opacity: 1;
                    transform: translateY(0);
                }}
            }}
        </style>
    </head>
    <body>

        <div id="card_div">
            <h2>STUDENT UPDATED</h2>

            <div class="data-group">
                <span class="data-label">First Name</span>
                <span class="data-value">{first_name}</span>
            </div>

            <div class="data-group">
                <span class="data-label">Last Name</span>
                <span class="data-value">{last_name}</span>
            </div>

            
            <div class="data-group">
                <span class="data-label">userame</span>
                <span class="data-value">{username}</span>
            </div>

            <div class="data-group">
                <span class="data-label">Date of Birth</span>
                <span class="data-value">{date_of_birth}</span>
            </div>

            <div class="data-group">
                <span class="data-label">Calculated Age</span>
                <span class="data-value">{age} years old</span>
            </div>

            <a class="back-button" href="/students">
                BACK TO STUDENTS
            </a>
        </div>

    </body>
    </html>
    """

@app.route("/register_account")
def register_account():
    return render_template("register_account.html")

@app.route("/submit_registration", methods=["POST"])
def submit_registration():
    role = request.form.get("role")
    username = request.form.get("username")
    password = request.form.get("password")

    cursor = db.cursor()
    sql = """
        INSERT INTO account 
        (username, password, role)
        VALUES (%s, %s, %s)
        """
    
    cursor.execute(
        sql,
        (username, password, role))
    
    db.commit()
    cursor.close()

    return redirect("/staff_reg")
    


if __name__ == "__main__":
    app.run(debug=True)
