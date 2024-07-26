# main.py

import os
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import webcolors

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///toDoList.db'
db = SQLAlchemy(app)

class List(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    task_color = db.Column(db.String(250), nullable=False)
    content = db.Column(db.String(250), nullable=False)
    priority = db.Column(db.Integer, nullable=False)
    bucket = db.Column(db.String(250), nullable=False)

def calculate_text_color(background_color):
    try:
        # Convert color name to hex if necessary
        background_color = webcolors.name_to_hex(background_color)
    except ValueError:
        # If it's not a named color, assume it's already a hex color
        pass

    background_color = background_color.lstrip('#')
    r, g, b = int(background_color[0:2], 16), int(background_color[2:4], 16), int(background_color[4:6], 16)
    brightness = (r * 299 + g * 587 + b * 114) / 1000
    return 'black' if brightness > 128 else 'white'

@app.route("/")
def home():
    tasks = List.query.all()
    for task in tasks:
        task.text_color = calculate_text_color(task.task_color)
    return render_template("index.html", tasks=tasks)

@app.route("/addTask", methods=["POST"])
def add_task():
    name = request.form.get("name")
    task_color = request.form.get("task_color")
    content = request.form.get("content")
    priority = request.form.get("priority")
    bucket = request.form.get("bucket")

    new_task = List(name=name, task_color=task_color, content=content, priority=priority, bucket=bucket)
    db.session.add(new_task)
    db.session.commit()

    flash("Task added successfully!", "success")
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)


