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



# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({"status": "error", "message": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"status": "error", "message": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)