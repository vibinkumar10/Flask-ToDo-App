from flask import Flask,render_template,redirect,url_for,flash,session
from flask_sqlalchemy import SQLAlchemy
from forms import Login_form,Register_form,Task_form

db = SQLAlchemy()

app = Flask(__name__)

app.config["SECRET_KEY"] = "7777777"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo_app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

#DATABASE
class Users(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(50),nullable=False)
    email = db.Column(db.String(50),nullable=False,unique=True)
    password = db.Column(db.String(15),nullable=False)

class Tasks(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    task = db.Column(db.String(50),nullable=False)
    status = db.Column(db.String(20),default="Pending",nullable=False)
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))

#APP CREATION (PATHS)
#Login 
@app.route("/",methods=["GET","POST"])
def login():
    form = Login_form()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        existing_user = Users.query.filter_by(email=email).first()
        if existing_user and existing_user.password == password:
            session["id"] = existing_user.id
            session["name"] = existing_user.name
            flash("Login successful","success")
            return redirect(url_for("tasks"))
        elif existing_user and existing_user.password != password:
            flash("Incorrect Password","warning")
            return redirect(url_for("login"))
        else:
            flash("Invalid credentials please register to continue","danger")
            return redirect(url_for("register"))
    return render_template("login.html",form=form)

#Register
@app.route("/register",methods=["GET","POST"])
def register():
    form = Register_form()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data
        existing_user = Users.query.filter_by(email=email).first()
        if existing_user:
            flash("You already have an account, please login here","warning")
            return redirect(url_for("login"))
        new_user = Users(name=name,email=email,password=password)
        db.session.add(new_user)
        db.session.commit()
        flash("Registration successful","success")
        return redirect(url_for("login"))
    return render_template("register.html",form=form)

#Showing Tasks
@app.route("/tasks")
def tasks():
    if "id" not in session:
        flash("Please login to access this feature","danger")
        return redirect(url_for("login"))
    tasks = Tasks.query.filter_by(user_id = session["id"]).all()
    return render_template("tasks.html",tasks=tasks,name=session["name"])

#Adding tasks
@app.route("/add",methods=["GET","POST"])
def add():
    if "id" not in session:
        flash("Please login to access this feature","danger")
        return redirect(url_for("login"))
    form = Task_form()
    if form.validate_on_submit():
        task = form.task.data
        new_task = Tasks(task=task,user_id=session["id"])
        db.session.add(new_task)
        db.session.commit()
        flash("One task added successfully","success")
        return redirect(url_for("tasks"))
    return render_template("add.html",form=form)

#clearing Tasks
@app.route("/clear")
def clear():
    if "id" not in session:
        flash("Please login to access this feature","danger")
        return redirect(url_for("login"))
    Tasks.query.filter_by(user_id=session["id"]).delete()
    db.session.commit()
    flash("All tasks have been cleared successfully","success")
    return redirect(url_for("tasks"))

#Deleting a single task
@app.route("/delete/<int:task_id>",methods=["GET","POST"])
def delete(task_id):
    if "id" not in session:
        flash("Please login to access this feature","danger")
        return redirect(url_for("login"))
    del_task = Tasks.query.get(task_id)
    if del_task and del_task.user_id == session["id"]:
        db.session.delete(del_task)
        db.session.commit()
        flash("one item deleted successfully","success")
    return redirect(url_for("tasks"))

#Marking the status
@app.route("/toggle/<int:task_id>",methods=["GET","POST"])
def toggle(task_id):
    if "id" not in session:
        flash("Please login to access this feature","danger")
        return redirect(url_for("login"))
    task = Tasks.query.get(task_id)
    if task and task.user_id == session["id"]:
        if task.status == "Pending":
            task.status = "Working"
        elif task.status == "Working":
            task.status = "Done"
        else:
            task.status = "Pending"
        db.session.commit()
    return redirect(url_for("tasks"))

#Logout
@app.route("/logout")
def logout():
    session.pop("id",None)
    session.pop("name",None)
    flash("Logged out successfully","success")
    return redirect(url_for("login"))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug = True)