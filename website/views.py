import json
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
views = Blueprint("views", __name__)

@views.route("/", methods = ["GET", "POST"])
def home():
    if not current_user.is_authenticated:
        return redirect(url_for("auth.account"))
    else:
        variables = {"user": current_user}

        if request.method == "POST":
            note = request.form.get("note")
            new_note = Note(content = note, user_id = current_user.id)
            db.session.add(new_note)
            db.session.commit()
        return render_template("home.html", variables = variables)

@views.route("/delete_note", methods = ["POST"])
def delete_note():
    data = json.loads(request.data)
    note_id = data["note_id"]
    note = Note.query.get(note_id)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
    
    return jsonify({})

@views.route("/toggle_completed", methods = ["POST"])
def toggle_completed():
    data = json.loads(request.data)
    note_id = data["note_id"]
    note = Note.query.get(note_id)
    if note:
        if note.user_id == current_user.id:
            note.completed = not note.completed
            db.session.commit()

    return jsonify({})