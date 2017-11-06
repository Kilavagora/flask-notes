import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify


app = Flask(__name__, static_url_path='')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    note = db.Column(db.String, nullable=False)
    created = db.Column(db.DateTime, default=db.func.current_timestamp())
    modified = db.Column(
        db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())

    def save(self):
        """Save model to DB"""
        db.session.add(self)
        db.session.commit()
    
    @classmethod
    def get_all(cls):
        """Gell all items"""
        return cls.query.all()

    def __init__(self, title, note):
        self.title = title
        self.note = note

    def __repr__(self):
        return f'<Note {self.id}:{self.title}>'

    def to_dict(self):
        return {k.name: getattr(self, k.name) for k in self.__table__.columns}


@app.route('/')
def root():
    return app.send_static_file('index.html')


@app.route('/api/notes/', methods=['GET'])
def get_notes():
    """Get all notes"""
    notes = [note.to_dict() for note in Note.get_all()]
    return jsonify(notes), 200


@app.route('/api/notes/', methods=['POST'])
def create_note():
    """Create a note"""
    data = request.get_json(silent=True)
    try:
        note = Note(**data)
        note.save()
    except Exception as ex:
        print("Cannot create the note.")
    else:
        return jsonify(note.to_dict()), 201
    return jsonify({'message': 'Invalid input.'}), 405
    

@app.route('/api/notes/<int:id>', methods=['GET'])
def get_note(id):
    """Get the note by id"""
    note = Note.query.get(id)
    if not note:
        return jsonify({'message': 'Not found.'}), 404
    return jsonify(note.to_dict()), 200


@app.route('/api/notes/<int:id>', methods=['PUT'])
def update_note(id):
    """Update the note by id"""
    note = Note.query.get(id)  # filter_by(note.id=id).first()
    try:
        data = request.get_json(silent=True)
        note.__init__(**data)
        note.save()
    except:
        print("Cannot update the note.")
    else:
        return jsonify({'message': 'Not found.'}), 404
    return jsonify({'message': 'Invalid input.'}), 405


@app.route('/api/notes/<int:id>', methods=['DELETE'])
def delete_note(id):
    """Delete the note by id"""
    note = Note.query.get(id)
    if not note:
        return bad_request(404)
    note.delete()
    return jsonify({
         "message": f"note {note.id} has been deleted successfully."
        }), 200


if __name__ == '__main__':
    app.run()
