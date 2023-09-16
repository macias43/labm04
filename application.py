from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)
app.app_context().push()

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(120))

    def __repr__(self):
        return f"{self.name} - {self.description}"

# Create the application context
with app.app_context():
    # Create the database tables
    db.create_all()

@app.route('/')
def index():
    return 'Hello!'

@app.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    book_list = []
    for book in books:
        book_list.append({
            'name': book.name,
            'description': book.description
        })
    return jsonify({'books': book_list})

@app.route('/books', methods=['POST'])
def add_book():
    data = request.json
    name = data.get('name')
    description = data.get('description')

    if not name:
        return jsonify({'message': 'Name is required'}), 400

    # Check if the book already exists in the database
    existing_book = Book.query.filter_by(name=name).first()
    if existing_book:
        return jsonify({'message': 'Book with this name already exists'}), 400

    book = Book(name=name, description=description)

    db.session.add(book)
    db.session.commit()

    return jsonify({'message': 'Book added successfully'}), 201

if __name__ == "__main__":
    app.run(debug=True)
