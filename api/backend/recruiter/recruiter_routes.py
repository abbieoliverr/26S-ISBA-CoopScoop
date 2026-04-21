from flask import Blueprint, request, jsonify, make_response
from backend.db_connection import get_db

recruiters = Blueprint('recruiters', __name__)


@recruiters.route('/listings', methods=['POST'])
def create_listing():
    data = request.get_json()
    required = ['positionTitle', 'description', 'skillsRequired',
                'location', 'salary', 'companyId', 'cycleId']
    missing = [f for f in required if f not in data]
    if missing:
        return make_response(jsonify({'error': f'Missing fields: {missing}'}), 400)

    cursor = get_db().cursor()
    cursor.execute(
        '''
        INSERT INTO Listings
            (positionTitle, description, skillsRequired,
             location, salary, companyId, cycleId)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ''',
        (
            data['positionTitle'],
            data['description'],
            data['skillsRequired'],
            data['location'],
            data['salary'],
            data['companyId'],
            data['cycleId'],
        )
    )
    get_db().commit()
    return make_response(
        jsonify({'message': 'Listing created', 'listingId': cursor.lastrowid}), 201
    )


@recruiters.route('/listings/<int:listing_id>', methods=['PUT'])
def update_listing(listing_id):
    data = request.get_json()
    cursor = get_db().cursor()
    cursor.execute(
        '''
        UPDATE Listings
        SET positionTitle  = %s,
            description    = %s,
            skillsRequired = %s,
            location       = %s,
            salary         = %s
        WHERE listingId = %s
        ''',
        (
            data.get('positionTitle'),
            data.get('description'),
            data.get('skillsRequired'),
            data.get('location'),
            data.get('salary'),
            listing_id,
        )
    )
    get_db().commit()
    return make_response(jsonify({'message': 'Listing updated'}), 200)


@recruiters.route('/listings/<int:listing_id>', methods=['DELETE'])
def delete_listing(listing_id):
    cursor = get_db().cursor()
    cursor.execute('DELETE FROM Applications WHERE listingId = %s', (listing_id,))
    cursor.execute('DELETE FROM Listings WHERE listingId = %s', (listing_id,))
    get_db().commit()
    return make_response(jsonify({'message': 'Listing deleted'}), 200)


@recruiters.route('/listings/<int:listing_id>/applications', methods=['GET'])
def get_listing_applications(listing_id):
    status = request.args.get('status')

    query = '''
        SELECT a.applicationId,
               a.status,
               a.deadline,
               s.firstName,
               s.lastName,
               u.email
        FROM Applications a
        JOIN Students s ON a.studentId = s.studentId
        JOIN Users    u ON s.userId    = u.userId
        WHERE a.listingId = %s
    '''
    params = [listing_id]

    if status:
        query += ' AND a.status = %s'
        params.append(status)

    query += ' ORDER BY a.deadline ASC'

    cursor = get_db().cursor()
    cursor.execute(query, tuple(params))
    return make_response(jsonify(cursor.fetchall()), 200)


@recruiters.route('/applications/<int:application_id>/status', methods=['PUT'])
def update_application_status(application_id):
    data = request.get_json()
    new_status = data.get('status')
    allowed = {'Offered', 'Rejected', 'Interviewing', 'Pending'}

    if new_status not in allowed:
        return make_response(
            jsonify({'error': f'status must be one of {allowed}'}), 400
        )

    cursor = get_db().cursor()
    cursor.execute(
        'UPDATE Applications SET status = %s WHERE applicationId = %s',
        (new_status, application_id)
    )
    get_db().commit()
    return make_response(jsonify({'message': 'Application status updated'}), 200)


@recruiters.route('/interviews', methods=['POST'])
def create_interview():
    data = request.get_json()
    required = ['headInterviewerFullName', 'headInterviewerEmail',
                'dateTime', 'position', 'listingId', 'studentId', 'companyId']
    missing = [f for f in required if f not in data]
    if missing:
        return make_response(jsonify({'error': f'Missing fields: {missing}'}), 400)

    cursor = get_db().cursor()
    cursor.execute(
        '''
        INSERT INTO Interviews
            (headInterviewerFullName, headInterviewerEmail,
             dateTime, position, listingId, studentId, companyId)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ''',
        (
            data['headInterviewerFullName'],
            data['headInterviewerEmail'],
            data['dateTime'],
            data['position'],
            data['listingId'],
            data['studentId'],
            data['companyId'],
        )
    )
    get_db().commit()
    return make_response(
        jsonify({'message': 'Interview scheduled', 'interviewId': cursor.lastrowid}), 201
    )


@recruiters.route('/companies/<int:company_id>/alumni', methods=['GET'])
def get_opted_in_alumni(company_id):
    cursor = get_db().cursor()
    cursor.execute(
        '''
        SELECT s.firstName,
               s.lastName,
               u.email,
               l.positionTitle,
               cc.name AS coopCycle
        FROM   Students    s
        JOIN   Users       u  ON s.userId        = u.userId
        JOIN   Applications a  ON a.studentId    = s.studentId
        JOIN   Offers       o  ON o.applicationId = a.applicationId
        JOIN   Listings     l  ON a.listingId    = l.listingId
        JOIN   COOPCycle   cc  ON l.cycleId      = cc.cycleId
        WHERE  l.companyId        = %s
          AND  s.optedIn          = TRUE
          AND  o.acceptanceStatus = 'Accepted'
        ORDER BY cc.name DESC
        ''',
        (company_id,)
    )
    return make_response(jsonify(cursor.fetchall()), 200)


@recruiters.route('/companies/<int:company_id>/analytics', methods=['GET'])
def get_hiring_analytics(company_id):
    cursor = get_db().cursor()
    cursor.execute(
        '''
        SELECT l.positionTitle,
               COUNT(a.applicationId)                                      AS totalApplicants,
               SUM(CASE WHEN a.status = 'Offered'      THEN 1 ELSE 0 END) AS totalOffers,
               SUM(CASE WHEN a.status = 'Rejected'     THEN 1 ELSE 0 END) AS totalRejected,
               SUM(CASE WHEN a.status = 'Interviewing' THEN 1 ELSE 0 END) AS inInterview,
               ROUND(
                   SUM(CASE WHEN a.status = 'Offered' THEN 1 ELSE 0 END)
                   / NULLIF(COUNT(a.applicationId), 0) * 100, 1
               )                                                           AS acceptanceRatePct,
               ROUND(AVG(DATEDIFF(i.dateTime, a.deadline)), 1)            AS avgDaysToInterview
        FROM   Listings    l
        LEFT JOIN Applications a ON a.listingId = l.listingId
        LEFT JOIN Interviews   i ON i.listingId = l.listingId
                                AND i.studentId = a.studentId
        WHERE  l.companyId = %s
        GROUP  BY l.listingId, l.positionTitle
        ORDER  BY totalApplicants DESC
        ''',
        (company_id,)
    )
    columns = [desc[0] for desc in cursor.description]
    rows = cursor.fetchall()
    result = [dict(zip(columns, row)) for row in rows]
    return make_response(jsonify(result), 200)
