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
