from app import app, db
from flask import render_template, flash, redirect, url_for, request, jsonify
from datetime import datetime
from app.models import Note, PreviousNote
from app.forms import AddNoteForm, DeleteForm, EditNoteForm


@app.route('/')
@app.route('/index')
def index():
    notes = Note.query.all()
    return render_template('index.html',
                           title='Home',
                           notes=notes if len(notes) > 0 else None)


@app.route('/add', methods=['GET', 'POST'])
def add():
    form = AddNoteForm()
    if form.validate_on_submit():
        new_note = Note(title=form.title.data, text=form.text.data)
        db.session.add(new_note)
        db.session.commit()
        new_history_note = PreviousNote(title=form.title.data, text=form.text.data, original_id=new_note.id)
        db.session.add(new_history_note)
        db.session.commit()
        flash('Note successfully added')
        return redirect(url_for('index'))

    return render_template('add.html', title='Add', form=form)


@app.route('/note/<note_id>')
def note(note_id):
    current_note = Note.query.filter_by(id=note_id).first_or_404()
    return render_template('note.html', title='Show', note=current_note)


@app.route('/delete/<note_id>', methods=['GET', 'POST'])
def delete(note_id):
    current_note = Note.query.filter_by(id=note_id).first_or_404()
    form = DeleteForm()
    if form.validate_on_submit():
        if form.delete.data:
            db.session.delete(current_note)
            db.session.commit()
            flash('Note successfully deleted')

        return redirect(url_for('index'))

    return render_template('delete.html', title='Delete', current_note=current_note, form=form)


@app.route('/edit/<note_id>', methods=["GET", "POST"])
def edit(note_id):
    current_note = Note.query.filter_by(id=note_id).first_or_404()
    form = EditNoteForm(current_note.title, current_note.text)
    if form.validate_on_submit():
        current_note.last_edited_on = datetime.utcnow()
        current_note.title = form.title.data
        current_note.text = form.text.data
        new_history_note = PreviousNote(title=current_note.title,
                                        text=current_note.text,
                                        original_id=current_note.id)
        db.session.add(new_history_note)
        db.session.commit()
        flash('Note successfully edited')
        return redirect(url_for('edit', note_id=note_id))
    elif request.method == "GET":
        form.title.data = current_note.title
        form.text.data = current_note.text
    return render_template('edit.html', title='Edit', form=form)


@app.route('/history/<note_id>')
def history(note_id):
    current_note = Note.query.filter_by(id=note_id).first_or_404()
    previous_notes = PreviousNote.query.filter_by(original_id=note_id).order_by(PreviousNote.created_on.desc()).all()
    return render_template('history.html', title='History',
                           current_note=current_note,
                           previous_notes=previous_notes)


@app.route('/previous_note/<previous_id>')
def previous_note(previous_id):
    previous = PreviousNote.query.filter_by(id=previous_id).first_or_404()
    return render_template('previous_note.html', previous_note=previous)
