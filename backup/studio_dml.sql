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

-- Display the Customer_Classes table but replace the Customer ID and Class ID with the Customer Name and Class Name
SELECT Customers.name, Classes.name, Classes.date FROM Customer_Classes
INNER JOIN Customers ON Customer_Classes.customer_id = Customers.customer_id
INNER JOIN Classes ON Customer_Classes.class_id = Classes.class_id
WHERE Customers.name = :nameInput

-- Display the Customer_Events table but replace the Customer ID and Event ID with the Customer Name and Event Name
SELECT Customers.name, Events.name, Events.date FROM Customer_Events
INNER JOIN Customers ON Customer_Events.customer_id = Customers.customer_id
INNER JOIN Events ON Customer_Events.event_id = Events.event_id
WHERE Customers.name = :nameInput

-- Populate Customer Choice Drop Down Menu
SELECT customer_id FROM Customers;

-- Populate Customer Choice Drop Down Based On Customer Name (May use this one across the board)
SELECT customer_id FROM Customers WHERE name = :nameInput;

-- Populate Class Choice Drop Down Menu
SELECT class_id FROM Classes;

-- Populate Class Choice Drop Down Based On Class Name
SELECT class_id FROM Classes WHERE name = :nameInput;

-- Populate Event Choice Drop Down Menu
SELECT event_id FROM Events;

-- Populate Event Choice Drop Down Based On Event Name 
SELECT event_id FROM Events WHERE name = :nameInput;

-- Populate Studio Choice Drop Down Menu
SELECT studio_id FROM Studios;

-- Populate Studio Choice Drop Down Based On Studio Location
SELECT studio_id FROM Studios WHERE location = :locationInput;

/*
(C)RUD Queries
*/

-- Create a new customer
INSERT INTO Customers (name, address, phone_number) 
    VALUES (:fnameInput, :addressInput, :phoneInput);

-- Create a new class
INSERT INTO Classes (date, name, size, instructor, category_id, studio_id) 
    VALUES (:dateInput, :nameInput, :sizeInput, :instructorInput, :category_idInput, :studio_idInput);

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
UPDATE Customers
    SET name = :nameInput, address = :addressInput, phone_number = :phone_numberInput
    WHERE customer_id = :customer_idInput;

/*
CRU(D) Queries
*/
-- Delete a customer
DELETE FROM Customers
WHERE customer_id = :customer_idInput;

-- Delete a class
DELETE FROM Classes
WHERE class_id = :class_idInput;

-- Delete an event
DELETE FROM Events
WHERE event_id = :event_idInput;

-- Delete a studio
DELETE FROM Studios
WHERE studio_id = :studio_idInput;

-- Delete a customer_class (Unschedule a Class)
DELETE FROM Customer_Classes
WHERE customer_id = :customer_idInput AND class_id = :class_idInput;

-- Delete a customer_event (Unschedule an Event)
DELETE FROM Customer_Events
WHERE customer_id = :customer_idInput AND event_id = :event_idInput;