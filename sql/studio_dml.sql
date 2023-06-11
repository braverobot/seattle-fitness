/* 
Shi Qin & Brian Heartwood
CS340 - Intro to Databases
Oregon State University
Group 26 Project: CRUD Queries
*/


/*
C(R)UD Queries
*/
-- Display the Customers table and include Customer ID, Name, Phone, and Address
SELECT customer_id, name, phone_number, address FROM Customers;

-- Display the Classes table and include Class ID, Date, Name, Size, Instructor, Category id, and Studio id
SELECT class_id, date, name, size, instructor, category_id, studio_id FROM Classes;

-- Display the Events table and include Event ID, Date, Name, Description, and Studio ID
SELECT event_id, date, name, description, studio_id FROM Events;

-- Display the Studios table and include Studio ID, Location, and Phone Number
SELECT studio_id, location, phone_number FROM Studios;

-- Display the Class Categories table and include Category ID and Experience Level
SELECT category_id, experience_level FROM Class_Categories;

-- Display the Customer_Classes table but replace the Customer ID and Class ID with the Customer Name and Class Name
SELECT Cust.name, Classes.name, Classes.date 
FROM Customer_Classes AS CC
INNER JOIN Customers AS Cust ON CC.customer_id = Cust.customer_id
INNER JOIN Classes ON CC.class_id = Classes.class_id
ORDER BY Cust.name;

-- Display the Customer_Events table but replace the Customer ID and Event ID with the Customer Name and Event Name
SELECT C.name, E.name, E.date
FROM Customer_Events CE
INNER JOIN Customers AS C ON CE.customer_id = C.customer_id
INNER JOIN Events AS E ON CE.event_id = E.event_id
ORDER BY C.name;

-- Display Classes and replace category_id and studio_id with experience level and location
SELECT C.class_id, C.date, C.name, C.size, C.instructor, CC.experience_level, S.location FROM Classes C
INNER JOIN Class_Categories CC ON C.category_id = CC.category_id
INNER JOIN Studios S ON S.studio_id = C.studio_id;

-- Display Classes for update class form where you match on class_id
SELECT C.class_id, C.date, C.name, C.size, C.instructor, CC.experience_level, S.location 
FROM Classes C
LEFT JOIN Class_Categories CC ON C.category_id = CC.category_id
LEFT JOIN Studios S ON S.studio_id = C.studio_id
WHERE C.class_id = :class_idInput;




-- Populate Customer Choice Drop Down Menu
SELECT customer_id, name FROM Customers;

-- Populate Class Choice Drop Down Menu
SELECT class_id, name, date FROM Classes;

-- Populate Category Choice Drop Down Menu
SELECT category_id, experience_level FROM Class_Categories;

-- Populate Event Choice Drop Down Menu
SELECT event_id, name, date FROM Events;

-- Populate Studio Choice Drop Down Menu
SELECT studio_id, location FROM Studios;

/*
(C)RUD Queries
*/
-- Create a new customer
INSERT INTO Customers (name, address, phone_number) 
    VALUES (:fnameInput, :addressInput, :phoneInput);

-- Create a new class
INSERT INTO Classes (date, name, size, instructor, category_id, studio_id) 
    VALUES (:dateInput, :nameInput, :sizeInput, :instructorInput, :category_idInput, :studio_idInput);

-- Create a new Category
INSERT INTO Class_Categories (experience_level) \
    VALUES (:experience_level);

-- Create a new event
INSERT INTO Events (date, name, description, studio_id) 
    VALUES (:dateInput, :nameInput, :descriptionInput, :studio_idInput);

-- Create a new studio
INSERT INTO Studios (location, phone_number) 
    VALUES (:locationInput, :phone_numberInput);

-- Create a new customer_class (Schedule a Class)
INSERT INTO Customer_Classes (customer_id, class_id) 
    VALUES (:customer_idInput, :class_idInput);

-- Create a new customer_event (Schedule an Event)
INSERT INTO Customer_Events (customer_id, event_id) 
    VALUES (:customer_idInput, :event_idInput);

/*
CR(U)D Queries
*/
-- Update a customer's information
UPDATE Customers SET name = :nameInput, address = :addressInput, phone_number = :phone_numberInput
WHERE customer_id = :customer_idInput;

-- Update a Studio's information
UPDATE Studios SET location = :locationInput, phone_number = :phone_numberInput 
WHERE studio_id = :studio_idInput;

-- Update a Class's information
UPDATE Classes SET date = :dateInput, name = :nameInput, size = :sizeInput, instructor = :instructorInput,
category_id = :category_idInput, studio_id = :studio_idInput
WHERE class_id = :class_idInput;

-- Update a Class_Categories information
UPDATE Class_Categories SET experience_level = :experienceLevelInput
WHERE category_id = :category_id;

-- Update an Event's information
UPDATE Events SET date = :dateInput, name = :nameInput, description = :descriptionInput, 
studio_id = :studio_idInput
WHERE event_id = :event_idInput;

-- Dislpay the Update a Customer_Class (update a scheduled Class)
SELECT Cust.customer_id, CC.class_id, Cust.name, Classes.name, Classes.date
FROM Customer_Classes AS CC
INNER JOIN Customers AS Cust 
ON CC.customer_id = Cust.customer_id
INNER JOIN Classes
ON CC.class_id = Classes.class_id
WHERE Cust.name = :customer_idInput AND Classes.name = :class_idInput;

-- Update a Customer_Class (update a scheduled Class)
UPDATE Customer_Classes
SET class_id = :class_idInput
WHERE customer_id = :customer_idInput AND class_id = :class_idInput;

-- Display Update a Customer_Event (update a scheduled Event)
SELECT Cust.customer_id, CE.event_id, Cust.name, E.name, E.date
FROM Customer_Events AS CE
INNER JOIN Customers AS Cust
ON CE.customer_id = Cust.customer_id
INNER JOIN Events AS E
ON CE.event_id = E.event_id
WHERE Cust.name = :customer_idInput AND E.name = :event_idInput;

-- Update a Customer_Event (update a scheduled Event)
UPDATE Customer_Events
SET event_id = :event_idInput
WHERE customer_id = :customer_idInput AND event_id = :event_idInput;

/*
CRU(D) Queries
*/
-- Delete a customer
DELETE FROM Customers
WHERE customer_id = :customer_idInput;

-- Delete a class
DELETE FROM Classes
WHERE class_id = :class_idInput;

-- Delete a category
DELETE FROM Class_Categories
WHERE category_id = :category_id;

-- Delete an event
DELETE FROM Events
WHERE event_id = :event_idInput;

-- Delete a studio
DELETE FROM Studios
WHERE studio_id = :studio_idInput;

-- Delete a customer_class (Unschedule a Class)
DELETE Customer_Classes
FROM Customer_Classes
JOIN Customers AS Cust ON Customer_Classes.customer_id = Cust.customer_id
JOIN Classes ON Customer_Classes.class_id = Classes.class_id
WHERE Cust.name = :customer_idInput AND :class_idInput;

-- Delete a customer_event (Unschedule an Event)
DELETE Customer_Events
FROM Customer_Events
JOIN Customers AS Cust ON Customer_Events.customer_id = Cust.customer_id
JOIN Events ON Customer_Events.event_id = Events.event_id
WHERE Cust.name = :customer_idInput AND Events.name = :event_idInput;