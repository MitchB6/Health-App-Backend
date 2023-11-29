from ..extensions import db

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