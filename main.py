from flask import Flask
app = Flask(__name__)
from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(80), unique=True, nullable=False)
    author = db.Column(db.String(120))
    publisher = db.Column(db.String(120))

    def __repr__(self):
        return f"{self.book_name} - {self.author} - {self.publisher}"

@app.route('/')
def index():
    return 'Hello!'

@app.route('/books')
def get_books():
    books = Book.query.all()
    output = []
    for book in books:
        book_data = {'id': book.id, 'book_name': book.book_name, 'author': book.author, 'publisher': book.publisher}
        output.append(book_data)
    return {'books': output}

@app.route('/books/<id>')
def get_book(id):
    book = Book.query.get_or_404(id)
    return {'id': book.id, 'book_name': book.book_name, 'author': book.author, 'publisher': book.publisher}

@app.route('/books', methods=['POST'])
def add_book():
    book_name = request.json['book_name']
    author = request.json['author']
    publisher = request.json['publisher']
    book = Book(book_name=book_name, author=author, publisher=publisher)
    db.session.add(book)
    db.session.commit()
    return {'id': book.id}

@app.route('/books/<id>', methods=['PUT'])
def update_book(id):
    book = Book.query.get(id)
    if book is None:
        return {"error": "Book not found"}
    book.book_name = request.json.get('book_name', book.book_name)
    book.author = request.json.get('author', book.author)
    book.publisher = request.json.get('publisher', book.publisher)
    db.session.commit()
    return {'message': 'Book updated'}

@app.route('/books/<id>', methods=['DELETE'])
def delete_book(id):
    book = Book.query.get(id)
    if book is None:
        return {"error": "Book not found"}
    db.session.delete(book)
    db.session.commit()
    return {'message': 'Book deleted'}

if __name__ == '__main__':
    app.run(debug=True)