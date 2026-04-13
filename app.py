from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime, timedelta

from utils.scheduler import get_next_review, update_stage
from ai_helper import generate_study_plan

app = Flask(__name__)

def get_db():
    return sqlite3.connect("database.db")

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/add",methods = ['POST'])
def add_task():
    subject = request.form['subject']
    topic = request.form['topic']

    created_at = datetime.now()
    stage = 1
    review_date = datetime.now() + timedelta(days=1)

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO tasks (subject,topic,status,created_at,review_date,stage)
        VALUES (?,?,?,?,?,?)
""",(subject,topic,"pending",created_at,review_date,stage))
    
    conn.commit()
    conn.close()

    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()

    conn.close()

    plan = generate_study_plan(tasks)
    
    return render_template('dashboard.html',tasks=tasks,plan=plan)

@app.route('/complete/<int:id>')
def complete_task(id):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT stage FROM tasks WHERE id = ?",(id,))
    stage = cursor.fetchone()[0]

    new_stage = update_stage(stage)
    next_review = get_next_review(new_stage)

    cursor.execute(""" 
        UPDATE tasks
        SET status = ? , stage = ? , review_date = ?
        WHERE id = ?
""",("Completed",new_stage,next_review,id))
    
    conn.commit()
    conn.close()

    return redirect('/dashboard')

@app.route('/delete/<int:id>')
def delete_task(id):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM tasks WHERE id = ?",(id,))

    conn.commit()
    conn.close()

    return redirect('/dashboard')

if __name__ == '__main__':
    app.run(debug=True)
    


