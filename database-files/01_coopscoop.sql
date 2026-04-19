DROP DATABASE IF EXISTS `Coop-Scoop`;
CREATE DATABASE IF NOT EXISTS `Coop-Scoop`;
USE `Coop-Scoop`;
 
CREATE TABLE Users (
    userId INT AUTO_INCREMENT PRIMARY KEY,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    accountStatus ENUM('Active', 'Suspended') NOT NULL DEFAULT 'Active'
);
 
CREATE TABLE Advisors (
    advisorId INT AUTO_INCREMENT PRIMARY KEY,
    userId INT NOT NULL,
    firstName VARCHAR(100),
    lastName VARCHAR(100),
    college VARCHAR(100),
    CONSTRAINT fk_user_advisors FOREIGN KEY (userId) REFERENCES Users(userId)
);
 
CREATE TABLE Admins (
    adminId INT AUTO_INCREMENT PRIMARY KEY,
    userId INT NOT NULL,
    firstName VARCHAR(100),
    lastName VARCHAR(100),
    CONSTRAINT fk_user_admins FOREIGN KEY (userId) REFERENCES Users(userId)
);
 
CREATE TABLE Companies (
    companyId INT AUTO_INCREMENT PRIMARY KEY,
    companyName VARCHAR(255) NOT NULL,
    location VARCHAR(255),
    website VARCHAR(255),
    searching BOOLEAN DEFAULT TRUE
);
 
CREATE TABLE Recruiters (
    recruiterId INT AUTO_INCREMENT PRIMARY KEY,
    userId INT NOT NULL,
    firstName VARCHAR(100),
    lastName VARCHAR(100),
    companyId INT,
    CONSTRAINT fk_user_recruiters FOREIGN KEY (userId) REFERENCES Users(userId),
    CONSTRAINT fk_recruiter_company FOREIGN KEY (companyId) REFERENCES Companies(companyId)
);
 
CREATE TABLE COOPCycle (
    cycleId INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    current BOOLEAN DEFAULT FALSE
);
 
CREATE TABLE Students (
    studentId INT AUTO_INCREMENT PRIMARY KEY,
    userId INT NOT NULL,
    firstName VARCHAR(100),
    lastName VARCHAR(100),
    phoneNumber VARCHAR(20),
    linkedInLink VARCHAR(255),
    optedIn BOOLEAN DEFAULT TRUE,
    cycleId INT,
    advisorId INT,
    searchStatus ENUM('Searching', 'Accepted Offer', 'Completed') DEFAULT 'Searching',
    CONSTRAINT fk_user_students FOREIGN KEY (userId) REFERENCES Users(userId),
    CONSTRAINT fk_student_cycle FOREIGN KEY (cycleId) REFERENCES COOPCycle(cycleId),
    CONSTRAINT fk_student_advisor FOREIGN KEY (advisorId) REFERENCES Advisors(advisorId)
);
 
CREATE TABLE Notes (
    noteId INT AUTO_INCREMENT PRIMARY KEY,
    studentId INT NOT NULL,
    content TEXT,
    CONSTRAINT fk_student_notes FOREIGN KEY (studentId) REFERENCES Students(studentId)
);
 
CREATE TABLE AdvisorNotes (
    advisorNoteId INT AUTO_INCREMENT PRIMARY KEY,
    advisorId INT NOT NULL,
    studentId INT NOT NULL,
    content TEXT,
    dateTime DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_student_advNotes FOREIGN KEY (studentId) REFERENCES Students(studentId),
    CONSTRAINT fk_advisor_notes FOREIGN KEY (advisorId) REFERENCES Advisors(advisorId)
);
 
CREATE TABLE Reviews (
    reviewId INT AUTO_INCREMENT PRIMARY KEY,
    content TEXT,
    rating INT,
    position VARCHAR(255),
    anonymous BOOLEAN DEFAULT FALSE,
    approval ENUM('Approved', 'Rejected', 'Pending') DEFAULT 'Pending',
    studentId INT NOT NULL,
    companyId INT NOT NULL,
    cycleId INT,
    adminId INT,
    CONSTRAINT validRating CHECK (rating <= 5 AND rating >= 0),
    CONSTRAINT fk_review_student FOREIGN KEY (studentId) REFERENCES Students(studentId),
    CONSTRAINT fk_review_company FOREIGN KEY (companyId) REFERENCES Companies(companyId),
    CONSTRAINT fk_review_cycle FOREIGN KEY (cycleId) REFERENCES COOPCycle(cycleId),
    CONSTRAINT fk_review_admin FOREIGN KEY (adminId) REFERENCES Admins(adminId)
);
 
