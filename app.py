from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:root1983@localhost/libraryCatalog'
app.debug=True

db = SQLAlchemy(app)

class Books(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    bookTitle = db.Column(db.String(100), nullable=False)
    bookText = db.Column(db.String(), nullable=False)
    likes = db.Column(db.Integer(), nullable=False, default=0)

    def __init__(self, bookTitle, bookText, likes):
        self.bookTitle = bookTitle
        self.bookText = bookText
        self.likes = likes

    def __repr__(self):
        return '%s/%s/%s/%s' % (self.id, self.bookTitle, self.bookText, self.likes)

@app.route('/books', methods=['GET'])
def getBooks():
    all_books = Books.query.all()
    output = []
    for book in all_books:
        currBook = {}
        currBook['id'] = book.id
        currBook['bookTitle'] = book.bookTitle
        currBook['bookText'] = book.bookText
        currBook['likes'] = book.likes
        output.append(currBook)

    return jsonify({'books': output})

@app.route('/books', methods=['POST'])
def data():
    
    # POST a data to database
    if request.method == 'POST':
        body = request.json
        bookTitle = body['bookTitle']
        bookText = body['bookText']
        likes = body['likes']

        data = Books(bookTitle, bookText, likes)
        db.session.add(data)
        db.session.commit()

        return jsonify({
            'status': 'Data is posted to PostgreSQL!'
        })

@app.route('/books/<string:id>', methods=['GET'])
def getBookById(id):
    data = Books.query.get(id)
    dataDict = {
        'id': str(data).split('/')[0],
        'bookTitle': str(data).split('/')[1],
        'bookText': str(data).split('/')[2],
        'likes': str(data).split('/')[3]
    }
    return jsonify(dataDict)

@app.route('/books/<string:id>', methods=['DELETE'])
def deleteBook(id):
    delData = Books.query.filter_by(id=id).first()
    db.session.delete(delData)
    db.session.commit()
    return jsonify({'status': 'Data '+id+' is deleted from PostgreSQL!'})

@app.route('/books/<string:id>', methods=['PUT'])
def updateBook(id):
    body = request.json
    editData = Books.query.filter_by(id=id).first()
    editData.bookTitle = body['bookTitle']
    editData.bookText = body['bookText']
    editData.likes = body['likes']
    db.session.commit()
    return jsonify({'status': 'Data '+id+' is updated from PostgreSQL!'})

if __name__ == '__main__':
    app.debug = True
    app.run()