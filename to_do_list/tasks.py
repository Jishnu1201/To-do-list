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
        cursor.execute(f"select l.id, l.task, l.created, l.due, l.status from list l order by l.{oby}")
    else:
        cursor.execute(f"select l.id, l.task, l.created, l.due, l.status from list l order by l.{oby} desc")
    tasks = cursor.fetchall()
    return render_template('index.html', tasks = tasks, order="desc" if order=="asc" else "asc")


