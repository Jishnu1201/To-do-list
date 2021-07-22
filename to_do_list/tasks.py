import datetime

from flask import Blueprint
from flask import render_template, request, redirect, url_for, jsonify
from flask import g

from . import db

bp = Blueprint("tasks", "tasks", url_prefix="")

def format_date(d):
    if d:
        v = d.strftime("%d/%m/%Y %H:%M")
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
        if(not task or not due ):
            return redirect(url_for("tasks.dashboard"), 302)
        due = due.replace("T", "-")
        due = due.split("-")
        due = due[2] + "/" +  due[1] + "/" +  due[0] + " " + due[3]
        description = request.form.get('description')
        status = "Not completed"
        cursor.execute("INSERT INTO list (task, created, due, description, status) values (?, ?, ?, ?, ?)", (task, created, due, description, status))
        conn.commit()
      
        return redirect(url_for("tasks.dashboard"), 302)
        
@bp.route("/<tid>", methods=["GET", "POST"])
def task_info(tid): 
    conn = db.get_db()
    cursor = conn.cursor()
    cursor.execute("select task, created, due, description, status from list WHERE id = ?", [tid])
    task = cursor.fetchone()
    taskname, created, due, description, status = task
    if status == "Not completed":
        status = None
    data = dict(id = tid,
                taskname = taskname,
                created = created,#format_date(created),
                due = due,#format_date(due),
                description = description, 
                status = status)
    return render_template("taskdetail.html", **data)

@bp.route("/<tid>/edit", methods=["GET", "POST"])
def edit(tid):
    conn = db.get_db()
    cursor = conn.cursor()
    if request.method == "GET":
        cursor.execute("select task, created, due, description, status from list WHERE id = ?", [tid])
        task = cursor.fetchone()
        taskname, created, due, description, status = task
        data = dict(id = tid,
                taskname = taskname,
                created = created,#format_date(created),
                due = due,#format_date(due),
                description = description, 
                status = status)
        return render_template("edittask.html", **data)

    elif request.method == "POST":
        task = request.form.get("task")
        due = request.form.get("due")
        if (due != ""):
            due = due.replace("T", "-")
            due = due.split("-")
            due = due[2] + "/" +  due[1] + "/" +  due[0] + " " + due[3]
        description = request.form.get('description')
        status = "Not completed"
        cursor.execute("UPDATE list SET task = ?, description = ?  WHERE id = ?;",(task, description, tid))
        if due != "":
            cursor.execute("UPDATE list SET due = ? WHERE id = ?;",(due, tid))
        conn.commit()
        return redirect(url_for("tasks.dashboard"), 302)