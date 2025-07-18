#To create the database

from app import app, db
from applications import models  # This ensures all models are registered

with app.app_context():
    db.create_all()
    print("All tables created.")



