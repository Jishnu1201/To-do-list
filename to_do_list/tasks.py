import datetime

from flask import Blueprint
from flask import render_template, request, redirect, url_for, jsonify
from flask import g

from . import db

bp = Blueprint("tasks", "tasks", url_prefix="")

def format_date(d):
    if d:
        v = d.strftime('%Y-%m-%d %H:%M:%S')
        return v
    else:
        return None

@bp.route("/")
def dashboard():
    conn = db.get_db()
    cursor = conn.cursor()
    oby = request.args.get("order_by", "id")  
    order = request.args.get("order", "asc")
    if order == "asc":
        cursor.execute(f"select id, task, created, due, status from list order by {oby}")
    else:
        cursor.execute(f"select id, task, created, due, status from list order by {oby} desc")
    tasks = cursor.fetchall()
    return render_template('index.html', tasks = tasks, order="desc" if order=="asc" else "asc")


@bp.route("/add", methods=["GET", "POST"])
def add():
    conn = db.get_db()
    cursor = conn.cursor()
    if request.method == "GET":
        data = dict(id = "",
                    task = "",
                    created = "",
                    due = "",
                    description = "",
                    status = "")
        return render_template("addtask.html", **data)
    elif request.method == "POST":
        task = request.form.get("task")
        created = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
        due = request.form.get("due")
        due = due.replace("T", "-")
        due = due.split("-")
        due = due[2] + "/" +  due[1] + "/" +  due[0] + " " + due[3]
        description = request.form.get('description')
        status = "Not completed"
        cursor.execute("INSERT INTO list (task, created, due, description, status) values (?, ?, ?, ?, ?)", (task, created, due, description, status))
        conn.commit()
      
        return redirect(url_for("tasks.dashboard"), 302)
        