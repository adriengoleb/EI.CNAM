# on importe les libraries nécessaires
from numpy.core.numeric import NaN
import pytesseract as tess
from PIL import Image
from passporteye import read_mrz
import pandas as pd
from translate import Translator
from datetime import datetime
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# on instancie la base de donnée des code ISO 3
iso = pd.read_csv("./../src/Data/ISO.csv", sep=";")

# on instancie la fonction de reconnaissance de pays
def convert_pays(value):
    try:
        return iso.loc[iso["code"] == value, "nationality"].values[0]
    except:
        return value

# on instancie la fonction de premier traitement
def traitement(path):
    
    mrz = read_mrz(path)

    # on essaye de le transformer en dictionnaire de données
    try:
        mrz_data = mrz.to_dict()
        return mrz_data['nationality']

    # si une erreur apparait, on affiche l'échec
    except:
        return "Non identifié"


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return '<Task %r>' % self.id


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content.split("\\")[-1], date_created=convert_pays(traitement(task_content)))

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'Il y a eu une erreur'

    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'Il y a eu une erreur lors de la suppression'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'Il y a eu une erreur lors de la modification'

    else:
        return render_template('update.html', task=task)


if __name__ == "__main__":
    app.run(debug=True)

