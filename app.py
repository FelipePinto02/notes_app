from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123456@localhost/notes_app'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Notes(db.Model):
    __tablename__ = 'notes'
    id = db.Column(db.Integer, primary_key=True)
    note = db.Column(db.String(200))

    def __init__(self, note):
        self.note = note

notes = Notes.query.all()

@app.route("/", methods=["POST", 'GET'])
def index():
  if request.method == "POST":
    if request.form.get("new"):
      note = request.form.get("note")
      data = Notes(note)
      db.session.add(data)
      db.session.commit()
      #notes.append(note)
      return render_template("index.html", notes=notes)
    elif request.form.get("edit"):
      new_note = request.form.get("note")
      old_note = Notes.query.get(int(request.form['edit']))
      old_note.note = new_note
      db.session.commit()
      #notes[int(request.form['edit']) - 1] = note
      return render_template("index.html", notes=notes)
  else:
    return render_template("index.html", notes=notes)  

@app.route("/notes", methods=["POST"])
def salvar():
  if request.form.get("new"):
    name = 'new'
    value = 'new'
    return render_template("add.html", name=name, value=value)
  elif request.form.get("edit"):
    name = 'edit'
    value = int(request.form.get('edit'))
    return render_template("add.html", name=name, value=value)
  elif request.form.get("delete"):
    value = int(request.form['delete'])
    notes.pop(value - 1)
    return render_template("index.html", notes=notes)

if __name__ == '__main__':
    app.debug = True
    app.run()