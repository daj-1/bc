from flask import request, jsonify, Blueprint, render_template, redirect, url_for
from models import db, Book

bp = Blueprint('api', __name__)

@bp.route('/')
def index():
    search = request.args.get('search')
    if search:
        books = Book.query.filter(
            (Book.title.like(f'%{search}%')) |
            (Book.author.like(f'%{search}%')) |
            (Book.genre.like(f'%{search}%')) |
            (Book.year.like(f'%{search}%'))
        ).all()
    else:
        books = Book.query.all()
    return render_template('index.html', books=books)

@bp.route('/books/<int:book_id>')
def book_detail(book_id):
    book = Book.query.get_or_404(book_id)
    return render_template('book_detail.html', book=book)

@bp.route('/stats', methods=['GET'])
def get_stats():
    # Total number of books
    total_books = Book.query.count()

    # Distribution of genres
    genre_distribution = db.session.query(Book.genre, db.func.count(Book.id)).group_by(Book.genre).all()
    # Convert the result to a list of dictionaries
    genre_distribution = [{"genre": genre, "count": count} for genre, count in genre_distribution]

    # Most popular author (author with the most books)
    most_popular_author = db.session.query(Book.author, db.func.count(Book.id)).group_by(Book.author).order_by(db.func.count(Book.id).desc()).first()
    # Convert the result to a dictionary
    most_popular_author = {"author": most_popular_author[0], "count": most_popular_author[1]} if most_popular_author else None

    # Prepare statistics data
    stats = {
        "total_books": total_books,
        "genre_distribution": genre_distribution,
        "most_popular_author": most_popular_author,
    }

    return jsonify(stats)


@bp.route('/add', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        new_book = Book(
            title=request.form['title'],
            author=request.form['author'],
            genre=request.form['genre'],
            year=request.form['year'],
            description=request.form['description'],
            copies=request.form['copies']
        )
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('api.index'))
    return render_template('add_book.html')

@bp.route('/edit/<int:book_id>', methods=['GET', 'POST'])
def edit_book(book_id):
    book = Book.query.get_or_404(book_id)
    if request.method == 'POST':
        book.title = request.form['title']
        book.author = request.form['author']
        book.genre = request.form['genre']
        book.year = request.form['year']
        book.description = request.form['description']
        book.copies = request.form['copies']
        db.session.commit()
        return redirect(url_for('api.book_detail', book_id=book.id))
    return render_template('edit_book.html', book=book)

@bp.route('/delete/<int:book_id>', methods=['POST'])
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for('api.index'))

# API endpoints for CRUD operations
@bp.route('/api/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    return jsonify([book.serialize() for book in books])

@bp.route('/api/books/<int:id>', methods=['GET'])
def get_book(id):
    book = Book.query.get_or_404(id)
    return jsonify(book.serialize())

@bp.route('/api/books', methods=['POST'])
def add_book_api():
    data = request.get_json()
    new_book = Book(
        title=data['title'],
        author=data['author'],
        genre=data['genre'],
        year=data['year'],
        description=data.get('description', ''),
        copies=data['copies']
    )
    db.session.add(new_book)
    db.session.commit()
    return jsonify(new_book.serialize()), 201

@bp.route('/api/books/<int:id>', methods=['PUT'])
def update_book_api(id):
    book = Book.query.get_or_404(id)
    data = request.get_json()
    book.title = data['title']
    book.author = data['author']
    book.genre = data['genre']
    book.year = data['year']
    book.description = data.get('description', book.description)
    book.copies = data['copies']
    db.session.commit()
    return jsonify(book.serialize())

@bp.route('/api/books/<int:id>', methods=['DELETE'])
def delete_book_api(id):
    book = Book.query.get_or_404(id)
    db.session.delete(book)
    db.session.commit()
    return '', 204

# Serialize method for Book model
def serialize(self):
    return {
        'id': self.id,
        'title': self.title,
        'author': self.author,
        'genre': self.genre,
        'year': self.year,
        'description': self.description,
        'copies': self.copies
    }

Book.serialize = serialize
