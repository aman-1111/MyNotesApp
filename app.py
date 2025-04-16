from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Database setup (SQLite in the 'instance' folder)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + 'notes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Model for the Notes
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<Note {self.title}>'

# Create the database tables if they don't exist
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    notes = Note.query.all()  # Retrieve all notes from the database
    return render_template('index.html', notes=notes)

@app.route('/add', methods=['POST'])
def add_note():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        new_note = Note(title=title, content=content)

        db.session.add(new_note)
        db.session.commit()

        return redirect(url_for('index'))

@app.route('/delete/<int:id>', methods=['GET'])
def delete_note(id):
    note_to_delete = Note.query.get_or_404(id)

    db.session.delete(note_to_delete)
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update_note(id):
    note = Note.query.get_or_404(id)

    if request.method == 'POST':
        note.title = request.form['title']
        note.content = request.form['content']

        db.session.commit()
        return redirect(url_for('index'))

    return render_template('update.html', note=note)

if __name__ == "__main__":
    app.run(debug=True)

# import os
# from flask import Flask

# app = Flask(__name__)

# # Configure the app to use the database file inside the 'instance' folder
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.instance_path, 'your_db.db')

# # This allows Flask to access the database in the instance folder
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
