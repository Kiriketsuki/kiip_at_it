import json
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from .models import Note, User
from . import db
from datetime import datetime
views = Blueprint("views", __name__)

@views.route("/", methods = ["GET", "POST"])
def home():
    if not current_user.is_authenticated:
        return redirect(url_for("auth.account"))
    else:
        variables = {"user": current_user}
        total, completed = get_user_notes(current_user.id)
        variables["total"] = total
        variables["completed"] = completed
        variables["colour_sub"] = 0

        if request.method == "POST":
            note = request.form.get("note")
            if len(note.replace(" ","")) > 0:
                new_note = Note(content = note, user_id = current_user.id)
                db.session.add(new_note)
                db.session.commit()

        return render_template("home.html", variables = variables)

@views.route("/about")
def about():
    return render_template("about.html")

@views.route("/delete_note", methods = ["POST"])
def delete_note():
    data = json.loads(request.data)
    note_id = data["note_id"]
    note = Note.query.get(note_id)
    update_modifiability(note_id)
    if note:
        if note.user_id == current_user.id:
            if note.modifiable == True:
                db.session.delete(note)
                db.session.commit()
    
    return jsonify({})

@views.route("/toggle_completed", methods = ["POST"])
def toggle_completed():
    data = json.loads(request.data)
    note_id = data["note_id"]
    note = Note.query.get(note_id)
    update_modifiability(note_id)
    if note:
        if note.user_id == current_user.id:
            if note.modifiable == True:
                note.completed = not note.completed # within a day still can mark the task and unmark
            else:
                note.completed = True # after a day can still finish a task, but cannot unmark a task

    return jsonify({})


def get_user_notes(user_id):
    user = User.query.get(user_id)
    total = 0
    completed = 0
    for note in user.notes:
        total += 1
        if note.completed == True:
            completed += 1

    return total, completed

def update_modifiability(note_id):
    note = Note.query.get(note_id)
    difference = datetime.now() - note.date
    if difference.days > 1:
        note.modifiable = False
        db.session.commit()
