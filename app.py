from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__, static_folder="static")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Notes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Notes %r>' % self.id



@app.route('/')
def main():
    return render_template("main.html")


@app.route('/add-note', methods=['POST', 'GET'])
def add_note():
    if request.method == 'POST':
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']

        note = Notes(title=title, intro=intro, text=text)

        try:
            db.session.add(note)
            db.session.flush()  # Сохраняем изменения в базе данных
            db.session.commit()
            return redirect(url_for('read_notes'))

        except Exception as e:
            return "Error: " + str(e)
    else:
        return render_template("insert.html")


@app.route('/read-note')
def read_notes():
    notes = Notes.query.order_by(Notes.date.desc()).all()
    return render_template("notes.html", notes=notes)


@app.route('/read-note/<int:id>')
def notes_detail(id):
    note = Notes.query.get(id)
    return render_template("note_detail.html", note=note)


@app.route('/read-note/<int:id>/delete')
def notes_delete(id):
    note = Notes.query.get_or_404(id)

    try:
        db.session.delete(note)
        db.session.flush()  # Сохраняем изменения в базе данных
        db.session.commit()
        return redirect(url_for('read_notes'))

    except Exception as e:
        return "Error: " + str(e)


@app.route('/read-note/<int:id>/update', methods=['POST', 'GET'])
def note_update(id):
    note = Notes.query.get(id)
    if request.method == 'POST':
        note.title = request.form['title']
        note.intro = request.form['intro']
        note.text = request.form['text']

        try:
            db.session.commit()
            return redirect(url_for('read_notes'))

        except Exception as e:
            return "Error: " + str(e)
    else:

        return render_template("note_update.html", note=note)


if __name__ == "__main__":
    app.run(debug=True)