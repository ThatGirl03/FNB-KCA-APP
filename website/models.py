from datetime import datetime
from sqlalchemy import TIMESTAMP, Column, Integer, String, Float, Text, ForeignKey
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from website import db
from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash, check_password_hash

class Note(db.Model):
    id = Column(Integer, primary_key=True)
    data = Column(String(10000))
    date = Column(TIMESTAMP(timezone=True), default=func.now())
    user_id = Column(Integer, ForeignKey('user.id'))

class User(db.Model, UserMixin):
    id = Column(Integer, primary_key=True)
    firstname = Column(String(120))
    lastname = Column(String(120))
    email = Column(String(150), unique=True)
    password = Column(String(130))
    notes = relationship('Note', backref='user', lazy=True)
    profile = relationship('UserProfile', back_populates='user', uselist=False)

class UserProfile(db.Model):
    id = Column(Integer, primary_key=True)
    firstname = Column(String(50))
    lastname = Column(String(50))
    bio = Column(String(200))
    location = Column(String(100))
    workplace = Column(String(100))
    education = Column(String(100))
    highlights = Column(String(200))
    linkedin = Column(String(200))
    facebook = Column(String(200))
    instagram = Column(String(200))
    cover_photo = Column(String(200))
    media_upload = Column(String(200))
    media_type = Column(String(50))
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    user = relationship('User', back_populates='profile')
    posts = relationship('tradepost', back_populates='author', lazy=True)


class tradepost(db.Model, UserMixin):
    __tablename__ = 'trade_posts'
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    price = Column(Float, nullable=True)
    image = Column(String(100), nullable=True)
    category = Column(String(50), nullable=False)
    user_id = Column(Integer, ForeignKey('user_profile.id'), nullable=False)
    author = relationship('UserProfile', back_populates='posts')
    
    def __repr__(self):
        return f"<tradepost '{self.title}', posted by User ID {self.user_id}>"

    
class  Admin(db.Model, UserMixin):
       id = Column(Integer, primary_key=True)
       name = Column(String(100), unique=False, nullable=False)
       staff = Column(String(100), unique=True, nullable=False)
       contact_email = Column(String(150), unique=True, nullable=False)
       password = Column(String(130))
       
  

class Posts(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(150), nullable=False)
    pdf = db.Column(db.String(255), nullable=False)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return f'<Post {self.id}>'

class Save(db.Model):
         id = db.Column(db.Integer, primary_key=True)
         device_name = db.Column(db.String(100), nullable=False)  # Device name
         image = db.Column(db.String(200), nullable=False)  # Image filename
         price = db.Column(db.Float, nullable=False)  # Price in Rands
         created_at = db.Column(db.DateTime, default=datetime.utcnow)  # 

         def __repr__(self):
          return f"<SaveStorage {self.device_name} - R{self.price}>" 

class CyberPosts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(150), nullable=False)
    pdf = db.Column(db.String(255), nullable=False)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return f"<CyberPosts {self.id}>"
    
class DataPosts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(150), nullable=False)
    pdf = db.Column(db.String(255), nullable=False)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return f"<DataPosts {self.id}>"  

    
class NetworkPosts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(150), nullable=False)
    pdf = db.Column(db.String(255), nullable=False)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return f"<NetworkPosts {self.id}>"  


class QuestionPosts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(150), nullable=False)
    pdf = db.Column(db.String(255), nullable=False)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return f"<QuestionPosts {self.id}>"  


class MemoPosts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(150), nullable=False)
    pdf = db.Column(db.String(255), nullable=False)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return f"<MemoPosts {self.id}>"             
    
    