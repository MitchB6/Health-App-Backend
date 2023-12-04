
from ..models.coach_model import CoachInfo
from ..extensions import db


def update_coach(data):
  try:
    approved = bool(data.get('approved'))
    coach_id = data.get('coach_id')

    if coach_id is None:
      return {"message": "Coach not found"}, 404

    coach = CoachInfo.query.get_or_404(coach_id, description="Coach not found")

    if approved:
      print("APPROVAL", approved)
      coach.approved = approved
      coach.member.role_id = 1
      db.session.commit()
      return {"message": "Coach approved"}, 200
    else:
      db.CoachInfo.delete(coach)
      return {"message": "Coach denied"}, 200
  except Exception as e:
    return {"error": str(e)}, 500


def get_all_coach_forms():
  try:
    forms = CoachInfo.query.filter_by(approved=False).all()
    serialized_forms = [form.serialize() for form in forms]
    return serialized_forms, 200
  except Exception as e:
    return {"error": str(e)}, 500
