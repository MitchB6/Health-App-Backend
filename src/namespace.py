from flask_restx import Namespace

auth_ns=Namespace('auth',description="A namespace for Authentication")
home_ns=Namespace('home',description='A namespace for Home')
member_ns = Namespace('member', description='A namespace for Member')