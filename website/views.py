from flask import Blueprint,render_template, request, flash, redirect
from flask_login import current_user
from .models import Note
from . import db

views = Blueprint('views', __name__)


@views.route("/")
def home():
    return render_template('index.html', user=current_user, thumbnail="../static/thumbnail.png")


@views.route('/app', methods=["GET", "POST"])
def main():
    if current_user.is_authenticated:
        if request.method == "POST":
            title = request.form.get('title')
            description = request.form.get('description')
            new_note = Note(title=title, description=description, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash("New Note Added Successfully!", "success")
        return render_template('app.html', user=current_user)
    flash("You Need To Login to Access this Page", "danger")
    return redirect('/login')


@views.route('/delete/<serial>')
def delete(serial):
    if current_user.is_authenticated:
        note = Note.query.filter_by(serial=serial).first()
        if note and note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
            flash("Note Removed Successfully!", "success")
        else:
            flash('Note Not Found', 'danger')
        return redirect('/app')
    flash("You Need To Login to Access this Page", 'danger')
    return redirect('/login')


@views.route('/update/<serial>', methods=["GET", "POST"])
def update(serial):
    if current_user.is_authenticated:
        note = Note.query.filter_by(serial=serial).first()
        if note and note.user_id == current_user.id:
            if request.method == "POST":
                title = request.form.get('title')
                description = request.form.get('description')
                note = Note.query.filter_by(serial=serial).first()
                note.title = title
                note.description = description
                db.session.add(note)
                db.session.commit()
                flash("Note Updated Successfully!", "success")
                return redirect('/app')
            return render_template("update.html", note=note, user=current_user)
        else:
            return redirect('/app')
    flash("You Need To Login to Access this Page", 'danger')
    return redirect('/login')

