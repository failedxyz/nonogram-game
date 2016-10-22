import os


class Config:
    def __init__(self, testing=False):
        self.SQLALCHEMY_DATABASE_URI = self._get_database_url()
        self.SQLALCHEMY_TRACK_MODIFICATIONS = False
        self.SECRET_KEY = self._load_secret_key()

        if testing:
            self.TESTING = True
            self.WTF_CSRF_ENABLED = False

    def _get_database_url(self):
        return os.getenv("DATABASE_URL", "")

    def _load_secret_key(self):
        key = os.getenv("SECRET_KEY")
        if key:
            return key
        file = open(".secret_key", "a+b")
        key = file.read()
        if not key:
            key = os.urandom(128)
            file.write(key)
            file.flush()
        file.close()
        return key
