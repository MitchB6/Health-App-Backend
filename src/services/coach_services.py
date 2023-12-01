from flask import jsonify
from ..models.coach_model import CoachInfo, db


def get_all_coaches():
  """Get a list of all registered coaches."""
  coaches = CoachInfo.query.all()
  coach_list = []

  for coach in coaches:
    coach_info = {
        'coach_id': coach.coach_id,
        'specialization': coach.specialization,
        'price': float(coach.price),
        'location': coach.location,
        'schedule_text': coach.schedule_text,
        'qualifications': coach.qualifications,
        'member_id': coach.member_id  # You may include additional coach information here
    }
    coach_list.append(coach_info)

  return jsonify(coach_list)


def get_coach(coach_id):
  """Get details of a specific coach by coach_id."""
  coach = CoachInfo.query.get(coach_id)

  if not coach:
    return jsonify({'error': 'Coach not found'}), 404

  coach_info = {
      'coach_id': coach.coach_id,
      'specialization': coach.specialization,
      'price': float(coach.price),
      'location': coach.location,
      'schedule_text': coach.schedule_text,
      'qualifications': coach.qualifications,
      'member_id': coach.member_id  # You may include additional coach information here
  }

  return jsonify(coach_info)


def create_coach(data):
  """Create a new coach."""
  specialization = data.get('specialization')
  price = data.get('price')
  location = data.get('location')
  schedule_text = data.get('schedule_text')
  qualifications = data.get('qualifications')
  member_id = data.get('member_id')

  if not all([specialization, price, location, schedule_text, qualifications, member_id]):
    return jsonify({'error': 'Missing data'}), 400

  new_coach = CoachInfo(
      specialization=specialization,
      price=price,
      location=location,
      schedule_text=schedule_text,
      qualifications=qualifications,
      member_id=member_id
  )

  db.session.add(new_coach)
  db.session.commit()

  return jsonify({'message': 'Coach created successfully'}), 201


def update_coach(coach_id, data):
  """Update a coach's information."""
  coach = CoachInfo.query.get(coach_id)

  if not coach:
    return jsonify({'error': 'Coach not found'}), 404

  coach.specialization = data.get('specialization', coach.specialization)
  coach.price = data.get('price', coach.price)
  coach.location = data.get('location', coach.location)
  coach.schedule_text = data.get('schedule_text', coach.schedule_text)
  coach.qualifications = data.get('qualifications', coach.qualifications)
  coach.member_id = data.get('member_id', coach.member_id)

  db.session.commit()

  return jsonify({'message': 'Coach updated successfully'})


def delete_coach(coach_id):
  """Delete a coach by coach_id."""
  coach = CoachInfo.query.get(coach_id)

  if not coach:
    return jsonify({'error': 'Coach not found'}), 404

  db.session.delete(coach)
  db.session.commit()

  return jsonify({'message': 'Coach deleted successfully'})
