from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from .extensions import db

# The `Member` class represents a member in a database, with various attributes and relationships to
# other tables.
class Member(db.Model):
  __tablename__ = 'members'

  member_id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(100), nullable=True)
  first_name = db.Column(db.String(100), nullable=True)
  last_name = db.Column(db.String(100), nullable=True)
  email = db.Column(db.String(255), nullable=False, unique=True)
  phone = db.Column(db.String(20), nullable=True)
  role_id = db.Column(db.Boolean, nullable=False, default=False)
  city = db.Column(db.String(100), nullable=True)
  state = db.Column(db.String(100), nullable=True)
  zip_code = db.Column(db.String(20), nullable=True)
  join_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
  birthdate = db.Column(db.Date, nullable=True)
  height = db.Column(db.Integer, nullable=True)  
  weight = db.Column(db.Integer, nullable=True)

  passwords = relationship('Password', back_populates='member', uselist=False)
  coaches = relationship('CoachInfo', secondary='coaches_members_link', back_populates='member')
  coach_info = relationship('CoachInfo', back_populates='member')
  goals = relationship('MemberGoals', back_populates='member')
  workouts = relationship('Workout', back_populates='member')
  workout_plans = relationship('WorkoutPlan', back_populates='member')

  def __repr__(self):
    """String representation of a Member instance."""
    return f"<Member {self.first_name} {self.last_name}>"

  def save(self, flush=False, commit=False):
    """Saves the Member instance. Use 'flush' to get member_id without committing"""
    db.session.add(self)
    if flush:
      db.session.flush()
    if commit:
      db.session.commit()
  
  def delete(self):
    """ Permanently delete the member """
    db.session.delete(self)
    db.session.commit()
    
  def update(self, **kwargs):
    """Updates Member attributes specified in 'kwargs'."""
    for key, value in kwargs.items():
      if hasattr(self, key) and value is not None:
        setattr(self, key, value)
    db.session.commit()

# The `Password` class represents a table in a database that stores password information for members,
# including hashed passwords, creation and update timestamps, password reset tokens, and expiration
# dates.
class Password(db.Model):
  __tablename__ = 'passwords'
  
  member_id = db.Column(db.Integer, ForeignKey('members.member_id'), primary_key=True)
  hashed_pw = db.Column(db.String(255), nullable=False)
  created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
  updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
  password_reset_token = db.Column(db.String(64), nullable=True)
  password_reset_expiration = db.Column(db.DateTime, nullable=True)

  member = relationship("Member", back_populates="passwords")
  
  def __init__(self, **kwargs):
    """Initialize a Password instance."""
    super().__init__(**kwargs)
    
  def save(self):
    """Saves the Password instance to the DB."""
    db.session.add(self)
    db.session.commit()

  def delete(self):
    """Deletes the Password instance from the DB."""
    db.session.delete(self)
    db.session.commit()

# The `Exercise` class represents an exercise in a fitness application and provides methods for
# saving, deleting, updating, and retrieving exercises from a database.
class Exercise(db.Model):
  __tablename__ = 'exercises'

  exercise_id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(255), nullable=False)
  description = db.Column(db.Text, nullable=True)
  muscle_group = db.Column(db.String(255), nullable=True)

  stats = db.relationship('ExerciseStat', back_populates='exercise')
  workout_exercises = db.relationship('WorkoutExercise', back_populates='exercise')
  
  def save(self):
    """Saves the exercise to the database."""
    db.session.add(self)
    db.session.commit()

  def delete(self):
    """Deletes the exercise from the database."""
    db.session.delete(self)
    db.session.commit()

  def update(self, **kwargs):
    """Updates exercise attributes with given keyword arguments."""
    for key, value in kwargs.items():
      if hasattr(self, key) and value is not None:
        setattr(self, key, value)
    db.session.commit()
    
  @classmethod
  def find_by_name(cls, name):
    """Finds an exercise by its name."""
    return cls.query.filter_by(name=name).first()

  @classmethod
  def all_exercises(cls):
    """Returns all exercises."""
    return cls.query.all()

  @classmethod
  def exercises_by_muscle_group(cls, muscle_group):
    """Returns exercises for a specific muscle group."""
    return cls.query.filter_by(muscle_group=muscle_group).all()
   
