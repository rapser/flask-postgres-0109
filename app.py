from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields
from marshmallow_sqlalchemy import ModelSchema

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:root1983@localhost/libraryCatalog'
app.debug=True

db = SQLAlchemy(app)

# Model
class Todo(db.Model):
    __tablename__ = "todos"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20))
    todo_description = db.Column(db.String(100))

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __init__(self, title, todo_description):
        self.title = title
        self.todo_description = todo_description

    def __repr__(self):
        return f"{self.id}"

class Book(db.Model):
    __tablename__ = "books"
    id = db.Column(db.Integer, primary_key=True)
    bookTitle = db.Column(db.String(100), nullable=False)
    bookText = db.Column(db.String(), nullable=False)
    likes = db.Column(db.Integer(), nullable=False, default=0)

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __init__(self, bookTitle, bookText, likes):
        self.bookTitle = bookTitle
        self.bookText = bookText
        self.likes = likes

    def __repr__(self):
        return f"{self.id}"


db.create_all()


class TodoSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Todo
        sqla_session = db.session

    id = fields.Integer(dump_only=True)
    title = fields.String(required=True)
    todo_description = fields.String(required=True)


@app.route('/api/v1/todo', methods=['GET'])
def index():
    get_todos = Todo.query.all()
    todo_schema = TodoSchema(many=True)
    todos = todo_schema.dump(get_todos)
    return make_response(jsonify({"todos": todos}))


@app.route('/api/v1/todo/<id>', methods=['GET'])
def get_todo_by_id(id):
    get_todo = Todo.query.get(id)
    todo_schema = TodoSchema()
    todo = todo_schema.dump(get_todo)
    return make_response(jsonify({"todo": todo}))


@app.route('/api/v1/todo/<id>', methods=['PUT'])
def update_todo_by_id(id):
    data = request.get_json()
    get_todo = Todo.query.get(id)
    if data.get('title'):
        get_todo.title = data['title']
    if data.get('todo_description'):
        get_todo.todo_description = data['todo_description']
    db.session.add(get_todo)
    db.session.commit()
    todo_schema = TodoSchema(only=['id', 'title', 'todo_description'])
    todo = todo_schema.dump(get_todo)
    return make_response(jsonify({"todo": todo}))


@app.route('/api/v1/todo/<id>', methods=['DELETE'])
def delete_todo_by_id(id):
    get_todo = Todo.query.get(id)
    db.session.delete(get_todo)
    db.session.commit()
    return make_response("", 204)


@app.route('/api/v1/todo', methods=['POST'])
def create_todo():
    data = request.get_json()
    todo_schema = TodoSchema()
    todo = todo_schema.load(data)
    result = todo_schema.dump(todo.create())
    return make_response(jsonify({"todo": result}), 200)

class BookSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Book
        sqla_session = db.session

    id = fields.Integer(dump_only=True)
    bookTitle = fields.String(required=True)
    bookText = fields.String(required=True)
    likes = fields.Integer(required=True)

@app.route('/api/v1/book', methods=['GET'])
def get_books():
    get_books = Book.query.all()
    book_schema = BookSchema(many=True)
    books = book_schema.dump(get_books)
    return make_response(jsonify({"books": books}))

@app.route('/api/v1/book/<id>', methods=['GET'])
def get_book_by_id(id):
    get_book = Book.query.get(id)
    book_schema = BookSchema()
    book = book_schema.dump(get_book)
    return make_response(jsonify({"book": book}))

@app.route('/api/v1/book', methods=['POST'])
def create_book():
    data = request.get_json()
    book_schema = BookSchema()
    book = book_schema.load(data)
    result = book_schema.dump(book.create())
    return make_response(jsonify({"book": result}), 200)

@app.route('/api/v1/book/<id>', methods=['DELETE'])
def delete_book_by_id(id):
    try:
        get_book = Book.query.get(id)
        db.session.delete(get_book)
        db.session.commit()
        return make_response("", 204)
    except:
        return make_response(jsonify({'status': 'No se puedo eliminar'}), 404)

@app.route('/api/v1/book/<id>', methods=['PUT'])
def update_book_by_id(id):
    try:
        data = request.get_json()
        get_book = Book.query.get(id)
        if data.get('bookTitle'):
            get_book.bookTitle = data['bookTitle']
        if data.get('bookText'):
            get_book.bookText = data['bookText']
        if data.get('likes'):
            get_book.likes = data['likes']
        db.session.add(get_book)
        db.session.commit()
        book_schema = BookSchema(only=['id', 'bookTitle', 'bookText', 'likes'])
        book = book_schema.dump(get_book)
        return make_response(jsonify({"book": book}))
    except :
        return make_response(jsonify({'status': 'No se pudo actualizar'}), 404)

if __name__ == '__main__':
    app.debug = True
    app.run()