from . import db
from flask_login import UserMixin
from datetime import datetime

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer(), primary_key = True)
    username = db.Column(db.String(50), nullable= False, unique= True)
    email = db.Column(db.String(50), nullable= False, unique= True)
    password_hash = db.Column(db.Text(), nullable = False)
    urls = db.relationship('Url', backref='user', lazy=True)

    def __repr__(self) -> str:
        return f"<User {self.username}>"
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Url(db.Model):
    __tablename__ = "urls"
    id = db.Column(db.Integer(), primary_key = True)
    long_url = db.Column(db.String(), nullable= False)
    short_url = db.Column(db.String(), nullable= False, unique= True)
    clicks = db.Column(db.Integer(), nullable = False, default=0)
    title = db.Column(db.String(64) , nullable=True  )
    custom_url = db.Column(db.String(64) , nullable=True, default=None  )
    url_code = db.Column(db.String(64) , nullable=True  )
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    # date_created = db.Column(db.DateTime(), default=datetime.utcnow)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'), nullable = False)

    def __repr__(self) -> str:
        return f"<User {self.title}>"
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
