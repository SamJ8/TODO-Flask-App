from . import db
from datetime import datetime

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    task = db.Column(db.String(60), unique = True)
    complete = db.Column(db.Boolean, default = False)
    category = db.Column(db.String(100))
    date = db.Column(db.DateTime, default=datetime.now)

    #! Creation of our Todo class. This will use inheritance to inherit db.Model
    #! The properties we have set above will become columns and set what data types the columns will be
    #! The id is set as a primary key because it is unique and unchanging and used to identify each row
    #! I have also set new columns for completing of task, task category and the date task was made