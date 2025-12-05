from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date
import sys

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///conferences.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Database Model
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
@app.route('/conferences', methods=['GET'])
def get_conferences():
    conferences = Conference.query.all()
    return jsonify([c.to_dict() for c in conferences]), 200

@app.route('/conferences/<int:conf_id>', methods=['GET'])
def get_conference(conf_id):
    conference = Conference.query.get(conf_id)
    if not conference:
        return jsonify({"error": "Conference not found"}), 404
    return jsonify(conference.to_dict()), 200

@app.route('/conferences', methods=['POST'])
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

@app.route('/conferences/<int:conf_id>', methods=['PUT'])
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

@app.route('/conferences/<int:conf_id>', methods=['DELETE'])
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


from flask_cors import CORS
import os
from dotenv import load_dotenv
from Python.connection import get_connection
import mysql.connector
from mysql.connector import Error

load_dotenv()

CORS(app, origins=["http://localhost:5173"])

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

# Get all papers
@app.get("/papers")
def get_papers():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Paper;")
        papers = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(papers), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500


# Get single paper by ID
@app.get("/papers/<int:paper_id>")
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
@app.post("/papers")
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
@app.put("/papers/<int:paper_id>")
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
@app.delete("/papers/<int:paper_id>")
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
@app.get("/users")
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
@app.get("/users/<int:user_id>")
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
        # Validate required fields
        if not data.get("username"):
            return jsonify({"message": "Username is required"}), 400
        if not data.get("email"):
            return jsonify({"message": "Email is required"}), 400
        if not data.get("password_hash"):
            return jsonify({"message": "Password is required"}), 400
        
        conn = get_connection()
        cursor = conn.cursor()

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
@app.put("/users/<int:user_id>")
def update_user(user_id):
    data = request.json
    try:
        conn = get_connection()
        cursor = conn.cursor()

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
        cursor.close()
        conn.close()

        return jsonify({"message": "User updated successfully."}), 200

    except Error as e:
        return jsonify({"error": str(e)}), 500

#delete user
@app.delete("/users/<int:user_id>")
def delete_user(user_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM user WHERE ID = %s;", (user_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "User deleted successfully."}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    
#verify user login
@app.post("/users/verify-login")
def verify_login():
    data = request.json
    username = data.get("username")
    password_hash = data.get("password_hash")

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user WHERE username = %s AND password_hash = %s;", (username, password_hash))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user:
            return jsonify({"message": "Login successful.", "user": user}), 200
        else:
            return jsonify({"message": "Invalid username or password."}), 401

    except Error as e:
        return jsonify({"error": str(e)}), 500
    
#-------------------
#BACKUP AND RECOVERY 
#-------------------
#author: Seth Tedder
#the code here was in part generated by an AI language model and then modified.
#Models used: ChatGPT-5, VS copilot
import subprocess
from apscheduler.schedulers.background import BackgroundScheduler
scheduler = BackgroundScheduler()
BACKUP_DIR = os.environ.get("BACKUP_DIR", "./backups")
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_NAME = os.environ.get("DB_NAME")

@app.route("/api/create-backup", methods=["POST"])

def create_backup_api():
    os.makedirs(BACKUP_DIR, exist_ok=True)
    conn = get_connection()
    cursor = conn.cursor()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{DB_NAME}_backup_{timestamp}.sql"
    filepath = os.path.join(BACKUP_DIR, filename)

    cmd = [
        "mysqldump",
        f"--user={DB_USER}",
        f"--password={DB_PASSWORD}",
        f"--host={DB_HOST}",
        DB_NAME
    ]

    try:
        with open(filepath, "w") as f:
            subprocess.run(cmd, stdout=f)
        return jsonify({"status": "success", "file": filename})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/api/restore", methods=["POST"])
def restore_backup_api():
    os.makedirs(BACKUP_DIR, exist_ok=True)
    data = request.json
    filename = data.get("filename")
    if not filename:
        return jsonify({"status": "error", "message": "No filename provided"}), 400

    filepath = os.path.join(BACKUP_DIR, filename)
    if not os.path.exists(filepath):
        return jsonify({"status": "error", "message": "Backup file not found"}), 404

    cmd = [
        "mysql",
        f"--user={DB_USER}",
        f"--password={DB_PASSWORD}",
        f"--host={DB_HOST}",
        DB_NAME
    ]

    try:
        with open(filepath, "r") as f:
            subprocess.run(cmd, stdin=f)
        return jsonify({"status": "success", "restored_from": filename})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    
def scheduled_backup():
    with app.test_request_context():
        create_backup_api()


def scheduled_health_check():
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            connection_timeout=3
        )
        if conn.is_connected():
            conn.close()
            return
    except:
        pass

    backups = sorted(os.listdir(BACKUP_DIR))
    if backups:
        latest = backups[-1]
        with app.test_request_context(json={"filename": latest}):
            restore_backup_api()

#scheduler for backups and health checks
with app.app_context():
    scheduler.add_job(scheduled_backup, "interval", hours=24)
    scheduler.add_job(scheduled_health_check, "interval", minutes=5)
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
        app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)
