from dotenv import load_dotenv
import os

load_dotenv()

TESTING = os.getenv("TESTING", "false").lower() == "true"
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "")

BASE_URL = "https://www.kalibrr.com"