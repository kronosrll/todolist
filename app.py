# Import the Flask library and render_templates library
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

# Create a Flask app
app = Flask(__name__) #two underscores on each side of name 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    


# Define a route for the home page ("/")
@app.route('/')
def index():
    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    task_content = request.form['content']
    if task_content:
        new_task = Task(content=task_content)
        db.session.add(new_task)
        db.session.commit()
    return redirect('/')

@app.route('/delete/<int:id>')
def delete_task(id):
    task = Task.query.get(id)
    if task:
        db.session.delete(task)
        db.session.commit()
    return redirect('/')



# Run the Flask app if this script is the main entry point. #two underscores on each side of name and main

if __name__ == "__main__":
    with app.app_context():
       db.create_all()
    app.run(debug=True)