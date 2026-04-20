from flask import Blueprint, request, jsonify, make_response
from backend.db_connection import get_db

advisor = Blueprint('advisor', __name__)


@advisor.route('/<int:advisor_id>/students', methods=['GET'])
def get_advisor_students(advisor_id):
    cursor = get_db().cursor(dictionary=True)
    cursor.execute(
        '''
        SELECT s.studentId,
               s.firstName,
               s.lastName,
               s.searchStatus,
               s.linkedInLink,
               COUNT(a.applicationId) AS applicationCount
        FROM   Students s
        LEFT JOIN Applications a ON a.studentId = s.studentId
        WHERE  s.advisorId = %s
        GROUP  BY s.studentId, s.firstName, s.lastName, s.searchStatus, s.linkedInLink
        ORDER  BY s.lastName, s.firstName
        ''',
        (advisor_id,)
    )
    return make_response(jsonify(cursor.fetchall()), 200)


@advisor.route('/<int:advisor_id>/notes', methods=['POST'])
def add_advisor_note(advisor_id):
    data = request.get_json()
    required = ['studentId', 'content']
    missing = [f for f in required if f not in data]
    if missing:
        return make_response(jsonify({'error': f'Missing fields: {missing}'}), 400)

    cursor = get_db().cursor(dictionary=True)
    cursor.execute(
        '''
        INSERT INTO AdvisorNotes (advisorId, studentId, content, dateTime)
        VALUES (%s, %s, %s, NOW())
        ''',
        (advisor_id, data['studentId'], data['content'])
    )
    get_db().commit()
    return make_response(
        jsonify({'message': 'Note added', 'advisorNoteId': cursor.lastrowid}), 201
    )


@advisor.route('/<int:advisor_id>/stats', methods=['GET'])
def get_advisor_stats(advisor_id):
    cursor = get_db().cursor(dictionary=True)
    cursor.execute(
        '''
        SELECT c.companyId,
               c.companyName,
               COUNT(DISTINCT a.applicationId)                                         AS totalApplications,
               ROUND(AVG(o.finalSalary), 2)                                            AS avgSalary,
               SUM(CASE WHEN o.acceptanceStatus = 'Accepted' THEN 1 ELSE 0 END)       AS acceptedOffers,
               ROUND(
                   SUM(CASE WHEN o.acceptanceStatus = 'Accepted' THEN 1 ELSE 0 END)
                   / NULLIF(COUNT(o.offerId), 0) * 100, 1
               )                                                                        AS acceptanceRate
        FROM   Students    s
        JOIN   Applications a  ON a.studentId  = s.studentId
        JOIN   Listings     l  ON a.listingId  = l.listingId
        JOIN   Companies    c  ON l.companyId  = c.companyId
        LEFT JOIN Offers    o  ON o.applicationId = a.applicationId
        WHERE  s.advisorId = %s
        GROUP  BY c.companyId, c.companyName
        ORDER  BY totalApplications DESC
        ''',
        (advisor_id,)
    )
    return make_response(jsonify(cursor.fetchall()), 200)


@advisor.route('/<int:advisor_id>/students/<int:student_id>/status', methods=['PUT'])
def update_student_status(advisor_id, student_id):
    data = request.get_json()
    new_status = data.get('searchStatus')
    allowed = {'Searching', 'Accepted Offer', 'Completed'}
    if new_status not in allowed:
        return make_response(
            jsonify({'error': f'searchStatus must be one of {allowed}'}), 400
        )

    cursor = get_db().cursor(dictionary=True)
    cursor.execute(
        'UPDATE Students SET searchStatus = %s WHERE studentId = %s AND advisorId = %s',
        (new_status, student_id, advisor_id)
    )
    get_db().commit()
    return make_response(jsonify({'message': 'Status updated'}), 200)


@advisor.route('/<int:advisor_id>/offers', methods=['GET'])
def get_advisor_offers(advisor_id):
    cursor = get_db().cursor(dictionary=True)
    cursor.execute(
        '''
        SELECT s.studentId,
               s.firstName,
               s.lastName,
               c.companyName,
               l.positionTitle,
               o.offerId,
               o.finalSalary,
               o.acceptanceStatus
        FROM   Students    s
        JOIN   Applications a  ON a.studentId     = s.studentId
        JOIN   Offers       o  ON o.applicationId = a.applicationId
        JOIN   Listings     l  ON a.listingId     = l.listingId
        JOIN   Companies    c  ON l.companyId     = c.companyId
        WHERE  s.advisorId = %s
        ORDER  BY s.lastName, c.companyName
        ''',
        (advisor_id,)
    )
    return make_response(jsonify(cursor.fetchall()), 200)


@advisor.route('/<int:advisor_id>/placements', methods=['GET'])
def get_advisor_placements(advisor_id):
    cursor = get_db().cursor(dictionary=True)
    cursor.execute(
        '''
        SELECT s.firstName,
               s.lastName,
               c.companyName,
               l.positionTitle,
               o.finalSalary,
               cc.name AS cycleName
        FROM   Students    s
        JOIN   Applications a  ON a.studentId     = s.studentId
        JOIN   Offers       o  ON o.applicationId = a.applicationId
        JOIN   Listings     l  ON a.listingId     = l.listingId
        JOIN   Companies    c  ON l.companyId     = c.companyId
        JOIN   COOPCycle   cc  ON l.cycleId       = cc.cycleId
        WHERE  s.advisorId        = %s
          AND  cc.current         = FALSE
          AND  o.acceptanceStatus = 'Accepted'
        ORDER  BY cc.name DESC, s.lastName
        ''',
        (advisor_id,)
    )
    return make_response(jsonify(cursor.fetchall()), 200)


@advisor.route('/<int:advisor_id>/students/<int:student_id>/notes', methods=['GET'])
def get_student_notes(advisor_id, student_id):
    cursor = get_db().cursor(dictionary=True)
    cursor.execute(
        '''
        SELECT advisorNoteId,
               content,
               dateTime
        FROM   AdvisorNotes
        WHERE  advisorId = %s
          AND  studentId = %s
        ORDER  BY dateTime DESC
        ''',
        (advisor_id, student_id)
    )
    return make_response(jsonify(cursor.fetchall()), 200)


@advisor.route('/notes/<int:note_id>', methods=['DELETE'])
def delete_advisor_note(note_id):
    cursor = get_db().cursor(dictionary=True)
    cursor.execute(
        'DELETE FROM AdvisorNotes WHERE advisorNoteId = %s',
        (note_id,)
    )
    get_db().commit()
    return make_response(jsonify({'message': 'Note deleted'}), 200)
