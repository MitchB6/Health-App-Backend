from ..extensions import db
  
# The `WorkoutExercise` class represents a model for workout exercises in a database, with methods for
# saving, deleting, and finding exercises by workout or exercise ID.
class WorkoutExercise(db.Model):
  __tablename__ = 'workout_exercises'

  workout_exercise_id = db.Column(db.Integer, primary_key=True)
  workout_id = db.Column(db.Integer, db.ForeignKey('workouts.workout_id', ondelete='CASCADE'), nullable=False)
  exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.exercise_id'), nullable=False)
  sets = db.Column(db.Integer, nullable=True)
  reps = db.Column(db.Integer, nullable=True)
  notes = db.Column(db.Text, nullable=True)

  workout = db.relationship('Workout', back_populates='workout_exercises')
  exercise = db.relationship('Exercise', back_populates='workout_exercises')
  
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
  