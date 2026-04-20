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




@admins.route("/reviews", methods=["GET"])
def get_review_data():
    cursor = get_db().cursor(dictionary=True)
    try:
        query = """
        SELECT 
            r.reviewId, r.content, r.rating, r.approval,
            c.companyName, r.anonymous, s.firstName, s.lastName,
            u.userId, u.accountStatus
        FROM Reviews r
        JOIN Companies c ON r.companyId = c.companyId
        JOIN Students s ON r.studentId = s.studentId
        JOIN Users u ON s.userId = u.userId
        """
        cursor.execute(query)
        return jsonify(cursor.fetchall()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


@admins.route("/reviews/sync", methods=["POST"])
def sync_reviews():
    db = get_db()
    cursor = db.cursor()
    try:
        query = """
                UPDATE Reviews r
                    JOIN Students s ON r.studentId = s.studentId
                    JOIN Users u ON s.userId = u.userId
                SET r.approval = 'Rejected'
                WHERE u.accountStatus = 'Suspended'
                """
        cursor.execute(query)
        db.commit()
        return jsonify({"message": f"Data synced."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()




@admins.route("/reviews/log", methods=["GET"])
def get_review_logs():
    start = request.args.get('start')
    end = request.args.get('end')
    db = get_db()
    cursor = db.cursor(dictionary=True)
    try:
        query = """
                    SELECT r.reviewId, r.creationTime, r.content, r.lastUpdated,
                           r.anonymous, c.companyName, s.firstName, s.lastName
                    FROM Reviews r
                             JOIN Companies c ON r.companyId = c.companyId
                             JOIN Students s ON r.studentId = s.studentId
                    WHERE r.creationTime BETWEEN %s AND %s
                    ORDER BY r.creationTime DESC 
                    """
        cursor.execute(query, (start, end))
        logs = cursor.fetchall()
        return jsonify(logs), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()


@admins.route("/coopcycle/<int:cycle_id>/makecurrent", methods=["PUT"])
def set_current_cycle(cycle_id):
    db = get_db()
    cursor = db.cursor()
    try:
        query = "UPDATE COOPCycle SET current = FALSE"
        cursor.execute(query)
        query = "UPDATE COOPCycle SET current = TRUE WHERE cycleId = %s"
        cursor.execute(query, (cycle_id,))
        db.commit()
        return jsonify({"message": "Updated current co-op cycle"}), 200
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()

@admins.route("/coopcycle", methods=["GET"])
def get_cycles():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    try:
        query = "SELECT cycleId, name, current FROM COOPCycle ORDER BY cycleId DESC"
        cursor.execute(query)
        cycles = cursor.fetchall()
        return jsonify(cycles), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()

@admins.route("/coopcycle", methods=["POST"])
def create():
    name = request.json.get('name')
    db = get_db()
    cursor = db.cursor()
    try:
        query = "INSERT INTO COOPCycle (name, current) VALUES (%s, FALSE)"
        cursor.execute(query, (name,))
        db.commit()
        return jsonify({"message": f"Cycle created."}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()