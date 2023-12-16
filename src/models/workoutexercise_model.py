from ..models.exercise_model import Exercise
from ..extensions import db

# The `WorkoutExercise` class represents a model for workout exercises in a database, with methods for
# saving, deleting, and finding exercises by workout or exercise ID.


class WorkoutExercise(db.Model):
  __tablename__ = 'workout_exercises'

  workout_exercise_id = db.Column(db.Integer, primary_key=True)
  workout_id = db.Column(db.Integer, db.ForeignKey(
      'workouts.workout_id', ondelete='CASCADE'), nullable=False)
  exercise_id = db.Column(db.Integer, db.ForeignKey(
      'exercises.exercise_id'), nullable=False)
  sets = db.Column(db.Integer, nullable=True)
  reps = db.Column(db.Integer, nullable=True)
  sequence = db.Column(db.Integer, nullable=True)
  notes = db.Column(db.Text, nullable=True)

  workout = db.relationship('Workout', back_populates='workout_exercises')
  exercise = db.relationship('Exercise', back_populates='workout_exercises')

  def serialize(self):
    exercise_info = Exercise.query.filter_by(
        exercise_id=self.exercise_id).first()
    return {
        "workout_exercise_id": self.workout_exercise_id,
        "workout_id": self.workout_id,
        "exercise_id": self.exercise_id,
        "sets": self.sets,
        "reps": self.reps,
        "sequence": self.sequence,
        "notes": self.notes,
        "name": exercise_info.name if exercise_info else None,
        "description": exercise_info.description if exercise_info else None,
        "muscle_group": exercise_info.muscle_group if exercise_info else None,
        "equipment": exercise_info.equipment if exercise_info else None,
    }

  def save(self):
    """Saves a workout exercise record to the database."""
    db.session.add(self)
    db.session.commit()

  def delete(self):
    """Deletes a workout exercise record from the database."""
    db.session.delete(self)
    db.session.commit()
