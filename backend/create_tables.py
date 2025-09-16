# create_tables.py
from app.database import engine
from models.hazard import Base # Import Base from your models file

print("Creating database tables...")
Base.metadata.create_all(bind=engine)
print("Tables created successfully.")