from flask import Blueprint, jsonify, request, current_app
from backend.db_connection import get_db
from mysql.connector import Error

admins = Blueprint("admins", __name__)


@admins.route("/users", methods=["GET"])
def get_admins_users():
    cursor = get_db().cursor(dictionary=True)
    try:
        query = """
                SELECT u.userId, \
                       u.accountStatus
                FROM Users u
                """
        cursor.execute(query)
        return jsonify(cursor.fetchall()), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


@admins.route("/users/<int:userId>/status", methods=["PUT"])
def update_user_status(userId):
    data = request.get_json()
    new_status = data.get("status")

    if new_status not in ['Active', 'Suspended']:
        return jsonify({"error": "Invalid status"}), 400

    db = get_db()
    cursor = get_db().cursor()
    try:
        query = """
        UPDATE Users SET accountStatus = %s WHERE userId = %s"""
        cursor.execute(query, (new_status, userId))
        db.commit()
        return jsonify({"message": "User status updated"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
