from .database import db

class User(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, autoincrement = True, primary_key = True, unique = True)
    username = db.Column(db.String, nullable = False, unique = True)
    password = db.Column(db.String, nullable = False)
    email = db.Column(db.String, nullable = False, unique = True)
    lists = db.relationship("Lists", backref = 'user', lazy = True)

class Lists(db.Model):
    __tablename__ = "lists"
    list_id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable = False)
    list_title = db.Column(db.String, nullable = False)
    list_description = db.Column(db.String, nullable = False)
    cards = db.relationship("Cards", backref = "lists", lazy = True, cascade='all,delete-orphan')

class Cards(db.Model):
    __tablename__ = "cards"
    card_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    list_id = db.Column(db.Integer, db.ForeignKey("lists.list_id"), nullable = False)
    card_title = db.Column(db.String, nullable = False)
    card_content = db.Column(db.String(100), nullable=False)
    deadline = db.Column(db.Date, nullable = False)
    status = db.Column(db.String, nullable = False, default = "To-Do") # To-Do, In-Progress, Completed
    created_date = db.Column(db.Date, nullable = False)
    updated_date = db.Column(db.Date, nullable = False)
    completed_date = db.Column(db.Date, nullable = True)
    
    @property
    def is_not_started(self):
        return self.status == "To-Do"

    @property
    def is_in_progress(self):
        return self.status == "In-Progress"

    @property
    def is_completed(self):
        return self.status == "Completed"

    @property 
    def is_overdue(self):
        from datetime import date
        return not self.is_completed and self.deadline < date.today()