from flask import Blueprint, render_template, request, redirect, url_for
from .models import Todo
from . import db

my_view = Blueprint("my_view", __name__)

@my_view.route("/")
def home():
    todo_list = Todo.query.all()
    print(todo_list)
    message = request.args.get('message', None)
    filter = request.args.get('filter_category') #! added a filter button so I can display the category selected.
    if filter:
        todo_list = Todo.query.filter_by(category=filter).all()
    
    return render_template("index.html", todo_list=todo_list, message=message)

@my_view.route("/add", methods=["POST"])
def add():
    try: #! Implemented error handling so that user can't input same task again using try/except
        task = request.form.get("task") #! This is a value of the variable task is retrieved from the HTML input named task
        category = request.form.get("category") #! This is also the same but for the category
        new_todo = Todo(task=task, category=category) #! This is a new instantiation of the class we made. The ID property is set automatically, and task and category are set to what the users chose.
        db.session.add(new_todo) #! We then at the new_todo objects to the database where it will become a new row in the table
        db.session.commit() #! Because of the changes the user made, we have to commit them to the database
        message = "Task added." #! Message displayed when user inputs new task
        return redirect(url_for("my_view.home", message = message)) #! At the end of the function, the app redirects us to the route mapped

    except:
        message = "Task already exists." #! Error message sent to notify user if inputted task has already been entered.
        return redirect(url_for("my_view.home", message=message)) #! This will also redirect us to the route mapped

@my_view.route("/update/<todo_id>") #! Creation of our new route
def update(todo_id): #! Calling the function the same as our route which will take the todo ID as an argument
    todo = Todo.query.filter_by(id=todo_id).first() #! The object we want to update is the first result that matches the ID we give to the function when we query the database
    todo.complete = not todo.complete #! Update the complete property to the opposite of what it currently is.
    db.session.commit() #! Commit the change to the database.
    return redirect(url_for("my_view.home")) #! Return to the route of home.

@my_view.route("/delete/<todo_id>") #! New route created for deleting. This is also the exact same as updating but we use dot notation to delete it and then commit it to the database.
def delete(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    message = "Task deleted."
    return redirect(url_for("my_view.home", message=message))

@my_view.route("/edit/<todo_id>", methods = ["GET", "POST"]) #! New route created to edit tasks using both the GET and POST methods.
def edit(todo_id):
    try: #! Try/except used for error handling
        todo = Todo.query.filter_by(id=todo_id).first() #! This will be matching the ID we give to the function when we query the database.
        if request.method == "POST": #! This if statement checks if the request method is POST.
            updated_task = request.form.get("task") #! We will use .get to retrieve the updated task and category from the user
            updated_category = request.form.get("category")
            if updated_task and updated_category: #! checking if both are not empty.
                todo.task = updated_task
                todo.category = updated_category
                db.session.commit() #! It will then commit all the changes and change them on the database.
                message = "Task updated."
                return redirect(url_for("my_view.home", message = message)) #! This will then redirect them to the home page and display the message that the task has been updated
    except:
        message = "Task cannot be empty or the same." #! Task cannot be the same or empty and message will be displayed.
        return redirect(url_for("my_view.home", message = message))
    return render_template("edit.html", todo = todo) #! Will then pass the todo object and will return to the home page with changes made.


