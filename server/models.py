from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators 
    @validates('name')
    def validate_name(self, key, value):
        if not value:
            raise ValueError("It cannot be empty")
        if db.session.query(Author).filter(Author.name == value).filter(Author.id != self.id).count() > 0:
            raise ValueError("name already exists")
        return value
    
    @validates('phone_number')
    def validate_phone_number(self, key, phone_number):
       if phone_number and (not phone_number.isdigit() or len(phone_number) != 10):
           raise ValueError("Phone number must be 10 digits")
       return phone_number
    
    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators  
    @validates('title')
    def validate_title(self, key, value):
        if not value:
            raise ValueError("Post must have a title.")
        clickbait_keywords = ["Won't Believe", "Secret", "Top", "Guess"]
        if not any(keyword in value for keyword in clickbait_keywords):
            raise ValueError("Post title must contain either of the following: 'Won't Believe', 'Secret', 'Top', 'Guess'")
        return value
    
    @validates('content')
    def validate_content(self, key, value):
        if len(value) < 250:
            raise ValueError("Post content must be at least 250 characters")
        return value

    @validates('summary')
    def validate_summary(self, key, value):
        if len(value) > 250:
            raise ValueError("Post summary cannot be more than 250 characters.")
        return value

    @validates('category')
    def validate_category(self, key, value):
        valid_categories = ["Fiction", "Non-Fiction"]
        if value not in valid_categories:
            raise ValueError("Post category must be either 'Fiction' or 'Non-Fiction'.")
        return value


    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
