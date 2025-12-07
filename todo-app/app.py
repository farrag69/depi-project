from flask import Flask, request, jsonify, render_template, redirect, url_for
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

    # ---------------------------
    # HTML ROUTES
    # ---------------------------

    @app.route('/')
    def index():
        todos = Todo.query.order_by(Todo.id.desc()).all()
        return render_template('index.html', todos=todos)

    @app.route('/add', methods=['POST'])
    def add_from_form():
        title = request.form.get('title')
        todo = Todo(title=title)
        db.session.add(todo)
        db.session.commit()
        return redirect(url_for('index'))

    @app.route('/toggle/<int:todo_id>')
    def toggle(todo_id):
        todo = Todo.query.get_or_404(todo_id)
        todo.completed = not todo.completed
        db.session.commit()
        return redirect(url_for('index'))

    @app.route('/delete/<int:todo_id>')
    def delete(todo_id):
        todo = Todo.query.get_or_404(todo_id)
        db.session.delete(todo)
        db.session.commit()
        return redirect(url_for('index'))

    # ---------------------------
    # JSON API ROUTES (optional)
    # ---------------------------

    @app.route('/todos', methods=['POST'])
    def add_todo_json():
        data = request.json
        todo = Todo(title=data['title'])
        db.session.add(todo)
        db.session.commit()
        return jsonify({"message": "Todo created"}), 201

    @app.route('/todos', methods=['GET'])
    def get_todos_json():
        todos = Todo.query.all()
        return jsonify([
            {"id": t.id, "title": t.title, "completed": t.completed}
            for t in todos
        ])

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
