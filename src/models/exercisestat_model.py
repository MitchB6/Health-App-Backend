from ..extensions import db

# The `ExerciseStat` class represents exercise statistics and provides methods for saving, deleting,
# updating, and finding exercise stats in the database.
class ExerciseStat(db.Model):
  __tablename__ = 'exercise_stats'

  stat_id = db.Column(db.Integer, primary_key=True)
  exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.exercise_id', ondelete='CASCADE'), nullable=False)
  sets = db.Column(db.Integer)
  reps = db.Column(db.Integer)
  weight = db.Column(db.Numeric(10, 2))
  duration = db.Column(db.Integer)  
  recorded_at = db.Column(db.DateTime, server_default=db.func.now())

  exercise = db.relationship('Exercise', back_populates='stats')

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