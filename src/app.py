from flask import Flask, request
from flask.json import jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root@localhost/flaskmysql'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

# Devuelve instancia a base de datos
db = SQLAlchemy(app)
ma = Marshmallow(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String(13))
    title = db.Column(db.String(100))
    author = db.Column(db.String(50))
    year  = db.Column(db.Integer)
    editorial = db.Column(db.String(50))

    def __init__(self, isbn, title, author, year, editorial):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.year = year
        self.editorial = editorial

# Creación de Tablas
db.create_all()

class BookSchema(ma.Schema):
    class Meta:
        fields = ('id', 'isbn', 'title', 'author', 'year', 'editorial')

book_schema = BookSchema()
books_schema = BookSchema(many=True)

# Endpoints
@app.route('/book', methods = ['POST'])
def create_book():
    print(request.json)
    isbn = request.json['isbn']
    title = request.json['title']
    author = request.json['author']
    year  = request.json['year']
    editorial = request.json['editorial']
    new_book = Book(isbn,title, author, year, editorial)

    # Guardo en la base de datos
    db.session.add(new_book)
    db.session.commit()
    
    return book_schema.jsonify(new_book)

@app.route('/books', methods = ['GET'])
def get_books():
    all_books = Book.query.all()
    # Obtengo lista de datos
    result =  books_schema.dump(all_books)
    return jsonify(result)

@app.route('/book/<id>', methods=['GET'])
def get_book(id):
    book = Book.query.get(id)
    return book_schema.jsonify(book)

@app.route('/book/<id>', methods=['PUT'])
def update_book(id):
    book = Book.query.get(id)

    isbn = request.json['isbn']
    title = request.json['title']
    author = request.json['author']
    year = request.json['year']
    editorial = request.json['editorial']

    book.isbn = isbn
    book.title = title
    book.author = author
    book.year = year
    book.editorial = editorial

    db.session.commit()
    return book_schema.jsonify(book)

@app.route('/book/<id>', methods=['DELETE'])
def delete_book(id):
    book = Book.query.get(id)
    db.session.delete(book)
    db.session.commit()

    return book_schema.jsonify(book)

if __name__ == '__main__':
    app.run(debug=True)