from ..models.coach_model import CoachInfo
from ..models.coachmemberslink_model import CoachesMembersLink
from ..extensions import db


def get_all_clients():
  query = CoachesMembersLink.query.filter_by(status='approved')
  clients = query.all()

  if clients:
    serialized_clients = [clients.serialize_members() for clients in clients]
  else:
    return serialized_clients, 404

  return serialized_clients, 200


def search_coaches(specialization=None, price=0.00, location=None):
  query = CoachInfo.query.filter_by(approved=True)

  if specialization:
    query = query.filter_by(specialization=specialization)

  if price is not None:
    price = float(price)
    if price > 0.00:
      query = query.filter(CoachInfo.price <= price)

  if location:
    query = query.filter_by(location=location)

  coaches = query.all()

  if coaches:
    serialized_coaches = [coach.serialize() for coach in coaches]
    return serialized_coaches, 200
  else:
    return {"message": "No coaches found"}, 404
