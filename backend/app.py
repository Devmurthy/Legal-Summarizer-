import os
import sqlite3
import datetime
from functools import wraps
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import bcrypt
import jwt
import tempfile

from extractor import extract_text_from_pdf, extract_text_from_image
from utils import clean_text
from ner import extract_entities
from summarizer import extractive_summary, abstractive_summary
from legal_expert import suggest_legal_acts

app = Flask(__name__)
CORS(app)

JWT_SECRET = "your_jwt_super_secret_key_that_is_long_enough_for_hs256"
DB_PATH = os.path.join(os.path.dirname(__file__), "database.sqlite")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE,
        password TEXT,
        name TEXT
    )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS timeline_events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        title TEXT,
        description TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )''')
    conn.commit()
    conn.close()

init_db()

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('authorization')
        if not auth_header:
            return jsonify({"error": "No token provided"}), 403
        try:
            token = auth_header.split(" ")[1]
            data = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
            current_user_id = data['id']
        except Exception as e:
            return jsonify({"error": "Unauthorized"}), 401
        return f(current_user_id, *args, **kwargs)
    return decorated

@app.route('/api/signup', methods=['POST'])
def signup():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    if not all([name, email, password]):
        return jsonify({"error": "All fields are required"}), 400
        
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", (name, email, hashed_password))
        user_id = cursor.lastrowid
        conn.commit()
        
        token = jwt.encode({"id": user_id, "email": email, "name": name, "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24)}, JWT_SECRET, algorithm="HS256")
        
        cursor.execute("INSERT INTO timeline_events (user_id, title, description) VALUES (?, ?, ?)", 
                       (user_id, 'Account Created', 'Welcome to Legal Summarizer!'))
        conn.commit()
        return jsonify({"message": "User created successfully", "token": token, "user": {"id": user_id, "name": name, "email": email}}), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "Email already exists"}), 400
    finally:
        conn.close()

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()
    
    if not user:
        return jsonify({"error": "Invalid email or password"}), 400
        
    user_id, user_email, hashed_password, user_name = user
    if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
        token = jwt.encode({"id": user_id, "email": user_email, "name": user_name, "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24)}, JWT_SECRET, algorithm="HS256")
        
        cursor.execute("INSERT INTO timeline_events (user_id, title, description) VALUES (?, ?, ?)", 
                       (user_id, 'Logged In', 'User logged in to the application.'))
        conn.commit()
        return jsonify({"message": "Logged in successfully", "token": token, "user": {"id": user_id, "name": user_name, "email": user_email}}), 200
    
    return jsonify({"error": "Invalid email or password"}), 400

@app.route('/api/timeline', methods=['GET'])
@token_required
def get_timeline(current_user_id):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM timeline_events WHERE user_id = ? ORDER BY timestamp DESC", (current_user_id,))
    rows = cursor.fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])

@app.route('/api/timeline', methods=['POST'])
@token_required
def add_timeline(current_user_id):
    data = request.json
    title = data.get('title')
    description = data.get('description')
    if not title:
        return jsonify({"error": "Title is required"}), 400
        
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO timeline_events (user_id, title, description) VALUES (?, ?, ?)", 
                   (current_user_id, title, description))
    conn.commit()
    conn.close()
    return jsonify({"message": "Timeline event added"}), 201

@app.route('/api/summarize', methods=['POST'])
def summarize():
    if 'document' not in request.files:
        return jsonify({"error": "No document provided"}), 400
        
    file = request.files['document']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    num_sentences = int(request.form.get("ext_num", 5))
    min_len = int(request.form.get("abs_min", 40))
    max_len = int(request.form.get("abs_max", 150))
    ocr_mode = request.form.get("ocr_mode", "Default")
    dpi = int(request.form.get("dpi", 300))
    enhance = request.form.get("enhance", "true").lower() == "true"
    
    psm = 6 if ocr_mode == "Handwritten" else 3
    oem = 1 if ocr_mode == "Handwritten" else 3
    tess_config = f"--oem {oem} --psm {psm} -l eng -c preserve_interword_spaces=1"

    text = None
    ft = file.content_type
    
    temp_dir = tempfile.gettempdir()
    temp_path = os.path.join(temp_dir, secure_filename(file.filename))
    file.save(temp_path)

    try:
        if (ft and ft == "application/pdf") or file.filename.lower().endswith('.pdf'):
            text = extract_text_from_pdf(temp_path, dpi=dpi, tesseract_config=tess_config, enhance=enhance)
        elif (ft and ft.startswith("image/")) or file.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            text = extract_text_from_image(temp_path, tesseract_config=tess_config, enhance=enhance)
        else:
            return jsonify({"error": "Unsupported file type. Please upload a PDF or image."}), 400

        if not text or len(text.strip()) < 30:
             return jsonify({"error": "Could not extract readable text."}), 400

        cleaned_text = clean_text(text)
        ents = extract_entities(cleaned_text)
        ext_summary = extractive_summary(cleaned_text, num_sentences=num_sentences)
        abs_summary = abstractive_summary(cleaned_text, max_length=max_len, min_length=min_len)
        legal_acts = suggest_legal_acts(cleaned_text)

        return jsonify({
            "text": cleaned_text,
            "entities": ents,
            "ext_summary": ext_summary,
            "abs_summary": abs_summary,
            "legal_acts": legal_acts
        })
    except Exception as e:
        import traceback
        err_msg = traceback.format_exc()
        return jsonify({"error": err_msg}), 500
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

if __name__ == '__main__':
    app.run(port=5002, debug=True, use_reloader=False)
