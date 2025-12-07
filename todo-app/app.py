from flask import Flask, request, jsonify, render_template
from models import db, Todo

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        try:
            db.create_all()
        except Exception as e:
            print("Tables might already exist:", e)

    @app.route('/todos', methods=['POST'])
    def add_todo():
        data = request.json
        todo = Todo(title=data['title'])
        db.session.add(todo)
        db.session.commit()
        return jsonify({"message": "Todo created"}), 201

    @app.route('/todos', methods=['GET'])
    def get_todos():
        todos = Todo.query.all()
        return jsonify([{"id": t.id, "title": t.title, "completed": t.completed} for t in todos])

    @app.route('/')
    def index():
        return render_template('index.html')

    return app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