CREATE TABLE Updates (
    updateId INT AUTO_INCREMENT PRIMARY KEY,
    newContent TEXT,
    approvalStatus ENUM('Approved', 'Rejected', 'Pending') DEFAULT 'Pending',
    timeOfPosting DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    reviewId INT NOT NULL,
    studentId INT NOT NULL,
    CONSTRAINT fk_update_review FOREIGN KEY (reviewId) REFERENCES Reviews(reviewId),
    CONSTRAINT fk_update_student FOREIGN KEY (studentId) REFERENCES Students(studentId)
);
 
CREATE TABLE Listings (
    listingId INT AUTO_INCREMENT PRIMARY KEY,
    positionTitle VARCHAR(255),
    description TEXT,
    skillsRequired TEXT,
    location VARCHAR(255),
    salary INT,
    companyId INT NOT NULL,
    cycleId INT NOT NULL,
    CONSTRAINT fk_listing_company FOREIGN KEY (companyId) REFERENCES Companies(companyId),
    CONSTRAINT fk_listing_cycle FOREIGN KEY (cycleId) REFERENCES COOPCycle(cycleId)
);
 
CREATE TABLE Applications (
    applicationId INT AUTO_INCREMENT PRIMARY KEY,
    status ENUM('Offered', 'Rejected', 'Interviewing', 'Pending') DEFAULT 'Pending',
    deadline DATE,
    listingId INT NOT NULL,
    studentId INT NOT NULL,
    CONSTRAINT fk_application_listing FOREIGN KEY (listingId) REFERENCES Listings(listingId),
    CONSTRAINT fk_application_student FOREIGN KEY (studentId) REFERENCES Students(studentId)
);
 
CREATE TABLE Offers (
    offerId INT AUTO_INCREMENT PRIMARY KEY,
    finalSalary INT,
    acceptanceStatus ENUM('Accepted', 'Rejected', 'Pending'),
    applicationId INT NOT NULL,
    studentId INT NOT NULL,
    CONSTRAINT fk_application_offer FOREIGN KEY (applicationId) REFERENCES Applications(applicationId),
    CONSTRAINT fk_offer_student FOREIGN KEY (studentId) REFERENCES Students(studentId)
);
 
CREATE TABLE Interviews (
    interviewId INT AUTO_INCREMENT PRIMARY KEY,
    headInterviewerFullName VARCHAR(255),
    headInterviewerEmail VARCHAR(255),
    dateTime DATETIME,
    position VARCHAR(255),
    listingId INT NOT NULL,
    studentId INT NOT NULL,
    companyId INT NOT NULL,
    CONSTRAINT fk_interview_student FOREIGN KEY (studentId) REFERENCES Students(studentId),
    CONSTRAINT fk_interview_company FOREIGN KEY (companyId) REFERENCES Companies(companyId),
    CONSTRAINT fk_interview_listing FOREIGN KEY (listingId) REFERENCES Listings(listingId)
);
 
CREATE TABLE InterviewHistory (
    interviewHistoryId INT AUTO_INCREMENT PRIMARY KEY,
    position VARCHAR(255),
    question TEXT,
    companyId INT NOT NULL,
    interviewId INT,
    studentId INT NOT NULL,
    CONSTRAINT fk_history_company FOREIGN KEY (companyId) REFERENCES Companies(companyId),
    CONSTRAINT fk_history_interview FOREIGN KEY (interviewId) REFERENCES Interviews(interviewId),
    CONSTRAINT fk_history_student FOREIGN KEY (studentId) REFERENCES Students(studentId)
);
 
-- ----------------------------------------------------------------
-- Sample Data
-- ----------------------------------------------------------------
 
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
