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

-- Display the Customer_Classes table and include Customer ID and Class ID
SELECT customer_id, class_id FROM Customer_Classes;

-- Display the Customer_Events table and include Customer ID and Event ID
SELECT customer_id, event_id FROM Customer_Events;

-- Populate Customer Choice Drop Down Menu
SELECT customer_id FROM Customers;

-- Populate Customer Choice Drop Down Based On Customer Name (May use this one across the board)
SELECT customer_id FROM Customers WHERE name = :name;

-- Populate Class Choice Drop Down Menu
SELECT class_id FROM Classes;

-- Populate Class Choice Drop Down Based On Class Name
SELECT class_id FROM Classes WHERE name = :name;

-- Populate Event Choice Drop Down Menu
SELECT event_id FROM Events;

-- Populate Event Choice Drop Down Based On Event Name 
SELECT event_id FROM Events WHERE name = :name;

-- Populate Studio Choice Drop Down Menu
SELECT studio_id FROM Studios;

-- Populate Studio Choice Drop Down Based On Studio Location
SELECT studio_id FROM Studios WHERE location = :location;

/*
(C)RUD Queries
*/

-- Create a new customer
INSERT INTO Customers (name, address, phone_number) 
    VALUES (:fname, :address, :phone);

-- Create a new class
INSERT INTO Classes (date, name, size, instructor, category_id, studio_id) 
    VALUES (:date, :name, :size, :instructor, :category_id, :studio_id);

-- Create a new event
INSERT INTO Events (date, name, description, studio_id) 
    VALUES (:date, :name, :description, :studio_id);

-- Create a new studio
INSERT INTO Studios (location, phone_number) 
    VALUES (:location, :phone_number);

-- Create a new customer_class (Schedule a Class)
INSERT INTO Customer_Classes (customer_id, class_id) 
    VALUES (:customer_id, :class_id);

-- Create a new customer_event (Schedule an Event)
INSERT INTO Customer_Events (customer_id, event_id) 
    VALUES (:customer_id, :event_id);

/*
CR(U)D Queries
*/

-- Update a customer's information
UPDATE Customers
    SET name = :name, address = :address, phone_number = :phone_number
    WHERE customer_id = :customer_id;

/*
CRU(D) Queries
*/

-- Delete a customer
DELETE FROM Customers
WHERE customer_id = :customer_id;

-- Delete a class
DELETE FROM Classes
WHERE class_id = :class_id;

-- Delete an event
DELETE FROM Events
WHERE event_id = :event_id;

-- Delete a studio
DELETE FROM Studios
WHERE studio_id = :studio_id;

-- Delete a customer_class (Unschedule a Class)
DELETE FROM Customer_Classes
WHERE customer_id = :customer_id AND class_id = :class_id;

-- Delete a customer_event (Unschedule an Event)
DELETE FROM Customer_Events
WHERE customer_id = :customer_id AND event_id = :event_id;