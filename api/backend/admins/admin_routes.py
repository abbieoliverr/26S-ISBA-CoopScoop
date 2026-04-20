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
        query = """
                UPDATE COOPCycle 
                SET current = FALSE
                """
        cursor.execute(query)
        query = """
                UPDATE COOPCycle 
                SET current = TRUE 
                WHERE cycleId = %s
                """
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
        query = """
                SELECT cycleId, name, current 
                FROM COOPCycle 
                ORDER BY cycleId DESC
                """
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
        query = """
                INSERT INTO COOPCycle (name, current) 
                VALUES (%s, FALSE)
                """
        cursor.execute(query, (name,))
        db.commit()
        return jsonify({"message": f"Cycle created."}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()

@admins.route("/reviews/pending", methods=["GET"])
def get_pending_reviews():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    query = """
        SELECT r.reviewId, c.companyName, s.firstName, s.lastName, 
               r.rating, r.content, r.anonymous
        FROM Reviews r
        JOIN Companies c ON r.companyId = c.companyId
        JOIN Students s ON r.studentId = s.studentId
        WHERE r.approval = 'Pending'
    """
    cursor.execute(query)
    pending = cursor.fetchall()
    cursor.close()
    return jsonify(pending), 200

@admins.route("/reviews/<int:review_id>/status", methods=["PUT"])
def update_review_status():
    status = request.json.get('status')
    reviewId = request.view_args['reviewId']
    db = get_db()
    cursor = db.cursor()
    try:
        query = """
            UPDATE Reviews 
            SET approval = %s 
            WHERE reviewId = %s
        """
        cursor.execute(query, (status, reviewId))
        db.commit()
        return jsonify({"message": "Approval status updated"}), 200
    finally:
        cursor.close()


@admins.route("/data/integritydb", methods=["GET"])
def get_integrity_db():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    results = {}

    # Queries

    # student's status is searching but their co-op cycle isn't the current one
    q1 = """
        SELECT s.studentId, s.firstName, s.lastName, c.name as cycleName
        FROM Students s
        JOIN COOPCycle c ON s.cycleId = c.cycleId
        WHERE s.searchStatus = 'Searching' AND c.current = FALSE
    """

    # a student received an offer but their application status isn't offered
    q2 = """
        SELECT o.offerId, o.studentId, a.status as appStatus
        FROM Offers o
        JOIN Applications a ON o.applicationId = a.applicationId
        WHERE a.status != 'Offered'
    """

    # any of the users' first name or last name are null
    q3 = """
        SELECT 'Advisor' as type, advisorId as id 
        FROM Advisors 
        WHERE firstName IS NULL 
           OR lastName IS NULL
        UNION
        SELECT 'Admin', adminId 
        FROM Admins 
        WHERE firstName IS NULL 
           OR lastName IS NULL
        UNION
        SELECT 'Recruiter', recruiterId 
        FROM Recruiters 
        WHERE firstName IS NULL 
           OR lastName IS NULL
        UNION
        SELECT 'Student', studentId 
        FROM Students 
        WHERE firstName IS NULL 
           OR lastName IS NULL
    """

    # a student is searching for a co-op but has no advisor
    q4 = """
    SELECT studentId, firstName, lastName 
    FROM Students 
    WHERE searchStatus = 'Searching' 
      AND advisorId IS NULL"""


    # the time of last update is earlier than the time of creation
    q5 = """
        SELECT reviewId, creationTime, lastUpdated FROM Reviews 
        WHERE creationTime > NOW() OR lastUpdated < creationTime
    """

    # something has been created but the user is suspended
    q6 = """
    SELECT 'Reviews' as entity, r.reviewId, u.userId
    FROM Reviews r JOIN Students s ON r.studentId = s.studentId 
    JOIN Users u ON s.userId = u.userId WHERE u.accountStatus = 'Suspended'
    
    UNION

    SELECT 'Applications', a.applicationId, u.userId
    FROM Applications a JOIN Students s ON a.studentId = s.studentId 
    JOIN Users u ON s.userId = u.userId WHERE u.accountStatus = 'Suspended'
    
    UNION 

    SELECT 'Offers', o.offerId, u.userId
    FROM Offers o JOIN Students s ON o.studentId = s.studentId 
    JOIN Users u ON s.userId = u.userId WHERE u.accountStatus = 'Suspended'

    UNION 

    SELECT 'Interviews', i.interviewId, u.userId 
    FROM Interviews i JOIN Students s ON i.studentId = s.studentId 
    JOIN Users u ON s.userId = u.userId WHERE u.accountStatus = 'Suspended'

    UNION

    SELECT 'Student Notes', n.noteId, u.userId
    FROM Notes n JOIN Students s ON n.studentId = s.studentId 
    JOIN Users u ON s.userId = u.userId WHERE u.accountStatus = 'Suspended'

    UNION
        
    SELECT 'Advisor Notes', an.advisorNoteId, u.userId
    FROM AdvisorNotes an JOIN Advisors adv ON an.advisorId = adv.advisorId 
    JOIN Users u ON adv.userId = u.userId WHERE u.accountStatus = 'Suspended'

    UNION
        
    SELECT 'Interview History', ih.interviewHistoryId, u.userId
    FROM InterviewHistory ih JOIN Students s ON ih.studentId = s.studentId 
    JOIN Users u ON s.userId = u.userId WHERE u.accountStatus = 'Suspended'
"""

    cursor.execute(q1)
    results['invalid_search'] = cursor.fetchall()

    cursor.execute(q2)
    results['invalid_offer'] = cursor.fetchall()

    cursor.execute(q3)
    results['null_name'] = cursor.fetchall()

    cursor.execute(q4)
    results['unassigned_advisor'] = cursor.fetchall()

    cursor.execute(q5)
    results['time_mismatch'] = cursor.fetchall()

    cursor.execute(q6)
    results['suspended_activity'] = cursor.fetchall()

    cursor.close()
    return jsonify(results), 200