# The CoachInfo class represents coach information in a database and provides methods for saving,
# deleting, updating, and retrieving coach data.
class CoachInfo(db.Model):
  __tablename__ = 'coach_info'
  
  coach_id = db.Column(db.Integer, primary_key=True)
  member_id = db.Column(db.Integer, ForeignKey('members.member_id'), nullable=False)
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
  
  def save(self, flush=False, commit=False):
    """Saves coach information to the database."""
    db.session.add(self)
    if flush:
      db.session.flush()
    if commit:
      db.session.commit()

  def delete(self):
    """Deletes coach information from the database."""
    db.session.delete(self)
    db.session.commit()

  def update(self, **kwargs):
    """Updates coach attributes with given keyword arguments."""
    for key, value in kwargs.items():
      if hasattr(self, key) and value is not None:
        setattr(self, key, value)
    db.session.commit()
    
    @classmethod
    def all_coaches(cls):
      """Returns all registered coaches."""
      return cls.query.all()

# The `CoachesMembersLink` class is a model that represents the link between coaches and members in a
# database, providing methods to create, remove, and find links between them.
class CoachesMembersLink(db.Model):
  __tablename__ = 'coaches_members_link'

  link_id = db.Column(db.Integer, primary_key=True)
  coach_id = db.Column(db.Integer, db.ForeignKey('coach_info.coach_id'), nullable=False)
  member_id = db.Column(db.Integer, db.ForeignKey('members.member_id'), nullable=False)
  
  @classmethod
  def create_link(cls, coach_id, member_id):
    """Add new link if DNE"""
    existing_link = cls.query.filter_by(coach_id=coach_id, member_id=member_id).first()
    if not existing_link:
      new_link = cls(coach_id=coach_id, member_id=member_id)
      db.session.add(new_link)
      db.session.commit()
      return new_link
    return existing_link  # or handle this case as needed
  
  @classmethod
  def remove_link(cls, coach_id, member_id):
    """Remove link if exists"""
    link_to_remove = cls.query.filter_by(coach_id=coach_id, member_id=member_id).first()
    if link_to_remove:
      db.session.delete(link_to_remove)
      db.session.commit()

  @classmethod
  def find_coaches_by_member(cls, member_id):
    """Find coaches for specific member"""
    links = cls.query.filter_by(member_id=member_id).all()
    coach_ids = [link.coach_id for link in links]
    return CoachInfo.query.filter(CoachInfo.coach_id.in_(coach_ids)).all()

  @classmethod
  def find_members_by_coach(cls, coach_id):
    """Find members for specific coach"""
    links = cls.query.filter_by(coach_id=coach_id).all()
    member_ids = [link.member_id for link in links]
    return Member.query.filter(Member.member_id.in_(member_ids)).all()

# The `Availability` class represents the availability of a coach and provides methods for saving,
# deleting, and finding availabilities, as well as checking for overlapping availabilities.
class Availability(db.Model):
  __tablename__ = 'availability'

  availability_id = db.Column(db.Integer, primary_key=True)
  coach_id = db.Column(db.Integer, db.ForeignKey('coach_info.coach_id'), nullable=False)
  start_time = db.Column(db.DateTime, nullable=False)
  end_time = db.Column(db.DateTime, nullable=False)

  coach_info = relationship('CoachInfo', back_populates='availabilities')
  
  def save(self):
    """Save or update availability."""
    self.check_availability_overlap()
    db.session.add(self)
    db.session.commit()

  def delete(self):
    """Delete availability."""
    db.session.delete(self)
    db.session.commit()
  
  @classmethod
  def find_by_coach(cls, coach_id):
    """Find all availabilities for a specific coach."""
    return cls.query.filter_by(coach_id=coach_id).all()

  def check_availability_overlap(self):
    """Check for overlapping availability."""
    overlapping = Availability.query.filter(
      Availability.coach_id == self.coach_id,
      Availability.start_time < self.end_time,
      Availability.end_time > self.start_time
    ).first()
    if overlapping and overlapping.availability_id != self.availability_id:
      raise ValueError("This time slot overlaps with an existing availability.")
          
