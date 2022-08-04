from flask import Flask, render_template, request

app = Flask(__name__)

notes = []

@app.route("/", methods=["POST", 'GET'])
def index():
  if request.method == "POST":
    if request.form.get("new"):
      note = request.form.get("note")
      notes.append(note)
      return render_template("index.html", notes=notes)
    elif request.form.get("edit"):
      note = request.form.get("note")
      notes[int(request.form['edit']) - 1] = note
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