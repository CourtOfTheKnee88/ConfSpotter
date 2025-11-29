from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
from Python.connection import get_connection
import mysql.connector
from mysql.connector import Error

load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Enable CORS for all routes (allows React frontend to communicate)
CORS(app, origins=["http://localhost:5173"])

# Test route
@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "ConfSpotter API is running!"})

# Test database connection
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

# PAPERS API
# All papers
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


# Single paper by ID
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


# Create new paper
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


# Update existing paper
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


# Delete paper
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


# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({"status": "error", "message": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"status": "error", "message": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)