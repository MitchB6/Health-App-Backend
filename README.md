# Health-App-Backend

# Set up your virtual environment
python -m venv venv

# Activate the environment
or you can just do it without the venv but then your base python will have a bunch of bloat

# install requirements
pip install -r requirements.txt

# set up the .env file
SECRET_KEY=secret key  
MYSQL_DATABASE_URI=mysql+pymysql://root:password@localhost:3306/db_name  
SQLALCHEMY_TRACK_MODIFICATIONS = False  

# set up the .flaskenv file
FLASK_APP=run.py  
FLASK_ENV=development  
FLASK_RUN_PORT=8000
