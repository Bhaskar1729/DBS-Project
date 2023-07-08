drop database if exists assignment_manager;
create database assignment_manager;
use assignment_manager;

CREATE TABLE IF NOT EXISTS Student
(
  StudentID INT NOT NULL auto_increment,
  StudentName VARCHAR(50) NOT NULL,
  StudentPassword VARCHAR(50) NOT NULL,
  StudentEmail VARCHAR(50) NOT NULL unique,
  StudentPhone VARCHAR(15) NOT NULL,
  PRIMARY KEY (StudentID)
);

CREATE TABLE IF NOT EXISTS Instructor
(
  InstructorName VARCHAR(50) NOT NULL,
  InstructorID INT NOT NULL auto_increment,
  InstructorPassword VARCHAR(50) NOT NULL,
  InstructorEmail VARCHAR(50) NOT NULL unique,
  InstructorPhone VARCHAR(15) NOT NULL,
  PRIMARY KEY (InstructorID)
);

CREATE TABLE IF NOT EXISTS Course
(
  CourseCode INT NOT NULL auto_increment, 
  CourseName VARCHAR(50) NOT NULL,
  InstructorID INT NOT NULL,
  PRIMARY KEY (CourseCode),
  FOREIGN KEY (InstructorID) REFERENCES Instructor(InstructorID)
);

CREATE TABLE IF NOT EXISTS Assignment
(
  AssignmentID INT NOT NULL auto_increment,
  AssignmentName VARCHAR(50) NOT NULL,
  AssignmentDeadline DATETIME NOT NULL,
  CourseCode INT NOT NULL,
  PRIMARY KEY (AssignmentID),
  FOREIGN KEY (CourseCode) REFERENCES Course(CourseCode)
);

CREATE TABLE IF NOT EXISTS Submission
(
  Grade INT CHECK (Grade >= 0 AND Grade <= 10),
  Feedback VARCHAR(200),
  SubmissionID INT NOT NULL auto_increment,
  SubmissionDate DATETIME NOT NULL,
  SubmissionContent VARCHAR(200) NOT NULL,
  StudentID INT NOT NULL,
  AssignmentID INT NOT NULL,
  PRIMARY KEY (SubmissionID),
  FOREIGN KEY (StudentID) REFERENCES Student(StudentID),
  FOREIGN KEY (AssignmentID) REFERENCES Assignment(AssignmentID)
);

CREATE TABLE IF NOT EXISTS IsAssigned
(
  StudentID INT NOT NULL,
  AssignmentID INT NOT NULL,
  PRIMARY KEY (StudentID, AssignmentID),
  FOREIGN KEY (StudentID) REFERENCES Student(StudentID),
  FOREIGN KEY (AssignmentID) REFERENCES Assignment(AssignmentID)
);

CREATE TABLE IF NOT EXISTS Takes
(
  StudentID INT NOT NULL,
  CourseCode INT NOT NULL,
  PRIMARY KEY (StudentID, CourseCode),
  FOREIGN KEY (StudentID) REFERENCES Student(StudentID),
  FOREIGN KEY (CourseCode) REFERENCES Course(CourseCode)
);

DROP PROCEDURE IF EXISTS register_student;
DELIMITER $$
CREATE PROCEDURE register_student(sname varchar(50), pass varchar(50), email varchar(50), phone varchar(15))
	MODIFIES SQL DATA
BEGIN
	INSERT INTO STUDENT(StudentName, StudentPassword, StudentEmail, StudentPhone) values (sname, pass, email, phone);
END$$
DELIMITER ;

DROP PROCEDURE IF EXISTS register_instructor;
DELIMITER $$
CREATE PROCEDURE register_instructor(iname varchar(50), pass varchar(50), email varchar(50), phone varchar(15))
	MODIFIES SQL DATA
BEGIN
	INSERT INTO INSTRUCTOR(InstructorName, InstructorPassword, InstructorEmail, InstructorPhone) values (iname, pass, email, phone);
END$$
DELIMITER ;

DROP FUNCTION IF EXISTS student_auth;		-- verifies the student id and password for login
DELIMITER $$
CREATE FUNCTION student_auth(id int, pass varchar(50))
    RETURNS INT
    READS SQL DATA
BEGIN
    DECLARE check_value INT;
    SELECT COUNT(*) INTO check_value FROM student WHERE StudentID = id AND StudentPassword = pass;
    RETURN check_value;
END$$
DELIMITER ;

DROP FUNCTION IF EXISTS instructor_auth;	-- verifies the instructor id and password for login
DELIMITER $$
CREATE FUNCTION instructor_auth(id int, pass varchar(50))
    RETURNS INT
    READS SQL DATA
BEGIN
    DECLARE check_value INT;
    SELECT COUNT(*) INTO check_value FROM instructor WHERE InstructorID = id AND InstructorPassword = pass;
    RETURN check_value;
END$$
DELIMITER ;

