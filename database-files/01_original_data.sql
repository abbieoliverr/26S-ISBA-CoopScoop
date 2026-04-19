USE `Coop-Scoop`;

SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE InterviewHistory;
TRUNCATE TABLE Interviews;
TRUNCATE TABLE Offers;
TRUNCATE TABLE Applications;
TRUNCATE TABLE Listings;
TRUNCATE TABLE Updates;
TRUNCATE TABLE Reviews;
TRUNCATE TABLE AdvisorNotes;
TRUNCATE TABLE Notes;
TRUNCATE TABLE Students;
TRUNCATE TABLE COOPCycle;
TRUNCATE TABLE Recruiters;
TRUNCATE TABLE Companies;
TRUNCATE TABLE Admins;
TRUNCATE TABLE Advisors;
TRUNCATE TABLE Users;
SET FOREIGN_KEY_CHECKS = 1;

INSERT INTO Users (userId, password, email, accountStatus) VALUES
(1, 'Book-Plane-Mirror81', 'admin1@gmail.com', 'Active'),
(2, 'Balloon-Pencil-Rainbow87', 'admin2@gmail.com', 'Suspended'),
(3, 'Cow-Ship-Pillow', 'advisor1@gmail.com', 'Active'),
(4, 'Fish-Boat-Blanket2', 'advisor2@gmail.com', 'Active'),
(5, 'Cat-Car-Skates71', 'recruiter1@gmail.com', 'Active'),
(6, 'Dog-Train-Table', 'recruiter2@gmail.com', 'Active'),
(7, 'Turtle-Ski-Ceiling', 'student1@gmail.com', 'Active'),
(8, 'Mouse-Snowboard-Door11', 'student2@gmail.com', 'Active');

INSERT INTO Advisors (userId, firstName, lastName, college) VALUES
(3, 'Dingleford', 'McThunderfunk', 'Khoury'),
(4, 'Jane', 'Smith', 'Khoury');

INSERT INTO Admins (userId, firstName, lastName) VALUES
(1, 'Cooper', 'Employ'),
(2, 'Sammy', 'Dean');

INSERT INTO Companies (companyName, location, website, searching) VALUES
('Acme Corp', 'Boston MA', 'acmecorp.com', TRUE),
('MassDOT', 'Boston MA', 'massdot.com', TRUE),
('Fidelity', 'Boston MA', 'fidelity.com', TRUE);

INSERT INTO Recruiters (userId, firstName, lastName, companyId) VALUES
(5, 'Thiago', 'Goat', 1),
(6, 'Tony', 'Calzone', 2);

INSERT INTO COOPCycle (cycleId, name, current) VALUES
(1, 'Spring 2026', TRUE),
(2, 'Fall 2025', FALSE),
(3, 'Spring 2025', FALSE);

INSERT INTO Students (userId, firstName, lastName, phoneNumber, linkedInLink, optedIn, cycleId, advisorId, searchStatus) VALUES
(7, 'Fawn', 'Font', '6178888888', 'linkedin.com/fawnfont', TRUE, 1, 1, 'Searching'),
(8, 'Sara', 'Moshirzadeh', '6177477493', 'linkedin.com/saramoshirzadeh', TRUE, 1, 2, 'Accepted Offer');

INSERT INTO Notes (noteId, studentId, content) VALUES
(1, 1, 'Follow up with Acme Corp recruiter by Friday'),
(2, 1, 'MassDOT deadline is April 3'),
(3, 1, 'Fidelity offer expires April 10');

INSERT INTO AdvisorNotes (advisorId, studentId, content, dateTime) VALUES
(1, 1, 'Told student to apply to 5 more positions', NOW()),
(1, 1, 'Reviewed resume, suggested adding project experience', NOW()),
(2, 2, 'Student is on track, no action needed', NOW());

INSERT INTO Reviews (content, rating, position, studentId, companyId, cycleId, adminId) VALUES
('Great mentorship and real project work!', 4, 'Software Engineer Co-op', 1, 1, 1, 1),
('Very bureaucratic, limited learning opportunities.', 2, 'Data Analyst Co-op', 2, 2, 2, 1),
('Friendly team, good work-life balance.', 5, 'Compliance Co-op', 1, 2, 2, 1);

INSERT INTO Updates (newContent, approvalStatus, timeOfPosting, reviewId, studentId) VALUES
('Great mentorship and real project work!', 'Pending', NOW(), 1, 1),
('Very bureaucratic, limited learning opportunities.', 'Pending', NOW(), 2, 2);

INSERT INTO Listings (positionTitle, description, skillsRequired, location, salary, companyId, cycleId) VALUES
('Software Engineer Co-op', 'Build internal tools', 'Python, SQL', 'Boston, MA', 25, 1, 1),
('Data Analyst Co-op', 'Analyze traffic data', 'Excel, Python', 'Boston, MA', 22, 2, 1),
('Compliance Co-op', 'Support compliance team', 'Excel', 'Boston, MA', 20, 1, 1);

INSERT INTO Applications (status, deadline, listingId, studentId) VALUES
('Pending', '2026-03-30', 1, 1),
('Pending', '2026-03-30', 1, 2),
('Pending', '2026-03-30', 2, 1);

INSERT INTO Offers (finalSalary, acceptanceStatus, applicationId, studentId) VALUES
(25, 'Accepted', 1, 1),
(23, 'Rejected', 3, 1);

INSERT INTO Interviews (headInterviewerFullName, headInterviewerEmail, dateTime, position, listingId, studentId, companyId) VALUES
('Joe Pork', 'joepork@acmecorp.com', '2026-03-12 14:22:05', 'SWE Co-Op', 1, 1, 1),
('Sal Burger', 'salburg@massdot.com', '2026-03-15 15:00:00', 'Data Analyst', 2, 2, 2);

INSERT INTO InterviewHistory (position, question, companyId, interviewId, studentId) VALUES
('SWE Intern', 'Leetcode Race Car', 1, NULL, 1),
('Data Analyst', 'Leetcode #262', 2, 2, 2);
