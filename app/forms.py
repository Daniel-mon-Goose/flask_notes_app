from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, StringField
from wtforms.validators import Length, DataRequired, ValidationError
from app.models import Note


class AddNoteForm(FlaskForm):
    title = StringField('Note title', validators=[DataRequired(), Length(min=0, max=Note.MAX_TITLE_LENGTH)])
    text = TextAreaField('Note text', validators=[Length(min=0, max=Note.MAX_TEXT_LENGTH)])
    submit = SubmitField("Submit")


class EditNoteForm(AddNoteForm):
    def __init__(self, original_title, original_text, *args, **kwargs):
        super(EditNoteForm, self).__init__(*args, **kwargs)
        self.original_title = original_title
        self.original_text = original_text

    def validate_submit(self, submit):
        if self.title.data == self.original_title and self.text.data == self.original_text:
            raise ValidationError('No new data provided')


class DeleteForm(FlaskForm):
    delete = SubmitField("Delete")
    cancel = SubmitField("Cancel")