DROP PROCEDURE IF EXISTS create_assignment;		-- instructor creates an assignment for a course
DELIMITER $$
CREATE PROCEDURE create_assignment(aname varchar(50), deadline datetime, course_code int)
	MODIFIES SQL DATA
BEGIN
	DECLARE assignment_id INT;
	INSERT INTO assignment(AssignmentName, AssignmentDeadline, CourseCode) values (aname, deadline, course_code);	
	SELECT AssignmentID INTO assignment_id from Assignment where (AssignmentDeadline = deadline and assignmentname = aname and coursecode = course_code);
    INSERT INTO IsAssigned(StudentID, AssignmentID) SELECT StudentID, assignment_id as id FROM Student WHERE StudentID IN (SELECT StudentID FROM takes WHERE CourseCode = course_code);
END$$
DELIMITER ;

insert into INSTRUCTOR(InstructorName, InstructorPassword, InstructorEmail, InstructorPhone) values 
("Bhaskar", "bob", "bhaskar@gmail.com", "17291729"),
 ("Nishant", "dog", "nishant@gmail.com", "12345678");

insert into COURSE(CourseName, InstructorID) values 
("Math", 1), 
("ConSys", 2),
("DBS", 2);

insert into STUDENT(StudentName, StudentPassword, StudentEmail, StudentPhone) values 
("Sarthak", "iams", "sarthak@gmail.com", "1209434092"), 
("Kartike", "iamk", "kartike@gmail.com", "1223043040"),
("Rehan", "iamr", "rehan@gmail.com", "0343009990"),
("Shaun", "iams", "shaun@gmail.com", "1202384030");

insert into TAKES(StudentID, CourseCode) values 
(1, 1),
(2, 2),
(3, 2),
(4, 1),
(2, 1);

call create_assignment("first math assignment", CAST('2023-04-18 11:59:59.000' AS DATETIME), 1);
call create_assignment("first consys assignment", CAST('2023-04-18 11:59:59.000' AS DATETIME), 2);

DROP PROCEDURE IF EXISTS filter_assignment_by_student_id;	-- displays the assignments that are assigned to a particular student
DELIMITER $$
CREATE PROCEDURE filter_assignment_by_student_id(id int)
	READS SQL DATA
BEGIN
	SELECT * FROM assignment where AssignmentID in (Select AssignmentID from IsAssigned where StudentID = id) AND AssignmentDeadline > NOW();
END$$
DELIMITER ;

DROP PROCEDURE IF EXISTS filter_assignment_by_deadline;		-- displays the assignments that are whose deadline is not passed
DELIMITER $$
CREATE PROCEDURE filter_assignment_by_deadline(deadline datetime)
	READS SQL DATA
BEGIN
	SELECT * FROM assignment where AssignmentDeadline > deadline;
END$$
DELIMITER ;

DROP PROCEDURE IF EXISTS view_unsubmitted_students; 		-- displays the students who have not submitted a particular assignment
DELIMITER $$
CREATE PROCEDURE view_unsubmitted_students(assignment_id int)
	READS SQL DATA
BEGIN
	SELECT Studentid, StudentName FROM Student WHERE StudentID not in (SELECT StudentID from Submission where AssignmentID = assignment_id) and StudentID in (Select StudentID from IsAssigned where AssignmentID = assignment_id);
END$$
DELIMITER ;

DROP PROCEDURE IF EXISTS view_assignments_with_higher_average_grade;	-- displays assignments for which the average grade is higher than the input
DELIMITER $$
CREATE PROCEDURE view_assignments_with_higher_average_grade(avg_grade float)
	READS SQL DATA
BEGIN
	SELECT AssignmentId, AssignmentName FROM Assignment WHERE average_grade_statistic(AssignmentID) > avg_grade;
END$$
DELIMITER ;

DROP PROCEDURE IF EXISTS reset_student_password;		-- resets the student password by asking email as security question
DELIMITER $$
CREATE PROCEDURE reset_student_password(email varchar(50), new_pass varchar(50))
	MODIFIES SQL DATA
BEGIN
	update Student set StudentPassword = new_pass where StudentEmail = email;
END$$
DELIMITER ;

DROP PROCEDURE IF EXISTS update_student_email;		-- updates student's email
DELIMITER $$
CREATE PROCEDURE update_student_email(student_id int, email varchar(50))
	MODIFIES SQL DATA
BEGIN
	update Student set StudentEmail = email where StudentID = student_id;
END$$
DELIMITER ;

DROP PROCEDURE IF EXISTS update_student_phone;		-- updates student's phone number
DELIMITER $$
CREATE PROCEDURE update_student_phone(student_id int, phone varchar(15))
	MODIFIES SQL DATA
BEGIN
	update Student set StudentPhone = phone where StudentID = student_id;
END$$
DELIMITER ;

