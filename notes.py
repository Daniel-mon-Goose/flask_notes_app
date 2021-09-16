from app import app, db
from app.models import Note, PreviousNote


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Note': Note, 'PreviousNote': PreviousNote}
