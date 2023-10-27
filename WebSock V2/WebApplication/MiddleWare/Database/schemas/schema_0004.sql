CREATE TABLE Teacher(
    first_name VARCHAR(300) NOT NULL,
    last_name VARCHAR(300) NOT NULL,
    phone_number INT NOT NULL,
    PRIMARY KEY (first_name)
);

CREATE TABLE Student(
    first_name VARCHAR(300) NOT NULL,
    last_name VARCHAR(300) NOT NULL,
    phone_number INT NOT NULL,
    teacher_firstname VARCHAR(250) NOT NULL,
    teacher_lastname VARCHAR(250) NOT NULL,
    StudentID INT AUTO_INCREMENT NOT NULL,
    FOREIGN KEY (teacher_firstname) REFERENCES Teacher(first_name) ON DELETE CASCADE,
    FOREIGN KEY (teacher_lastname) REFERENCES Teacher(last_name) ON DELETE CASCADE,
    PRIMARY KEY (StudentID)
);

CREATE TABLE Classroom(
    first_name VARCHAR(300) NOT NULL,
    last_name VARCHAR(300) NOT NULL,
    phone_number INT NOT NULL,
    teacher_firstname VARCHAR(250) NOT NULL,
    teacher_lastname VARCHAR(250) NOT NULL,
    ClassroomID INT AUTO_INCREMENT NOT NULL,
    FOREIGN KEY (teacher_firstname) REFERENCES Teacher(first_name) ON DELETE CASCADE,
    FOREIGN KEY (teacher_lastname) REFERENCES Teacher(last_name) ON DELETE CASCADE,
    PRIMARY KEY (ClassroomID)
);