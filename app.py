from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc, asc

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
    all_books = Books.query.order_by(asc(Books.id)).all()
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
def addBook():
    try:
        body = request.json
        bookTitle = body['bookTitle']
        bookText = body['bookText']
        likes = body['likes']

        data = Books(bookTitle, bookText, likes)
        db.session.add(data)
        db.session.commit()

        return jsonify({'status': 'Data is posted to PostgreSQL!'}), 201
    except:
        return jsonify({'error': 'Ha sucedido un error en el servidor'})


@app.route('/books/<string:id>', methods=['GET'])
def getBookById(id):

    try:
        data = Books.query.get(id)
        dataDict = {
            'id': str(data).split('/')[0],
            'bookTitle': str(data).split('/')[1],
            'bookText': str(data).split('/')[2],
            'likes': str(data).split('/')[3]
        }
        return jsonify(dataDict)
    except:
        return jsonify({'error': 'No existe el usuario con id: '+id+''}), 404

@app.route('/books/<string:id>', methods=['DELETE'])
def deleteBook(id):
    try:
        delData = Books.query.filter_by(id=id).first()
        db.session.delete(delData)
        db.session.commit()
        return jsonify({'status': 'Data '+id+' is deleted from PostgreSQL!'})
    except:
        return jsonify({'status': 'No se puedo eliminar'})

@app.route('/books/<string:id>', methods=['PUT'])
def updateBook(id):
    try:
        body = request.json
        editData = Books.query.filter_by(id=id).first()
        editData.bookTitle = body['bookTitle']
        editData.bookText = body['bookText']
        editData.likes = body['likes']
        db.session.commit()
        return jsonify({'status': 'Data '+id+' is updated from PostgreSQL!'})
    except:
        return jsonify({'error': 'No se pudo actualizar'}), 404

if __name__ == '__main__':
    app.debug = True
    app.run()