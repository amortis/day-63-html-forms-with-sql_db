from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import sqlite3

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///books-collection.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Book {self.title}>'

with app.app_context():
    db.create_all()



@app.route('/')
def home():
    all_books = db.session.query(Book).all()
    return render_template("index.html", books_list=all_books)


@app.route("/add", methods=["POST", "GET"])
def add():
    if request.method == "POST":
        name = request.form["name"]
        author = request.form["author"]
        rating = request.form['rating']
        new_book = Book(title=name, author=author, rating=float(rating))
        print(new_book)
        db.session.add(new_book)
        db.session.commit()
        return render_template("add.html")
    elif request.method == "GET":
        return render_template("add.html")

@app.route("/edit/<int:id>", methods=["POST", "GET"])
def edit(id:int):
    book = Book.query.filter_by(id=id).first()
    if request.method == "GET":
        print(id)
        print(book)
        return render_template("edit.html", book=book)
    elif request.method == "POST":
        book_to_update = Book.query.get(id)
        book_to_update.rating = float(request.form["new_rating"])
        db.session.commit()
        return redirect(url_for("home"))

@app.route("/delete/<int:id>")
def delete(id:int):
    book = Book.query.filter_by(id=id).first()
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for("home"))



if __name__ == "__main__":
    app.run(debug=True)

