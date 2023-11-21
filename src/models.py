from .extensions import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

class Member(db.Model):
  __tablename__ = 'members'
  
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

  passwords = relationship('Password', back_populates='member', uselist=False)
  member_goals = relationship('MemberGoal', back_populates='member')
  member_progress = relationship('MemberProgress', back_populates='member')
  coaches = relationship('CoachInfo', secondary='coaches_members_link', back_populates='members')
  goals = relationship('MemberGoals', back_populates='member', order_by='MemberGoals.target_date')
  workouts = relationship('Workout', back_populates='member', order_by='Workout.workout_date')
  workout_plans = relationship('WorkoutPlan', back_populates='member', order_by='WorkoutPlan.start_date')
    
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
    
  """Indexing"""

class Password(db.Model):
  __tablename__ = 'passwords'
  
  pw_member_id = db.Column(db.Integer, ForeignKey('members.member_id'), primary_key=True)
  hashed_pw = db.Column(db.String(255), nullable=False)
  created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
  updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
  password_reset_token = db.Column(db.String(64), nullable=True)
  password_reset_expiration = db.Column(db.DateTime, nullable=True)

  member = relationship("Member", back_populates="passwords")
  
  """Encapsulation methods and Indexing"""

class Exercise(db.Model):
  __tablename__ = 'exercises'

  exercise_id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(255), nullable=False)
  description = db.Column(db.Text, nullable=True)
  muscle_group = db.Column(db.String(255), nullable=True)

  exercise_stats = db.relationship('ExerciseStat', back_populates='exercise')
  workout_exercises = db.relationship('WorkoutExercise', back_populates='exercise')
  
  """Encapsulation methods and Indexing"""
   
class CoachInfo(db.Model):
  __tablename__ = 'coach_info'
  
  coach_id = db.Column(db.Integer, primary_key=True)
  member_id = db.Column(db.Integer, db.ForeignKey('members.member_id'), nullable=False)
  email = db.Column(db.String(255), nullable=False)
  phone = db.Column(db.String(20))
  specialization = db.Column(db.Text)
  price = db.Column(db.Numeric(10, 2))
  location = db.Column(db.Text)
  schedule_text = db.Column(db.Text)
  qualifications = db.Column(db.Text)
  
  member = relationship('Member', back_populates='coach_info')
  member_coach_link = relationship('Member', secondary='coaches_members_link', back_populates='coaches')
  availabilities = relationship('Availability', back_populates='coach_info', order_by='Availability.start_time')
  
  """Encapsulation methods and Indexing"""

class CoachesMembersLink(db.Model):
  __tablename__ = 'coaches_members_link'

  link_id = db.Column(db.Integer, primary_key=True)
  coach_id = db.Column(db.Integer, db.ForeignKey('coach_info.coach_id'), nullable=False)
  member_id = db.Column(db.Integer, db.ForeignKey('members.member_id'), nullable=False)
  
  """Indexing"""

class Availability(db.Model):
  __tablename__ = 'availability'

  availability_id = db.Column(db.Integer, primary_key=True)
  coach_id = db.Column(db.Integer, db.ForeignKey('coach_info.coach_id'), nullable=False)
  start_time = db.Column(db.DateTime, nullable=False)
  end_time = db.Column(db.DateTime, nullable=False)

  coach_info = relationship('CoachInfo', back_populates='availabilities')
  
  """Encapsulation methods and Indexing"""

class MemberGoals(db.Model):
  __tablename__ = 'member_goals'

  member_goal_id = db.Column(db.Integer, primary_key=True)
  member_id = db.Column(db.Integer, db.ForeignKey('members.member_id'), nullable=False)
  goal_description = db.Column(db.Text, nullable=False)
  target_date = db.Column(db.Date, nullable=False)
  goal_type = db.Column(db.String(50), nullable=False)

  member = relationship('Member', back_populates='goals')
  
  """Encapsulation methods and Indexing"""
    