# The `MemberGoals` class represents a table in a database that stores goals for members, with methods
# for saving, deleting, and finding goals, as well as a property to check if a goal's deadline has
# passed.
class MemberGoals(db.Model):
  __tablename__ = 'member_goals'

  member_goal_id = db.Column(db.Integer, primary_key=True)
  member_id = db.Column(db.Integer, db.ForeignKey('members.member_id'), nullable=False)
  goal_description = db.Column(db.Text, nullable=False)
  target_date = db.Column(db.Date, nullable=False)
  goal_type = db.Column(db.String(50), nullable=False)

  member = relationship('Member', back_populates='goals')
  
  def save(self, commit=True):
    """Save or update a member goal."""
    db.session.add(self)
    if commit:
      db.session.commit()

  def delete(self):
    """Delete a member goal."""
    db.session.delete(self)
    db.session.commit()

  @classmethod
  def find_by_member(cls, member_id):
    """Find all goals for a specific member."""
    return cls.query.filter_by(member_id=member_id).all()

  @property
  def is_goal_deadline_passed(self):
    """Check if the goal deadline has passed."""
    return self.target_date < datetime.date.today()
    
# The `Workout` class represents a workout entity in a database, with various attributes and methods
# for saving, deleting, and linking workouts to workout plans.
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

  def save(self, commit=True):
    """Save or update a workout."""
    db.session.add(self)
    if commit:
      db.session.commit()
      
  def delete(self):
        """Delete a workout."""
        db.session.delete(self)
        db.session.commit()

  @classmethod
  def find_by_member(cls, member_id):
    """Find all workouts for a specific member."""
    return cls.query.filter_by(member_id=member_id).all()

  def link_to_workout_plan(self, plan_id, sequence, commit=True):
    """Link workout to a workout plan."""
    link = WorkoutPlanLink(workout_id=self.workout_id, plan_id=plan_id, sequence=sequence)
    db.session.add(link)
    if commit:
      db.session.commit()

  def unlink_from_workout_plan(self, plan_id, commit=True):
    """Unlink workout from a workout plan."""
    link = WorkoutPlanLink.query.filter_by(workout_id=self.workout_id, plan_id=plan_id).first()
    if link:
      db.session.delete(link)
      if commit:
        db.session.commit()

# The `WorkoutPlan` class represents a workout plan in a database, with methods for saving, deleting,
# linking and unlinking workouts, and retrieving linked workouts.
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

  def save(self, commit=True):
    """Save or update a workout plan."""
    db.session.add(self)
    if commit:
      db.session.commit()

  def delete(self):
    """Delete a workout plan."""
    db.session.delete(self)
    db.session.commit()

  def link_workout(self, workout_id, sequence, commit=True):
    """Link a workout to this workout plan."""
    link = WorkoutPlanLink(plan_id=self.plan_id, workout_id=workout_id, sequence=sequence)
    db.session.add(link)
    if commit:
      db.session.commit()

  def unlink_workout(self, workout_id, commit=True):
    """Unlink a workout from this workout plan."""
    link = WorkoutPlanLink.query.filter_by(plan_id=self.plan_id, workout_id=workout_id).first()
    if link:
      db.session.delete(link)
      if commit:
        db.session.commit()

  def get_workouts(self):
    """Retrieve all workouts linked to this workout plan."""
    return [link.workout for link in self.workout_plan_links]

