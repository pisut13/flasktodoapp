from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy

# alltaki satılar her programda olmalı; alınan web sayfası: https://flask-sqlalchemy.palletsprojects.com/en/2.x/quickstart/
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://///home/pisut/Masaüstü/ToDoApp/todo.db'   # ORM'ye veri tabanının tanıtılması
db = SQLAlchemy(app)



@app.route("/")
def index():
    todos = Todo.query.all()
    return render_template ("index.html",todos=todos)


@app.route("/complete/<string:id>")
def completeTodo(id):
    todo = Todo.query.filter_by(id = id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("index"))




@app.route("/add", methods=["POST"])
def addTodo():
    title = request.form.get("title")
    newTodo = Todo(title=title, complete=False)
    db.session.add(newTodo)
    db.session.commit()
    return redirect(url_for("index"))



@app.route("/delete/<string:id>")
def deleteTodo(id):
    todo = Todo.query.filter_by(id = id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("index"))




# veri tabanında "Todo" isimli bir tablo oluşturmak için oluşturulan class; bu class "SQLAlchemy" içindeki "Model" class'ından inherit ediliyor 
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)    # tabloda ilk sütun "id" olacak ve bu auto increment
    title = db.Column(db.String(80))                # bu sütundaki veriler string ve maksimum 80 karakter olacak
    complete = db.Column(db.Boolean)                # bu sütundaki verileri boolean değerleri (true-false) olacak








if __name__ == "__main__":
    db.create_all()        # bu satır bu dosyadaki bütün class'ları veri tabanına bir tablo olarak eklenecek..
    app.run(debug=True)    # burası uygulamayı çalıştırıyor..

