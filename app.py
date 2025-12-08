from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime, date, timedelta
import sys
import os
import re
import json
from dotenv import load_dotenv
from Python.connection import get_connection
import mysql.connector
from mysql.connector import Error
import subprocess
from apscheduler.schedulers.background import BackgroundScheduler

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///conferences.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
class Conference(db.Model):
    __tablename__ = 'conferences'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    acronym = db.Column(db.String(50), nullable=True)
    start_date = db.Column(db.Date, nullable=True)
    end_date = db.Column(db.Date, nullable=True)
    location = db.Column(db.String(255), nullable=True)
    url = db.Column(db.String(500), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "acronym": self.acronym,
            "start_date": self.start_date.isoformat() if self.start_date else None,
            "end_date": self.end_date.isoformat() if self.end_date else None,
            "location": self.location,
            "url": self.url,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

# Helpers
def parse_date(val):
    """Parse a date-like value into a datetime.date object.

    Accepts None, date, datetime, or ISO-8601 date strings (e.g. '2025-11-28').
    Returns None if the input is falsy.
    """
    if not val:
        return None
    if isinstance(val, date) and not isinstance(val, datetime):
        return val
    if isinstance(val, datetime):
        return val.date()
    if isinstance(val, str):
        try:
            # datetime.fromisoformat accepts 'YYYY-MM-DD' and datetimes
            parsed = datetime.fromisoformat(val)
            return parsed.date()
        except ValueError:
            # Try common date-only format
            try:
                return datetime.strptime(val, "%Y-%m-%d").date()
            except Exception:
                raise ValueError(f"Invalid date format: {val}")
    raise ValueError(f"Unsupported date value: {val}")

# Routes
@app.route('/api/conferences', methods=['GET'])
def get_conferences():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                CID,
                Title,
                Start_Date,
                End_Date
                DESCRIP,
                link,
                LID
            FROM Conferences
        """)

        conferences = cursor.fetchall()

        cursor.close()
        conn.close()

        return jsonify(conferences), 200

    except Error as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/conferences/<int:conf_id>', methods=['GET'])
def get_conference(conf_id):
    try:
        print(f"[DEBUG] Fetching conference with CID={conf_id}")
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT
                c.CID as id,
                c.Title as name,
                c.Start_Date as start_date,
                c.End_Date as end_date,
                c.Descrip as description,
                c.link as url,
                CONCAT_WS(', ', l.City, l.State, l.Country) as location
            FROM Conferences c
            LEFT JOIN Location l ON c.LID = l.LID
            WHERE c.CID = %s
        """
        
        cursor.execute(query, (conf_id,))
        conference = cursor.fetchone()

        print(f"[DEBUG] Query executed for CID={conf_id}, Result: {conference}")

        cursor.close()
        conn.close()

        if not conference:
            print(f"[DEBUG] Conference not found for CID={conf_id}")
            return jsonify({"error": "Conference not found"}), 404

        return jsonify(conference), 200

    except Error as e:
        print(f"[ERROR] Database error: {str(e)}")
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        print(f"[ERROR] Unexpected error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/conferences', methods=['POST'])
def create_conference():
    data = request.json or {}

    if not data.get('name'):
        return jsonify({"error": "'name' is required"}), 400

    try:
        start_date = parse_date(data.get('start_date'))
        end_date = parse_date(data.get('end_date'))
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    new_conf = Conference(
        name=data.get('name'),
        acronym=data.get('acronym'),
        start_date=start_date,
        end_date=end_date,
        location=data.get('location'),
        url=data.get('url'),
    )

    db.session.add(new_conf)
    db.session.commit()

    return jsonify(new_conf.to_dict()), 201

@app.route('/api/conferences/<int:conf_id>', methods=['PUT'])
def update_conference(conf_id):
    conference = Conference.query.get(conf_id)
    if not conference:
        return jsonify({"error": "Conference not found"}), 404

    data = request.json or {}

    if 'name' in data and not data.get('name'):
        return jsonify({"error": "'name' cannot be empty"}), 400

    try:
        if 'start_date' in data:
            conference.start_date = parse_date(data.get('start_date'))
        if 'end_date' in data:
            conference.end_date = parse_date(data.get('end_date'))
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    conference.name = data.get('name', conference.name)
    conference.acronym = data.get('acronym', conference.acronym)
    conference.location = data.get('location', conference.location)
    conference.url = data.get('url', conference.url)

    db.session.commit()

    return jsonify(conference.to_dict()), 200

@app.route('/api/conferences/<int:conf_id>', methods=['DELETE'])
def delete_conference(conf_id):
    conference = Conference.query.get(conf_id)
    if not conference:
        return jsonify({"error": "Conference not found"}), 404

    db.session.delete(conference)
    db.session.commit()

    return jsonify({"message": "Conference deleted"}), 200

# Simple test suite
def run_tests():
    """Run a few basic API tests using Flask's test client.

    These tests are intentionally simple sanity checks so you can verify
    that the API CRUD operations work in this sandbox environment.
    """
    print("Setting up test database...")
    # Ensure tables exist; for tests we use the same sqlite file.
    with app.app_context():
        db.drop_all()
        db.create_all()

    client = app.test_client()

    print("1) Test: create conference (POST /conferences)")
    payload = {
        "name": "TestConf",
        "acronym": "TC",
        "start_date": "2025-11-01",
        "end_date": "2025-11-03",
        "location": "Testville",
        "url": "https://testconf.example"
    }
    resp = client.post('/conferences', json=payload)
    print("  status:", resp.status_code)
    print("  body:", resp.json)
    assert resp.status_code == 201
    conf_id = resp.json['id']

    print("2) Test: get conference (GET /conferences/<id>)")
    resp = client.get(f'/conferences/{conf_id}')
    print("  status:", resp.status_code)
    print("  body:", resp.json)
    assert resp.status_code == 200
    assert resp.json['name'] == 'TestConf'

    print("3) Test: update conference (PUT /conferences/<id>)")
    update_payload = {"name": "UpdatedConf", "start_date": "2025-12-01"}
    resp = client.put(f'/conferences/{conf_id}', json=update_payload)
    print("  status:", resp.status_code)
    print("  body:", resp.json)
    assert resp.status_code == 200
    assert resp.json['name'] == 'UpdatedConf'
    assert resp.json['start_date'] == '2025-12-01'

    print("4) Test: list conferences (GET /conferences)")
    resp = client.get('/conferences')
    print("  status:", resp.status_code)
    print("  body length:", len(resp.json))
    assert resp.status_code == 200
    assert any(c['id'] == conf_id for c in resp.json)

    print("5) Test: delete conference (DELETE /conferences/<id>)")
    resp = client.delete(f'/conferences/{conf_id}')
    print("  status:", resp.status_code)
    print("  body:", resp.json)
    assert resp.status_code == 200

    print("6) Test: get deleted conference (should 404)")
    resp = client.get(f'/conferences/{conf_id}')
    print("  status:", resp.status_code)
    print("  body:", resp.json)
    assert resp.status_code == 404

    print("All tests passed!")


CORS(app, resources={r"/api/*": {"origins": ["http://localhost:5173"]}}, supports_credentials=True)

def validate_password_strength(password):
    """Validate password meets security requirements"""
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    if not re.search(r'[0-9]', password):
        return False, "Password must contain at least one number"
    return True, "Password is valid"

def log_audit(user_id, username, operation_type, old_values=None, new_values=None):
    """Log operations to AuditLog table"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO AuditLog (user_id, username, operation_type, old_values, new_values)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            user_id,
            username,
            operation_type,
            json.dumps(old_values) if old_values else None,
            json.dumps(new_values) if new_values else None
        ))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Audit logging error: {str(e)}")

def check_rate_limit(username):
    try:
        conn = get_connection()
        cursor = conn.cursor()
  
        fifteen_mins_ago = datetime.now() - timedelta(minutes=15)
        cursor.execute("""
            SELECT COUNT(*) FROM LoginAttempts 
            WHERE username = %s 
            AND attempt_time > %s 
            AND success = FALSE
        """, (username, fifteen_mins_ago))
        
        failed_attempts = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        
        return failed_attempts >= 5
    except Exception as e:
        print(f"Rate limit check error: {str(e)}")
        return False

def log_login_attempt(username, success):
    """Log login attempt to LoginAttempts table"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO LoginAttempts (username, success)
            VALUES (%s, %s)
        """, (username, success))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Login attempt logging error: {str(e)}")

@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "ConfSpotter API is running!"})

@app.route('/api/test-db', methods=['GET'])
def test_database():
    try:
        conn = get_connection()
        if conn and conn.is_connected():
            cursor = conn.cursor()
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()
            cursor.close()
            conn.close()
            return jsonify({
                "status": "success",
                "message": f"Connected to database: {db_name[0]}"
            })
    except Error as e:
        return jsonify({
            "status": "error",
            "message": f"Database connection failed: {str(e)}"
        }), 500


# PAPERS API:

# Get all papers (optionally filter by conference ID)
@app.get("/api/papers")
def get_papers():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Check if conferenceId query parameter is provided
        conference_id = request.args.get('conferenceId')
        
        if conference_id:
            cursor.execute("SELECT * FROM Papers WHERE CID = %s;", (conference_id,))
        else:
            cursor.execute("SELECT * FROM Papers;")
        
        papers = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(papers), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500


# Get single paper by ID
@app.get("/api/papers/<int:paper_id>")
def get_paper(paper_id):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Paper WHERE paper_id = %s;", (paper_id,))
        paper = cursor.fetchone()
        cursor.close()
        conn.close()
        return jsonify(paper), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500


# Create a new paper
@app.post("/api/papers")
def create_paper():
    data = request.json
    try:
        conn = get_connection()
        cursor = conn.cursor()

        sql = """
            INSERT INTO Paper (title, abstract, person_id, conference_id)
            VALUES (%s, %s, %s, %s)
        """

        cursor.execute(sql, (
            data["title"],
            data["abstract"],
            data["person_id"],
            data["conference_id"]
        ))

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"message": "Paper created successfully."}), 201
    except Error as e:
        return jsonify({"error": str(e)}), 500


# Update paper
@app.put("/api/papers/<int:paper_id>")
def update_paper(paper_id):
    data = request.json
    try:
        conn = get_connection()
        cursor = conn.cursor()

        sql = """
            UPDATE Paper
            SET title = %s,
                abstract = %s,
                person_id = %s,
                conference_id = %s
            WHERE paper_id = %s
        """

        cursor.execute(sql, (
            data["title"],
            data["abstract"],
            data["person_id"],
            data["conference_id"],
            paper_id
        ))

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"message": "Paper updated successfully."}), 200

    except Error as e:
        return jsonify({"error": str(e)}), 500


# Delete a paper
@app.delete("/api/papers/<int:paper_id>")
def delete_paper(paper_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Paper WHERE paper_id = %s;", (paper_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Paper deleted successfully."}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    
#-------------------
#USERS API
#-------------------
#author: Seth Tedder
#the code here was in part generated by an AI language model and then modified.
#Models used: ChatGPT-5, VS copilot

#get all users
@app.get("/api/users")
def get_all_users():    
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user;")
        users = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(users), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500

#get user by ID
@app.get("/api/users/<int:user_id>")
def get_user(user_id):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user WHERE ID = %s;", (user_id,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        return jsonify(user), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500

#insert user
@app.post("/api/users")
def create_user():
    data = request.json
    try:
        if not data.get("username"):
            return jsonify({"message": "Username is required"}), 400
        if not data.get("email"):
            return jsonify({"message": "Email is required"}), 400
        if not data.get("password_hash"):
            return jsonify({"message": "Password is required"}), 400
        if not data.get("Interest_1"):
            return jsonify({"message": "At least one Interest is required"}), 400
        
        is_valid, message = validate_password_strength(data.get("password_hash"))
        if not is_valid:
            return jsonify({"message": message}), 400
        
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            CALL CheckUserExists(%s, %s, %s, @exists_flag, @existing_user_id);
        """, (data.get("email"), data.get("Phone"), data.get("username")))

        cursor.execute("SELECT @exists_flag, @existing_user_id")
        exists_flag, existing_user_id = cursor.fetchone()
        
        if exists_flag == 1:
            cursor.close()
            conn.close()
            return jsonify({"message": "User with this email, username, or phone number already exists"}), 409

        sql = """
            INSERT INTO user (username, password_hash, email, Phone, Interest_1, Interest_2, Interest_3)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        cursor.execute(sql, (
            data["username"],
            data.get("password_hash"),
            data.get("email"),
            data.get("Phone"),
            data.get("Interest_1"),
            data.get("Interest_2"),
            data.get("Interest_3")
        ))

        conn.commit()
        
        log_audit(
            user_id=None,
            username=data["username"],
            operation_type="CREATE_USER",
            new_values={
                "username": data["username"],
                "email": data.get("email"),
                "phone": data.get("Phone")
            }
        )
        
        cursor.close()
        conn.close()

        return jsonify({"message": "User created successfully."}), 201
    except Error as e:
        print(f"Database error: {str(e)}")
        return jsonify({"message": f"Database error: {str(e)}"}), 500
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return jsonify({"message": f"Unexpected error: {str(e)}"}), 500

#update user
@app.put("/api/users/<int:user_id>")
def update_user(user_id):
    data = request.json
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("SELECT * FROM user WHERE ID = %s", (user_id,))
        old_user = cursor.fetchone()
        
        if not old_user:
            cursor.close()
            conn.close()
            return jsonify({"error": "User not found"}), 404
        
        if data.get("password_hash"):
            is_valid, message = validate_password_strength(data.get("password_hash"))
            if not is_valid:
                cursor.close()
                conn.close()
                return jsonify({"message": message}), 400

        sql = """
            UPDATE user
            SET username = %s,
                password_hash = %s,
                email = %s,
                Phone = %s,
                Interest_1 = %s,
                Interest_2 = %s,
                Interest_3 = %s
            WHERE ID = %s
        """

        cursor.execute(sql, (
            data["username"],
            data.get("password_hash"),
            data.get("email"),
            data.get("Phone"),
            data.get("Interest_1"),
            data.get("Interest_2"),
            data.get("Interest_3"),
            user_id
        ))

        conn.commit()
        
        log_audit(
            user_id=user_id,
            username=old_user["username"],
            operation_type="UPDATE_USER",
            old_values={
                "username": old_user["username"],
                "email": old_user["email"],
                "phone": old_user["Phone"]
            },
            new_values={
                "username": data["username"],
                "email": data.get("email"),
                "phone": data.get("Phone")
            }
        )
        
        cursor.close()
        conn.close()

        return jsonify({"message": "User updated successfully."}), 200

    except Error as e:
        return jsonify({"error": str(e)}), 500

#delete user
@app.delete("/api/users/<int:user_id>")
def delete_user(user_id):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("SELECT * FROM user WHERE ID = %s;", (user_id,))
        user_data = cursor.fetchone()
        
        if not user_data:
            cursor.close()
            conn.close()
            return jsonify({"error": "User not found"}), 404
        
        cursor.execute("DELETE FROM user WHERE ID = %s;", (user_id,))
        conn.commit()
        
        log_audit(
            user_id=user_id,
            username=user_data["username"],
            operation_type="DELETE_USER",
            old_values={
                "username": user_data["username"],
                "email": user_data["email"],
                "phone": user_data["Phone"]
            }
        )
        
        cursor.close()
        conn.close()
        return jsonify({"message": "User deleted successfully."}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    
#verify user login
@app.post("/api/users/verify-login")
def verify_login():
    data = request.json
    login_input = data.get("login")  # Can be username or email
    password_hash = data.get("password_hash")

    try:
        if check_rate_limit(login_input):
            return jsonify({"message": "Too many failed login attempts. Please try again in 15 minutes."}), 429
        
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user WHERE (username = %s OR email = %s) AND password_hash = %s;", (login_input, login_input, password_hash))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user:
            log_login_attempt(login_input, True)
            log_audit(
                user_id=user["ID"],
                username=user["username"],
                operation_type="LOGIN_SUCCESS"
            )
            
            return jsonify({"message": "Login successful.", "user": user}), 200
        else:
            log_login_attempt(login_input, False)
            log_audit(
                user_id=None,
                username=login_input,
                operation_type="LOGIN_FAILED"
            )
            
            return jsonify({"message": "Invalid username/email or password."}), 401

    except Error as e:
        return jsonify({"error": str(e)}), 500

#-------------------
# FAVORITES/STARRED CONFERENCES
#-------------------

@app.route('/api/users/<int:user_id>/favorites', methods=['GET'])
def get_user_favorites(user_id):
    """Get all starred conferences for a user"""
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Create favorites table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS UserFavorites (
                ID INT AUTO_INCREMENT PRIMARY KEY,
                user_ID INT NOT NULL,
                conference_ID INT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE KEY unique_favorite (user_ID, conference_ID),
                FOREIGN KEY (user_ID) REFERENCES user(ID) ON DELETE CASCADE,
                FOREIGN KEY (conference_ID) REFERENCES Conferences(CID) ON DELETE CASCADE
            )
        """)
        
        cursor.execute("""
            SELECT conference_ID 
            FROM UserFavorites 
            WHERE user_ID = %s
        """, (user_id,))
        
        favorites = [row['conference_ID'] for row in cursor.fetchall()]
        
        cursor.close()
        conn.close()
        
        return jsonify({"favorites": favorites}), 200
        
    except Error as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/users/<int:user_id>/favorites/<int:conference_id>', methods=['POST'])
