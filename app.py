from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os
 
app = Flask(__name__)
 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
 
class FileData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(150), nullable=False)
    lines = db.Column(db.Integer, nullable=False)
    words = db.Column(db.Integer, nullable=False)
    characters = db.Column(db.Integer, nullable=False)
 

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
 
@app.route('/')
def index():
    return render_template('upload.html')
 
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(url_for('index'))
 
    file = request.files['file']
    if file.filename == '':
        return redirect(url_for('index'))
 
    # Save the file to the uploads folder
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)
 
    # Read the file and calculate metrics
    try:
        with open(filepath, 'r') as f:
            content = f.read()
    except Exception as e:
        return f"Error reading file: {e}"
 
    lines = content.count('\n') + 1
    words = len(content.split())
    characters = len(content)
 
    # Insert file data into the database using SQLAlchemy
    try:
        new_file_data = FileData(
            filename=file.filename,
            lines=lines,
            words=words,
            characters=characters
        )
    
        db.session.add(new_file_data)
        db.session.commit()
 
        return f"File '{file.filename}' uploaded Sucessfully! Lines: {lines}, Words: {words}, Characters: {characters}"
    except Exception as e:
        return f"Error inserting into database: {e}"
 
if __name__ == '__main__':
    # Create the database and tables if they don't exist
    with app.app_context():
        print("Initializing the database...")
        try:
            db.create_all()
            print("Database and tables should now be created.")
        except Exception as e:
            print(f"Error creating tables: {e}")
 
    app.run(debug=True)