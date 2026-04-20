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