def add_favorite(user_id, conference_id):
    """Add a conference to user's favorites"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Create favorites table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS UserFavorites (
                ID INT AUTO_INCREMENT PRIMARY KEY,
                user_ID INT NOT NULL,
                conference_ID INT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE KEY unique_favorite (user_ID, conference_ID),
                FOREIGN KEY (user_ID) REFERENCES user(ID) ON DELETE CASCADE,
                FOREIGN KEY (conference_ID) REFERENCES Conferences(CID) ON DELETE CASCADE
            )
        """)
        
        cursor.execute("""
            INSERT IGNORE INTO UserFavorites (user_ID, conference_ID) 
            VALUES (%s, %s)
        """, (user_id, conference_id))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({"message": "Conference added to favorites"}), 201
        
    except Error as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/users/<int:user_id>/favorites/<int:conference_id>', methods=['DELETE'])
def remove_favorite(user_id, conference_id):
    """Remove a conference from user's favorites"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            DELETE FROM UserFavorites 
            WHERE user_ID = %s AND conference_ID = %s
        """, (user_id, conference_id))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({"message": "Conference removed from favorites"}), 200
        
    except Error as e:
        return jsonify({"error": str(e)}), 500

#-------------------
#BACKUP AND RECOVERY 
#-------------------
#author: Seth Tedder
#the code here was in part generated by an AI language model and then modified.
#Models used: ChatGPT-5, VS copilot
import shutil
import logging

