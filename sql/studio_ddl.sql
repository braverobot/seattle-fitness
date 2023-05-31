-- Disable foreign key checks, that way we can blast away tables without having to worry about the foreign key constraints etc.
SET FOREIGN_KEY_CHECKS = 0;
SET AUTOCOMMIT = 0;
-- Drop all tables
DROP TABLE IF EXISTS Classes;
DROP TABLE IF EXISTS Events;
DROP TABLE IF EXISTS Customers;
DROP TABLE IF EXISTS Studios;
DROP TABLE IF EXISTS Class_Categories;
DROP TABLE IF EXISTS Customer_Events;
DROP TABLE IF EXISTS Customer_Classes;

CREATE TABLE Studios (
    studio_id INT NOT NULL AUTO_INCREMENT,  
    location VARCHAR(128) NOT NULL,
    phone_number VARCHAR(11) NOT NULL,  
    PRIMARY KEY (studio_id)
);
-- Creating Customers table
CREATE TABLE Customers (
    customer_id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(128) NOT NULL,
    address VARCHAR(128),
    phone_number VARCHAR(11),  
    PRIMARY KEY (customer_id)
);

-- Creating Class_Categories table
CREATE TABLE Class_Categories (
    category_id TINYINT NOT NULL AUTO_INCREMENT, 
    experience_level VARCHAR(20) NOT NULL,
    PRIMARY KEY (category_id)
);

-- Creating Classes table
CREATE TABLE Classes (
    class_id INT NOT NULL AUTO_INCREMENT,
    date DATETIME NOT NULL,
    name VARCHAR(128) NOT NULL,
    size TINYINT NOT NULL,
    instructor VARCHAR(128) NOT NULL,
    category_id TINYINT,
    studio_id INT,
    PRIMARY KEY (class_id),
    FOREIGN KEY (category_id) REFERENCES Class_Categories(category_id) ON UPDATE CASCADE ON DELETE SET NULL,
    FOREIGN KEY (studio_id) REFERENCES Studios(studio_id) ON UPDATE CASCADE ON DELETE SET NULL
);

-- Creating Events table
CREATE TABLE Events (
    event_id INT NOT NULL AUTO_INCREMENT, 
    date DATETIME NOT NULL,
    name VARCHAR(128) NOT NULL,
    description VARCHAR(128),
    studio_id INT,
    PRIMARY KEY (event_id),
    FOREIGN KEY (studio_id) REFERENCES Studios(studio_id) ON UPDATE CASCADE ON DELETE SET NULL
);

-- Creating Customer_Classes table
CREATE TABLE Customer_Classes (
    customer_id INT,                     
    class_id INT,                          
    PRIMARY KEY (customer_id, class_id),
    FOREIGN KEY (customer_id) REFERENCES Customers(customer_id) ON DELETE CASCADE,
    FOREIGN KEY (class_id) REFERENCES Classes(class_id) ON DELETE CASCADE
);

-- Creating Customer_Events table
CREATE TABLE Customer_Events (
    customer_id INT,
    event_id INT,
    PRIMARY KEY (customer_id, event_id),
    FOREIGN KEY (customer_id) REFERENCES Customers(customer_id) ON DELETE CASCADE,
    FOREIGN KEY (event_id) REFERENCES Events(event_id) ON DELETE CASCADE
);

-- Inserting test data for all of the tables
INSERT INTO Studios (location, phone_number)
VALUES ('7001 Main St, Seattle, WA 98116', '5555551234'),
       ('333 Dexter Ave, Seattle, WA 98105', '5555551111'),
       ('15 1st Ln, Seattle, WA 98102', '5555551112'),
       ('1337 Union St, Seattle, WA 98265', '5555555555'),
       ('654 15th St, Seattle, WA 98122', '5555554321');

INSERT INTO Customers (name, address, phone_number) 
VALUES ('Mickey Mouse', '4550 38th Ave SW, Seattle, WA 98126','4022121212'),
       ('Donald Duck', '800 Elmer St, Seattle, WA 98105', '4022121225'),
       ('Goofy', '1 Oak St, Seattle, WA 98151', '4022121255'),
       ('Daisy Duck', '800 Elmer St, Seattle, WA 98102', '4022121225'),
       ('Chuck Norris', '420 Round House Ln, Seattle, WA 98106', '4025555555');

INSERT INTO Class_Categories (experience_level)
VALUES ('Beginner'),
       ('Intermediate'),
       ('Advanced'),
       ('Open'),
       ('Tutorial');

INSERT INTO Classes (date, name, size, instructor, category_id, studio_id) 
VALUES ('2023-03-11 18:00:00','Yoga For Noobs', 10, 'Kirk', 1, 1),    
       ('2023-06-21 18:30:00','Pilates For Wellness', 12, 'Picard', 2, 2),
       ('2023-06-01 18:00:00','Spin Class', 8, 'Bones', 3, 3),
       ('2023-06-06 16:00:00','Spin Class Advanced', 15, 'Uhura', 4, 4),
       ('2023-06-08 18:00:00','Cardio Kickboxing', 10, 'Data', 5, 5);

INSERT INTO Events (date, name, description, studio_id)
VALUES ('2023-06-01 18:00:00', 'Some Awesome Guru Yoga Workshop', 'A sound bath yoga workshop for beginners', 1),
       ('2023-06-01 19:00:00', 'Pilates Bougie Excursion', 'A weekend Pilates session', 2),
       ('2023-06-02 13:00:00', 'Spin Marathon', 'A 10-hour spin marathon for advanced riders', 3),
       ('2023-06-01 18:00:00', 'Zumba Party', 'A fun Zumba dance party', 4),
       ('2023-06-03 15:00:00', 'Kickboxing Open Competition', 'The Annual kickboxing competition', 5);

-- Show Donald and Daisy taking a few classes at our cool studios. They prolly go to the same classes
INSERT INTO Customer_Classes (customer_id, class_id)  
VALUES (2,2),
       (2,3),
       (4,2),
       (4,3);  

-- Show Mickey and Goofy attending some fabulous events .They don't attend the same events
INSERT INTO Customer_Events (customer_id, event_id)
VALUES (1,1), 
       (1,3),   
       (3,2),
       (3,4);


-- Re-enable foreign key checks
SET FOREIGN_KEY_CHECKS = 1;
COMMIT;

-- Below is used for our benefit and not to create or load data
DESCRIBE Studios;
SELECT * FROM Studios;

DESCRIBE Customers;
SELECT * FROM Customers;

DESCRIBE Class_Categories;
SELECT * FROM Class_Categories;

DESCRIBE Classes;
SELECT * FROM Classes;

DESCRIBE Events;
SELECT * FROM Events;

DESCRIBE Customer_Classes;
SELECT * FROM Customer_Classes;

DESCRIBE Customer_Events;
SELECT * FROM Customer_Events;