class Workout(db.Model):
  __tablename__ = 'workouts'

  workout_id = db.Column(db.Integer, primary_key=True)
  member_id = db.Column(db.Integer, db.ForeignKey('members.member_id'), nullable=False)
  workout_name = db.Column(db.String(255), nullable=False)
  workout_date = db.Column(db.Date, nullable=False)
  energy_level = db.Column(db.Integer)
  hydration_level = db.Column(db.Integer)

  member = relationship('Member', back_populates='workouts')
  workout_plan_links = relationship('WorkoutPlanLink', back_populates='workout', order_by='WorkoutPlanLink.sequence')
  workout_stats = relationship('WorkoutStat', back_populates='workout', order_by='WorkoutStat.date')
  workout_exercises = relationship('WorkoutExercise', back_populates='workout')

  """Encapsulation methods and Indexing"""
  
class WorkoutPlan(db.Model):
  __tablename__ = 'workout_plans'

  plan_id = db.Column(db.Integer, primary_key=True)
  member_id = db.Column(db.Integer, db.ForeignKey('members.member_id'), nullable=False)
  plan_name = db.Column(db.String(255), nullable=False)
  description = db.Column(db.Text, nullable=True)
  start_date = db.Column(db.Date, nullable=False)
  end_date = db.Column(db.Date, nullable=True)

  member = relationship('Member', back_populates='workout_plans')
  workout_plan_links = relationship('WorkoutPlanLink', back_populates='workout_plan', order_by='WorkoutPlanLink.sequence')

  """Encapsulation methods and Indexing"""

class ExerciseStat(db.Model):
  __tablename__ = 'exercise_stats'

  stat_id = db.Column(db.Integer, primary_key=True)
  exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.exercise_id'), nullable=False)
  sets = db.Column(db.Integer)
  reps = db.Column(db.Integer)
  weight = db.Column(db.Numeric(10, 2))
  duration = db.Column(db.Integer)  
  recorded_at = db.Column(db.DateTime, server_default=db.func.now())

  exercise = relationship('Exercise', back_populates='stats')
  exercise_stats = relationship('Exercise', back_populates='exercise_stats')

  """Encapsulation methods"""

class WorkoutPlanLink(db.Model):
  __tablename__ = 'workout_plan_links'

  link_id = db.Column(db.Integer, primary_key=True)
  plan_id = db.Column(db.Integer, db.ForeignKey('workout_plans.plan_id'), nullable=False)
  workout_id = db.Column(db.Integer, db.ForeignKey('workouts.workout_id'), nullable=False)
  sequence = db.Column(db.Integer, nullable=False)

  workout_plan = relationship('WorkoutPlan', back_populates='workout_plan_links')
  workout = relationship('Workout', back_populates='workout_plan_links')

  """Encapsulation methods and Indexing"""
  
class WorkoutStat(db.Model):
  __tablename__ = 'workout_stats'

  stat_id = db.Column(db.Integer, primary_key=True)
  workout_id = db.Column(db.Integer, db.ForeignKey('workouts.workout_id'), nullable=False)
  duration = db.Column(db.Integer)  
  calories_burned = db.Column(db.Integer) 
  date = db.Column(db.DateTime, default=db.func.current_timestamp())  

  workout = relationship('Workout', back_populates='workout_stats')
  
  """Encapsulation methods"""
  
class WorkoutExercise(db.Model):
  __tablename__ = 'workout_exercises'

  workout_exercise_id = db.Column(db.Integer, primary_key=True)
  workout_id = db.Column(db.Integer, db.ForeignKey('workouts.workout_id'), nullable=False)
  exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.exercise_id'), nullable=False)
  sets = db.Column(db.Integer, nullable=True)
  reps = db.Column(db.Integer, nullable=True)
  notes = db.Column(db.Text, nullable=True)

  workout = relationship('Workout', back_populates='workout_exercises')
  exercise = relationship('Exercise', back_populates='workout_exercises')
  
  """Encapsulation methods"""