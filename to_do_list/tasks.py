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

def format_date_back(d):
    date1 = d.replace(" ","/")
    date1 = date1.replace(":","")
    date1 = date1.split("/")
    date1 = date1[2] + date1[1] + date1[0] + date1[3]
    date1 = int(date1)
    return date1


@bp.route("/")
def dashboard():
    conn = db.get_db()
    cursor = conn.cursor()
    oby = request.args.get("order_by", "due")  
    order = request.args.get("order", "asc")
    if order == "asc":
        cursor.execute(f"select id, task, created, due, status from list order by {oby}")
    else:
        cursor.execute(f"select id, task, created, due, status from list order by {oby} desc")
    tasks = cursor.fetchall()
    slno = 1
    datas = []
    for task in tasks:
        overdue = 0
        id, taskname, created, due, status = task
        ldate = format_date_back(due)
        pdate = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
        pdate = format_date_back(pdate)
        if(pdate > ldate):
            overdue = 1
        data = (slno, id ,taskname ,created ,due ,status, overdue )
        datas.append(data)
        slno += 1
    return render_template('index.html', tasks = tuple(datas), order="desc" if order=="asc" else "asc")


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
        status = "Todo"
        cursor.execute("INSERT INTO list (task, created, due, description, status) values (?, ?, ?, ?, ?)", (task, created, due, description, status))
        conn.commit()
      
        return redirect(url_for("tasks.dashboard"), 302)
        
@bp.route("/<tid>/<action>", methods=["GET", "POST"])
def task_info(tid, action): 
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
        return render_template("taskdetail.html", **data)
    
    elif request.method == "POST":
        if action == "Delete":
            cursor.execute("DELETE FROM list WHERE id = ?;", tid)
        else:
            status = "Complete"
            if action == "Todo":
                status = "In Progress"
            elif action == "In Progress":
                status = "Complete"
            else:
                status = "Todo"
            cursor.execute("UPDATE list SET status = ? WHERE id = ?;",(status, tid))
        conn.commit()
        return redirect(url_for("tasks.dashboard"), 302)

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
        status = "Todo"
        cursor.execute("UPDATE list SET task = ?, description = ?  WHERE id = ?;",(task, description, tid))
        if due != "":
            cursor.execute("UPDATE list SET due = ? WHERE id = ?;",(due, tid))
        conn.commit()
        return redirect(url_for("tasks.dashboard"), 302)