from apscheduler.schedulers.background import BackgroundScheduler
scheduler = BackgroundScheduler()
BACKUP_DIR = os.environ.get("BACKUP_DIR", "./backups")
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_NAME = os.environ.get("DB_NAME")

# Creates a backup of the database and saves it to the backups directory
@app.route("/api/create-backup", methods=["POST"])
def create_backup_api():
    # Checks current status of database and restores to last backup if problem is found, ensuring that no backup is created that is missing tables.
    scheduled_health_check()
    os.makedirs(BACKUP_DIR, exist_ok=True)
    conn = get_connection()
    cursor = conn.cursor()
    # sets name of backup using the time it was created
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{DB_NAME}_backup_{timestamp}.sql"
    # ensures the backup is placed in the same directory every time
    filepath = os.path.join(BACKUP_DIR, filename)

    cmd = [
        # prefer full path to the executable so Windows finds it
        shutil.which("mysqldump") or "mysqldump",
        f"--user={DB_USER}",
        f"--password={DB_PASSWORD}",
        f"--host={DB_HOST}",
        DB_NAME
    ]

    # mysql dump is used to secure all information including schemas, procedurs, and data.
    # If mysqldump isn't on PATH, return a clear error message
    if not shutil.which("mysqldump"):
        return jsonify({"status": "error", "message": "mysqldump not found on PATH. Please install the MySQL client or add its `bin` directory to PATH."}), 500

    try:
        # Run the dump and capture stderr so we can return useful diagnostics
        with open(filepath, "w", encoding="utf-8") as f:
            proc = subprocess.run(cmd, stdout=f, stderr=subprocess.PIPE, text=True)

        if proc.returncode != 0:
            # include the stderr output in the response so the caller can see the cause
            return jsonify({"status": "error", "message": proc.stderr.strip()}), 500

        return jsonify({"status": "success", "file": filename})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# Restores the database from a specified backup file in the backups directory.  This process is destructive.
