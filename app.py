from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

ENV = 'dev'

if ENV == 'dev':
  app.debug = True
  app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123456@localhost/notes_app'
else:
  app.debug = False
  app.config['SQLALCHEMY_DATABASE_URI'] = ''

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Notes(db.Model):
    __tablename__ = 'notes'
    id = db.Column(db.Integer, primary_key=True)
    note = db.Column(db.String(200))

    def __init__(self, note):
        self.note = note

@app.route("/", methods=["POST", 'GET'])
def index():
  if request.method == "POST":
    if request.form.get("new"):
      note = request.form.get("note")
      data = Notes(note)
      db.session.add(data)
      db.session.commit()
      notes = Notes.query.order_by(Notes.id).all()
      return render_template("index.html", notes=notes)
    elif request.form.get("edit"):
      new_note = request.form.get("note")
      old_note = Notes.query.get(int(request.form['edit']))
      old_note.note = new_note
      db.session.commit()
      notes = Notes.query.order_by(Notes.id).all()
      return render_template("index.html", notes=notes)
  else:
    notes = Notes.query.order_by(Notes.id).all()
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
    old_note = Notes.query.get(value).note
    return render_template("add.html", name=name, value=value, old_note=old_note)
  elif request.form.get("delete"):
    value = int(request.form['delete'])
    old_note = db.session.query(Notes).filter(Notes.id==value).first()
    db.session.delete(old_note)
    db.session.commit()
    notes = Notes.query.order_by(Notes.id).all()
    return render_template("index.html", notes=notes)

if __name__ == '__main__':
    app.run()