# The `ExerciseStat` class represents exercise statistics and provides methods for saving, deleting,
# updating, and finding exercise stats in the database.
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

  def save(self):
    """Saves exercise stat to the database."""
    db.session.add(self)
    db.session.commit()
        
  def delete(self):
    """Deletes exercise stat from the database."""
    db.session.delete(self)
    db.session.commit()

  def update(self, **kwargs):
      """Updates exercise stats with given keyword arguments."""
      for key, value in kwargs.items():
          if hasattr(self, key) and value is not None:
              setattr(self, key, value)
      db.session.commit()

  @classmethod
  def find_by_exercise_id(cls, exercise_id):
      """Finds exercise stats by exercise ID."""
      return cls.query.filter_by(exercise_id=exercise_id).all()

  @classmethod
  def find_by_stat_id(cls, recorded_at):
      """Finds a specific exercise stat by its ID."""
      return cls.query.get(recorded_at)

# The `WorkoutPlanLink` class represents a link between a workout plan and a workout in a database,
# with methods for saving, deleting, and finding links.
class WorkoutPlanLink(db.Model):
  __tablename__ = 'workout_plan_links'

  link_id = db.Column(db.Integer, primary_key=True)
  plan_id = db.Column(db.Integer, db.ForeignKey('workout_plans.plan_id'), nullable=False)
  workout_id = db.Column(db.Integer, db.ForeignKey('workouts.workout_id'), nullable=False)
  sequence = db.Column(db.Integer, nullable=False)

  workout_plan = relationship('WorkoutPlan', back_populates='workout_plan_links')
  workout = relationship('Workout', back_populates='workout_plan_links')

  def save(self, commit=False):
    """Saves a workout plan link to the database."""
    db.session.add(self)
    if commit:
      db.session.commit()

  def delete(self):
    """Deletes a workout plan link from the database."""
    db.session.delete(self)
    db.session.commit()

  @classmethod
  def find_by_plan_id(cls, plan_id):
    """Finds all workout plan links for a given plan ID."""
    return cls.query.filter_by(plan_id=plan_id).all()

  @classmethod
  def find_by_workout_id(cls, workout_id):
    """Finds all workout plan links for a given workout ID."""
    return cls.query.filter_by(workout_id=workout_id).all()

  @classmethod
  def find_link(cls, plan_id, workout_id):
    """Finds a specific link between a workout plan and a workout."""
    return cls.query.filter_by(plan_id=plan_id, workout_id=workout_id).first()
  
# The `WorkoutStat` class represents a workout statistic and provides methods for saving, deleting,
# and finding workout stats in the database.
class WorkoutStat(db.Model):
  __tablename__ = 'workout_stats'

  stat_id = db.Column(db.Integer, primary_key=True)
  workout_id = db.Column(db.Integer, db.ForeignKey('workouts.workout_id'), nullable=False)
  duration = db.Column(db.Integer)  
  calories_burned = db.Column(db.Integer) 
  date = db.Column(db.DateTime, default=db.func.current_timestamp())  

  workout = relationship('Workout', back_populates='workout_stats')
  
  def save(self, commit=False):
    """Saves a workout statistic to the database."""
    db.session.add(self)
    if commit:
      db.session.commit()

  def delete(self):
    """Deletes a workout statistic from the database."""
    db.session.delete(self)
    db.session.commit()

  @classmethod
  def find_by_workout_id(cls, workout_id):
    """Finds all stats for a given workout ID."""
    return cls.query.filter_by(workout_id=workout_id).all()

  @classmethod
  def find_stat(cls, stat_id):
    """Finds a specific workout stat by its ID."""
    return cls.query.get(stat_id)
  
# The `WorkoutExercise` class represents a model for workout exercises in a database, with methods for
# saving, deleting, and finding exercises by workout or exercise ID.
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
  
  def save(self, commit=False):
    """Saves a workout exercise record to the database."""
    db.session.add(self)
    if commit:
        db.session.commit()

  def delete(self):
    """Deletes a workout exercise record from the database."""
    db.session.delete(self)
    db.session.commit()

  @classmethod
  def find_by_workout_id(cls, workout_id):
    """Finds all exercises for a given workout ID."""
    return cls.query.filter_by(workout_id=workout_id).all()

  @classmethod
  def find_by_exercise_id(cls, exercise_id):
    """Finds all workouts for a given exercise ID."""
    return cls.query.filter_by(exercise_id=exercise_id).all()
  