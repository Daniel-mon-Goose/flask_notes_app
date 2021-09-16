from app import db
from datetime import datetime


class Note(db.Model):
    MAX_TEXT_LENGTH = 280
    MAX_TITLE_LENGTH = 120

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(MAX_TITLE_LENGTH))
    text = db.Column(db.String(MAX_TEXT_LENGTH))
    created_on = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    last_edited_on = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    previous_versions = db.relationship('PreviousNote',
                                        backref='original_note',
                                        lazy='dynamic',
                                        cascade='all, delete, delete-orphan')


class PreviousNote(db.Model):
    MAX_TEXT_LENGTH = 280
    MAX_TITLE_LENGTH = 120

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(MAX_TITLE_LENGTH))
    text = db.Column(db.String(MAX_TEXT_LENGTH))
    created_on = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    original_id = db.Column(db.Integer, db.ForeignKey('note.id', ondelete='cascade'))