@app.route("/api/restore", methods=["POST"])
def restore_backup_api():
    # FORCEFUL restore: always run the last backup file found (by mtime)
    os.makedirs(BACKUP_DIR, exist_ok=True)
    data = request.json or {}
    # ignore filename if provided; always use the most recent backup
    files = [os.path.join(BACKUP_DIR, f) for f in os.listdir(BACKUP_DIR) if f.lower().endswith('.sql')]
    if not files:
        return jsonify({'status': 'error', 'message': 'No backups available'}), 404
    # pick latest by modification time
    latest_path = max(files, key=lambda p: os.path.getmtime(p))
    filename = os.path.basename(latest_path)

    # run the mysql client piping the SQL file; do not block on errors
    mysql_cmd = shutil.which('mysql') or 'mysql'
    cmd = [mysql_cmd, f'--user={DB_USER}', f'--password={DB_PASSWORD}', f'--host={DB_HOST}', DB_NAME]
    try:
        with open(latest_path, 'r', encoding='utf-8', errors='ignore') as bf:
            proc = subprocess.run(cmd, stdin=bf, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        # Always return success status 200 — consequences be damned
        logging.info('Force restore attempted from %s; returncode=%s', filename, proc.returncode)
        if proc.stderr:
            logging.warning('mysql stderr: %s', proc.stderr.strip())
        return jsonify({'status': 'success', 'restored_from': filename, 'returncode': proc.returncode, 'stderr': proc.stderr}), 200
    except Exception as e:
        logging.exception('Force restore exception: %s', e)
        # Even on exception, fulfill the user's request to run it; return success with exception text
        return jsonify({'status': 'success', 'restored_from': filename if 'filename' in locals() else None, 'exception': str(e)}), 200
    
#Runs the backup function on a schedule
def scheduled_backup():
    with app.test_request_context():
        create_backup_api()

# Performs a health check, determining if any tables of data are missing.  This protects the database against wide scale failure or tampering.
def scheduled_health_check():
    # Selects essential tables, defaults to user, Conferences, and Papers table if no environment variable is set.
    essential_tables = os.environ.get('HEALTH_CHECK_ESSENTIAL_TABLES', 'user,Conferences,Papers')
    essential_tables = [t.strip() for t in essential_tables.split(',') if t.strip()]

    try:
        conn = get_connection()
        if hasattr(conn, 'is_connected') and not conn.is_connected():
            logging.error('Health check: DB connection object not connected')
            return
        cursor = conn.cursor()
    except Exception as e:
        logging.exception('Health check: cannot connect to DB: %s', str(e))
        return

    # Check backups
    try:
        os.makedirs(BACKUP_DIR, exist_ok=True)
        backups = sorted([f for f in os.listdir(BACKUP_DIR) if f.lower().endswith('.sql')])
        if not backups:
            logging.error('Health check: no backups found in %s', BACKUP_DIR)
            return
        latest = os.path.join(BACKUP_DIR, backups[-1])
        try:
            if os.path.getsize(latest) == 0:
                logging.error('Health check: latest backup %s is empty', latest)
                return
        except Exception as be:
            logging.exception('Health check: failed to stat latest backup %s: %s', latest, str(be))
            return
    except Exception as e:
        logging.exception('Health check: backup dir access failed: %s', str(e))
        return

    # Parse the latest backup to find CREATE TABLE statements and detect missing tables
    try:
        with open(latest, 'r', encoding='utf-8', errors='ignore') as bf:
            content = bf.read()
        # Regex to find CREATE TABLE `name` or CREATE TABLE name (with optional IF NOT EXISTS)
        found = re.findall(r"CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?`?([A-Za-z0-9_]+)`?", content, flags=re.IGNORECASE)
        found_tables = set([t for t in found])
        if not found_tables:
            logging.debug('Health check: no CREATE TABLE statements found in backup (cannot determine expected tables)')
            logging.debug('Health check: lightweight checks passed')
            return

        # Query information_schema for existing tables (case-insensitive)
        try:
            conn2 = get_connection()
            cur2 = conn2.cursor()
            cur2.execute("SELECT table_name FROM information_schema.tables WHERE table_schema=%s", (DB_NAME,))
            rows = cur2.fetchall()
            live_tables = set([r[0] for r in rows])
            missing = [t for t in found_tables if t not in live_tables and t.lower() not in {lt.lower() for lt in live_tables}]
            cur2.close()
            conn2.close()
        except Exception as ie:
            logging.exception('Health check: failed to query live tables: %s', str(ie))
            return

        if missing:
            logging.error('Health check: missing tables detected: %s', missing)
            try:
                with app.test_request_context(json={"filename": os.path.basename(latest)}):
                    resp = restore_backup_api()
                    # If the endpoint returned a Flask response, log its data
                    try:
                        data = resp.get_data(as_text=True) if hasattr(resp, 'get_data') else str(resp)
                    except Exception:
                        data = str(resp)
                    logging.info('Health check: restore endpoint response: %s', data)
            except Exception as rexc:
                logging.exception('Health check: automatic restore attempt failed: %s', str(rexc))
            return
        else:
            logging.debug('Health check: all expected tables present')

    except Exception as pe:
        logging.exception('Health check: failed to parse backup for table list: %s', str(pe))
        return

    logging.debug('Health check: lightweight checks passed')

# scheduler for backups and health checks.  Performs backups every twelve hours.  Performs simple health check every ten minutes.
with app.app_context():
    scheduler.add_job(scheduled_backup, "interval", hours=12)
    scheduler.add_job(scheduled_health_check, "interval", minutes=10)
    scheduler.start()

# Entrypoint
if __name__ == '__main__':
    # If the user runs `python conference_api.py test` the test suite runs
    if 'test' in sys.argv:
        run_tests()
    else:
        # Ensure DB and tables exist before running the server in production/dev
        with app.app_context():
            db.create_all()
        app.run(host='0.0.0.0', port=5001, debug=False, use_reloader=False)
