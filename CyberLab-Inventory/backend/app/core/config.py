import os
from dotenv import load_dotenv

load_dotenv()

# Configuration générale de l'application
DATABASE_URL = os.getenv("DATABASE_URL")
APP_NAME = os.getenv("APP_NAME", "CyberLab CMDB API")
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# Configuration de la sécurité et des JWT
SECRET_KEY = os.getenv("SECRET_KEY", "super_secret_key_change_me_in_production_123456")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
