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


