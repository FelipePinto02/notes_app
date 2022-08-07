from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import os
import re

app = Flask(__name__)

ENV = 'prod'

if ENV == 'dev':
  app.debug = True
  app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123456@localhost/notes_app'
else:
  uri = os.getenv("DATABASE_URL")
  if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://")
  app.debug = False
  app.config['SQLALCHEMY_DATABASE_URI'] = uri

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Notes(db.Model):
    __tablename__ = 'notes'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    note = db.Column(db.Text)

    def __init__(self, title, note):
      self.title = title
      self.note = note

@app.route("/", methods=["POST", 'GET'])
def index():
  if request.method == "POST":
    if request.form.get("new"):
      title = request.form.get("title")
      note = request.form.get("note")
      if title == '' or note == '':
        return render_template("add.html", message="Please enter your title and note!", name='new', value='new')
      else:
        data = Notes(title, note)
        db.session.add(data)
        db.session.commit()
        notes = Notes.query.order_by(Notes.id).all()
        return render_template("index.html", notes=notes)
    elif request.form.get("edit"):
      new_title = request.form.get("title")
      new_note = request.form.get("note")
      old_note = Notes.query.get(int(request.form['edit']))
      if new_title == '' or new_note == '':
        return render_template("add.html", message="Please enter your title and note!", name='edit', value=int(request.form['edit']), old_note=old_note)
      else:
        old_note.note = new_note
        old_note.title = new_title
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
    old_note = Notes.query.get(value)
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
