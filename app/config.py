import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-prod")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "mysql+pymysql://wedding_user:wedding_pass@localhost:3306/wedding_db",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    GOOGLE_AI_API_KEY = os.environ.get("GOOGLE_AI_API_KEY", "")

    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "static", "uploads")
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max upload
