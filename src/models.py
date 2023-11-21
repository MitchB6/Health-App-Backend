from .extensions import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

class Member(db.Model):
    __tablename__ = 'members'
    
    # Columns
    member_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    phone = db.Column(db.String(20), nullable=True)
    is_coach = db.Column(db.Boolean, nullable=False, default=False)
    city = db.Column(db.String(100), nullable=True)
    state = db.Column(db.String(100), nullable=True)
    zip_code = db.Column(db.String(20), nullable=True)
    join_date = db.Column(db.DateTime, nullable=False)
    birthdate = db.Column(db.Date, nullable=True)
    height = db.Column(db.Integer, nullable=True)  
    weight = db.Column(db.Integer, nullable=True)  
    birthdate = db.Column(db.Date, nullable=True)  

    # Relationships
    """
    Password table: foreign key member_id, one to one
    Workout Plans: foreign key member_id, one to many
    Member Goal: foreign key member_id, one to many
    Member Progress: foreign key member_id, one to many
    """
    passwords = relationship('Password', back_populates='member', uselist=False)
    workout_plans = relationship('WorkoutPlan', back_populates='member')
    member_goals = relationship('MemberGoal', back_populates='member')
    member_progress = relationship('MemberProgress', back_populates='member')
    
    def __repr__(self):
        return f"<Member {self.first_name} {self.last_name}>"

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        
    def update(self, first_name, last_name, email):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        db.session.commit()

class Password(db.Model):
    __tablename__ = 'passwords'
    
    # Columns
    pw_member_id = db.Column(db.Integer, ForeignKey('members.member_id'), primary_key=True)
    hashed_pw = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    password_reset_token = db.Column(db.String(64), nullable=True)
    password_reset_expiration = db.Column(db.DateTime, nullable=True)

    # Relationships
    member = relationship("Member", back_populates="passwords")

class Exercise(db.Model):
    __tablename__ = 'exercises'
    
    exercise_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    muscle_group = db.Column(db.String(255), nullable=True)
    
    workout_exercises = relationship('WorkoutExercise', backref='exercise', lazy='dynamic')

def init_app(app):
    db.init_app(app)