import os

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


class Config:
    def __init__(self):
        self.SQLALCHEMY_DATABASE_URI = self._get_database_url()
        self.SQLALCHEMY_TRACK_MODIFICATIONS = False

    def _get_database_url(self):
        return os.getenv("DATABASE_URL", "")
