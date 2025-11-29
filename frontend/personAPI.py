import sys
import os
_sys_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Python'))
if _sys_path not in sys.path:
    sys.path.insert(0, _sys_path)
from connection.py import get_connection

def fetch_all_users():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

def fetch_user_by_id(user_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user WHERE ID = %s", (user_id,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return row

def insert_user(data):
    conn = get_connection()
    cursor = conn.cursor()
    query = """
    INSERT INTO user (username, email, Phone, Interest_1, Interest_2, Interest_3)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, (
        data["username"], data.get("email"), data.get("Phone"),
        data.get("Interest_1"), data.get("Interest_2"), data.get("Interest_3")
    ))
    conn.commit()
    last_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return last_id

def update_user(user_id, data):
    conn = get_connection()
    cursor = conn.cursor()
    query = """
    UPDATE user
    SET username=%s, email=%s, Phone=%s, Interest_1=%s, Interest_2=%s, Interest_3=%s
    WHERE ID=%s
    """
    cursor.execute(query, (
        data["username"], data.get("email"), data.get("Phone"),
        data.get("Interest_1"), data.get("Interest_2"), data.get("Interest_3"),
        user_id
    ))
    conn.commit()
    cursor.close()
    conn.close()

def delete_user(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM user WHERE ID = %s", (user_id,))
    conn.commit()
    cursor.close()
    conn.close()
