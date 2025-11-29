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
