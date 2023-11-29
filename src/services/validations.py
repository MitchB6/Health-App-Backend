import re, datetime

def validate_email(email):
  return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def validate_password(password):
  return len(password) >= 8

def validate_phone(phone):
  return re.match(r"\d{10}", phone)

def validate_height(height):
  return height > 0

def validate_weight(weight):
  return weight > 0

def validate_zip_code(zip_code):
  return re.match(r"\d{5}", zip_code)

def validate_state(state):
  return re.match(r"[A-Z]{2}", state)

def validate_city(city):
  return len(city) > 0

def validate_birthdate(birthdate): 
  return birthdate < datetime.date.today()

def validate_username(username):
  return len(username) > 0

def validate_first_name(first_name):
  return len(first_name) > 0

def validate_last_name(last_name): 
  return len(last_name) > 0