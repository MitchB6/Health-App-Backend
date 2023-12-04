from ..models.coach_model import CoachInfo

# Function to get all coaches


def get_all_coaches():
  coaches = CoachInfo.all_coaches()
  serialized_coaches = [coach.serialize() for coach in coaches]
  return serialized_coaches, 200

# Function to get a coach by coach_id


def get_coach(coach_id):
  coach = CoachInfo.query.get(coach_id)
  if coach:
    serialized_coach = coach.serialize()
    return serialized_coach, 200
  else:
    return {"message": "Coach not found"}, 404
