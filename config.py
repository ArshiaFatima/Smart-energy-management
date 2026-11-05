import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "mysql+pymysql://root:password@localhost:3306/smart_energy_assignment3"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
