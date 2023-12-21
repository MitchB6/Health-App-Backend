import re
import datetime


def validate_email(email):
  return re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email)


def validate_password(password):
  return (len(password) >= 8 and
          any(char.isdigit() for char in password) and
          any(char.isupper() for char in password) and
          any(char.islower() for char in password) and
          re.search(r"[!@#$%^&*(),.?\":{}|<>]", password))


def validate_phone(phone):
  return re.match(r"\d{10}", phone)


def validate_height(height):
  return 50 <= int(height) <= 300


def validate_weight(weight):
  return 2 <= int(weight) <= 500


def validate_zip_code(zip_code):
  return re.match(r"\d{5}", zip_code)


def validate_state(state):
  return re.match(r"[A-Z]{2}", state)


def validate_city(city):
  return re.match(r"^[a-zA-Z]+(?:[\s-][a-zA-Z]+)*$", city)


def validate_date(date):
  try:
    parsed_date = datetime.datetime.strptime(date, '%Y-%m-%d')
    return parsed_date < datetime.date.today()
  except ValueError:
    return False


def validate_birthdate(birthdate):
  try:
    parsed_birthdate = datetime.datetime.strptime(birthdate, '%Y-%m-%d').date()
    return parsed_birthdate < datetime.date.today()
  except ValueError:
    return False


def validate_username(username):
  return len(username) >= 3 and username.isalnum()


def validate_first_name(first_name):
  return len(first_name) >= 0


def validate_last_name(last_name):
  return len(last_name) >= 0


def validate_mood_level(mood_level):
  return mood_level in range(1, 11)


def validate_hydration_level(hydration_level):
  return hydration_level in range(1, 11)


def validate_calories_intake(calories_intake):
  return 0 < calories_intake <= 10000


def validate_age(age):
  return 0 < age <= 100


def validate_sets(sets):
  return 0 < sets


def validate_reps(reps):
  return reps > 0


def validate_sequence(sequence):
  return 0 < sequence <= 100


def validate_duration(duration):
  return 0 < duration <= 480  # Duration in minutes


def validate_calories_burned(calories_burned):
  return 0 < calories_burned <= 5000


def validate_workout_name(workout_name):
  return len(workout_name) > 0
