from flask import Blueprint, jsonify, request, current_app
from backend.db_connection import get_db
from mysql.connector import Error

students = Blueprint("students", __name__)

@students.route("/<int:student_id>/applications", methods=["GET"])

def get_student_applications(student_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        query = """
            SELECT a.applicationId, a.status, a.deadline,
                   l.positionTitle, l.salary, l.location,
                   c.companyName
            FROM Applications a
            JOIN Listings l ON a.listingId = l.listingId
            JOIN Companies c ON l.companyId = c.companyId
            WHERE a.studentId = %s
              AND a.deadline IS NOT NULL
            ORDER BY a.deadline ASC
        """
        cursor.execute(query, (student_id,))
        return jsonify(cursor.fetchall()), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()

@students.route("/offers/compare", methods=["GET"])
def compare_offers():
    cursor = get_db().cursor(dictionary=True)
    try:
        offer1 = request.args.get("offer1")
        offer2 = request.args.get("offer2")
 
        if not offer1 or not offer2:
            return jsonify({"error": "Provide offer1 and offer2 as query params"}), 400
 
        query = """
            SELECT o.offerId, o.finalSalary,
                   c.companyName, c.location,
                   AVG(r.rating) AS avgPeerRating
            FROM Offers o
            JOIN Applications a ON o.applicationId = a.applicationId
            JOIN Listings l ON a.listingId = l.listingId
            JOIN Companies c ON l.companyId = c.companyId
            LEFT JOIN Reviews r ON r.companyId = c.companyId
                               AND r.approval = 'Approved'
            JOIN Users u ON r.userId = u.userId
            WHERE o.offerId IN (%s, %s)
                AND u.accountStatus = 'Active'
            GROUP BY o.offerId, o.finalSalary, c.companyName, c.location
        """
        cursor.execute(query, (offer1, offer2))
        return jsonify(cursor.fetchall()), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()

@students.route("/listings", methods=["GET"])
def get_filtered_listings():
    cursor = get_db().cursor(dictionary=True)
    try:
        min_salary = request.args.get("min_salary", 0)
        min_rating = request.args.get("min_rating", 0)
        cycle_id   = request.args.get("cycle_id")
 
        query = """
            SELECT l.listingId, l.positionTitle, l.salary,
                   l.location, l.skillsRequired,
                   c.companyName,
                   AVG(r.rating) AS avgRating
            FROM Listings l
            JOIN Companies c ON l.companyId = c.companyId
            LEFT JOIN Reviews r ON r.companyId = c.companyId
                               AND r.approval = 'Approved'
            JOIN Users u ON r.userId = u.userId
            WHERE l.salary >= %s
                AND u.accountStatus = 'Active'
        """
        params = [min_salary]
 
        if cycle_id:
            query += " AND l.cycleId = %s"
            params.append(cycle_id)
 
        query += """
            GROUP BY l.listingId
            HAVING avgRating >= %s OR avgRating IS NULL
            ORDER BY avgRating DESC
        """
        params.append(min_rating)
 
        cursor.execute(query, params)
        return jsonify(cursor.fetchall()), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()

@students.route("/<int:student_id>/notes", methods=["GET"])
def get_notes(student_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        cursor.execute(
            "SELECT * FROM Notes WHERE studentId = %s", (student_id,)
        )
        return jsonify(cursor.fetchall()), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()

@students.route("/<int:student_id>/notes", methods=["POST"])
def create_note(student_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        data = request.get_json()
        if "content" not in data:
            return jsonify({"error": "Missing required field: content"}), 400
 
        cursor.execute(
            "INSERT INTO Notes (studentId, content) VALUES (%s, %s)",
            (student_id, data["content"])
        )
        get_db().commit()
        return jsonify({"message": "Note created", "noteId": cursor.lastrowid}), 201
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()

@students.route("/<int:student_id>/notes/<int:note_id>", methods=["PUT"])
def update_note(student_id, note_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        data = request.get_json()
        if "content" not in data:
            return jsonify({"error": "Missing required field: content"}), 400
 
        cursor.execute(
            "SELECT noteId FROM Notes WHERE noteId = %s AND studentId = %s",
            (note_id, student_id)
        )
        if not cursor.fetchone():
            return jsonify({"error": "Note not found"}), 404
 
        cursor.execute(
            "UPDATE Notes SET content = %s WHERE noteId = %s AND studentId = %s",
            (data["content"], note_id, student_id)
        )
        get_db().commit()
        return jsonify({"message": "Note updated"}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()

@students.route("/<int:student_id>/notes/<int:note_id>", methods=["DELETE"])
def delete_note(student_id, note_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        cursor.execute(
            "SELECT noteId FROM Notes WHERE noteId = %s AND studentId = %s",
            (note_id, student_id)
        )
        if not cursor.fetchone():
            return jsonify({"error": "Note not found"}), 404
 
        cursor.execute(
            "DELETE FROM Notes WHERE noteId = %s AND studentId = %s",
            (note_id, student_id)
        )
        get_db().commit()
        return jsonify({"message": "Note deleted"}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()

@students.route("/companies/<int:company_id>/reviews", methods=["GET"])
def get_company_reviews(company_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT r.reviewId, r.content, r.rating, r.position,
                   r.anonymous,
                   CASE WHEN r.anonymous = TRUE THEN 'Anonymous'
                        ELSE CONCAT(s.firstName, ' ', s.lastName)
                   END AS reviewerName,
                   cc.name AS coopCycle
            FROM Reviews r
            JOIN Students s ON r.studentId = s.studentId
            JOIN COOPCycle cc ON r.cycleId = cc.cycleId
            JOIN Users u ON r.userId = u.userId
            WHERE r.companyId = %s
              AND r.approval = 'Approved'
              AND u.accountStatus = 'Active'
            ORDER BY r.reviewId DESC
        """, (company_id,))
        return jsonify(cursor.fetchall()), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()

@students.route("/companies/<int:company_id>/interview-history", methods=["GET"])
def get_interview_history(company_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT ih.position, ih.question
            FROM InterviewHistory ih
            WHERE ih.companyId = %s
            ORDER BY ih.position
        """, (company_id,))
        return jsonify(cursor.fetchall()), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()