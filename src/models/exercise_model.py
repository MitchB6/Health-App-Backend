from ..extensions import db


# The `Exercise` class represents an exercise in a fitness application and provides methods for
# saving, deleting, updating, and retrieving exercises from a database.
class Exercise(db.Model):
  __tablename__ = "exercises"

  exercise_id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(255), nullable=False, unique=True)
  description = db.Column(db.Text, nullable=True)
  muscle_group = db.Column(db.String(255), nullable=True)

  stats = db.relationship("ExerciseStat", back_populates="exercise")
  workout_exercises = db.relationship(
      "WorkoutExercise", back_populates="exercise")

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