DROP PROCEDURE IF EXISTS reset_instructor_password;		-- resets the instructor's password by asking email as security question
DELIMITER $$
CREATE PROCEDURE reset_instructor_password(email varchar(50), new_pass varchar(50))
	MODIFIES SQL DATA
BEGIN
	update Instructor set InstructorPassword = new_pass where InstructorEmail = email;
END$$
DELIMITER ;

DROP PROCEDURE IF EXISTS update_instructor_email;		-- updates the email id of an instructor
DELIMITER $$
CREATE PROCEDURE update_instructor_email(instructor_id int, email varchar(50))
	MODIFIES SQL DATA
BEGIN
	update Instructor set InstructorEmail = email where InstructorID = instructor_id;
END$$
DELIMITER ;

DROP PROCEDURE IF EXISTS update_instructor_phone;		-- updates the phone number of the instructor
DELIMITER $$
CREATE PROCEDURE update_instructor_phone(instructor_id int, phone varchar(15))
	MODIFIES SQL DATA
BEGIN
	update Instructor set InstructorPhone = phone where InstructorID = instructor_id;
END$$
DELIMITER ;

DROP PROCEDURE IF EXISTS submit_assignment;			-- The procedure submits the student's assignment. It takes in the assignment, student_id and the assignment id as inputs. It also deletes any other submission done by the student
DELIMITER $$
CREATE PROCEDURE submit_assignment(content varchar(200), student_id int, assignment_id int)
	MODIFIES SQL DATA
BEGIN
	DELETE FROM Submission WHERE StudentID = student_id AND assignment_id = assignmentID;
	INSERT INTO submission(SubmissionDate, SubmissionContent, StudentID, AssignmentID) values (NOW(), content, student_id, assignment_id);	
END$$
DELIMITER ;

call submit_assignment("Sarthak's Math Submission", 1, 1);
call submit_assignment("Kartike's Math Submission", 2, 1);
call submit_assignment("Kartike's ConSys Submission", 2, 2);
call submit_assignment("Kartike's ReConSys Submission", 2, 2);

DROP PROCEDURE IF EXISTS view_submissions_by_assignment_id;		-- shows all the submissions done for a given assignment
DELIMITER $$
CREATE PROCEDURE view_submissions_by_assignment_id(assignment_id int)
	READS SQL DATA
BEGIN
	SELECT * FROM Submission WHERE AssignmentID = assignment_id;
END$$
DELIMITER ;

DROP PROCEDURE IF EXISTS view_submissions_by_student_id;		-- shows the final submissions done by a student 
DELIMITER $$
CREATE PROCEDURE view_submissions_by_student_id(student_id int)
	READS SQL DATA
BEGIN
	SELECT * FROM Submission WHERE StudentID = student_id;
END$$
DELIMITER ;

DROP PROCEDURE IF EXISTS grade_assignment;			-- the instructor assigns a grade for a submission
DELIMITER $$
CREATE PROCEDURE grade_assignment(submission_id int, grade int)
	MODIFIES SQL DATA
BEGIN
	UPDATE Submission SET Grade = grade WHERE SubmissionID = submission_id;
END$$
DELIMITER ;

call grade_assignment(1, 10);
call grade_assignment(2, 8);

DROP PROCEDURE IF EXISTS give_feedback;			-- the instructor can give feedback for the submission
DELIMITER $$
CREATE PROCEDURE give_feedback(submission_id int, fback varchar(200))
	MODIFIES SQL DATA
BEGIN
	UPDATE Submission SET Feedback = fback WHERE SubmissionID = submission_id;
END$$
DELIMITER ;

call give_feedback(1, "V. Good Sarthak, proud of you!");
call give_feedback(4, "Not bad Kartike, but can do better!");

DROP FUNCTION IF EXISTS completion_statistic; -- Returns the percentage of students who have submitted a particular assignment
DELIMITER $$
CREATE FUNCTION completion_statistic(assignment_id int)
    RETURNS DECIMAL(5, 2)
    READS SQL DATA
BEGIN
    DECLARE total_students_in_course INT;
    DECLARE submissions_for_assignment INT;
    SELECT COUNT(*) INTO total_students_in_course FROM IsAssigned WHERE AssignmentID = assignment_id;
    SELECT COUNT(*) INTO submissions_for_assignment FROM Submission WHERE AssignmentID = assignment_id;
	RETURN submissions_for_assignment / total_students_in_course * 100;
END$$
DELIMITER ;

DROP FUNCTION IF EXISTS average_grade_statistic; -- Returns the average grade for a particular assignment
DELIMITER $$
CREATE FUNCTION average_grade_statistic(assignment_id int)
    RETURNS DECIMAL(4, 2)
    READS SQL DATA
BEGIN
    DECLARE average_grade DECIMAL(4, 2);
    SELECT AVG(Grade) INTO average_grade FROM Submission WHERE AssignmentID = assignment_id;
	RETURN average_grade;
END$$
DELIMITER ;