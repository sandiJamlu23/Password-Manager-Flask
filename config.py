import os

DATABASE_URL = os.environ.get('DATABASE_URL') or 'sqlite:///passwords.db'