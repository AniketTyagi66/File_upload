from flask import Flask
from flask_sqlalchemy import SQLAlchemy
 
app = Flask(__name__)
 
# Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
 
# Define the FileData model
class FileData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(150), nullable=False)
    lines = db.Column(db.Integer, nullable=False)
    words = db.Column(db.Integer, nullable=False)
    characters = db.Column(db.Integer, nullable=False)
 
if __name__ == '__main__':
    with app.app_context():
        print("Creating tables...")
        try:
            db.create_all()
            print("Tables created successfully.")
        except Exception as e:
            print(f"Error creating tables: {e}")