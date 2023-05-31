# Group 26: Shi Qin & Brian Heartwood
# cs340 OSU Sprint 2023 - Group Project
# Description: This file contains the code for our Flask application.
#
# Citations: A majority of this code was taken from the OSU CS340 Flask
#   tutorial, as well as the notes from the bsg_db and modified

from flask import Flask, render_template, redirect, send_from_directory
from flask_mysqldb import MySQL
from flask import request
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# database connection info
app.config["MYSQL_HOST"] = os.environ.get("cs340DBHOST")
app.config["MYSQL_USER"] = user = os.environ.get("cs340DBUSER")
app.config["MYSQL_PASSWORD"] = passwd = os.environ.get("cs340DBPW")
app.config["MYSQL_DB"] = os.environ.get("cs340DB")
app.config["MYSQL_CURSORCLASS"] = "DictCursor"
mysql = MySQL(app)


#
# Routes for Home Page (index.html that sits in static folder)
# -----------------------------------------------------------------------------
@app.route("/")
def home():
    return send_from_directory('static', 'index.html')


#
# Routes for Customers page
# -----------------------------------------------------------------------------
@app.route("/customers", methods=["POST", "GET"])
def customers():
    """This is to render the customers page to display them from the DB"""

    # Grab customer data so we send it to our template to display
    if request.method == "GET":
        # mySQL query to grab all the customers in the Customers table
        query = "SELECT customer_id, name, phone_number, address \
                 FROM Customers"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()
        cur.close()
        return render_template("customers.j2", data=data)

    # Adding a customer using the POST method
    if request.method == "POST":
        name = request.form["name"]
        phone_number = request.form["phone_number"]
        address = request.form["address"]

        # mySQL query to add a customer to the Customers table
        query = "INSERT INTO Customers (name, phone_number, address) \
                 VALUES (%s, %s, %s);"
        cur = mysql.connection.cursor()
        cur.execute(query, (name, phone_number, address))
        mysql.connection.commit()
        cur.close()
        # redirect back to Customers page
        return redirect("/customers")


@app.route("/delete_customer/<int:customer_id>")
def delete_customer(customer_id):
    # mySQL query to delete the person with our passed id
    query = "DELETE FROM Customers WHERE customer_id = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query, (customer_id,))
    mysql.connection.commit()
    cur.close()
    # redirect back to Customers page after the action is taken
    return redirect("/customers")


@app.route("/update_customer/<int:customer_id>", methods=["POST", "GET"])
def update_customer(customer_id):
    # Grab customer data so we send it to our template to display
    if request.method == "GET":
        # mySQL query to grab all the customers in the Customers table
        query = "SELECT customer_id, name, phone_number, address \
                 FROM Customers WHERE customer_id = %s;"
        cur = mysql.connection.cursor()
        cur.execute(query, (customer_id,))
        data = cur.fetchall()
        cur.close()
        return render_template("update_customer.j2", data=data)

    # Adding a customer using the POST method
    if request.method == "POST":
        name = request.form["name"]
        phone_number = request.form["phone_number"]
        address = request.form["address"]

        # mySQL query to add a customer to the Customers table
        query = "UPDATE Customers SET name = %s, phone_number = %s, \
                 address = %s WHERE customer_id = %s;"
        cur = mysql.connection.cursor()
        cur.execute(query, (name, phone_number, address, customer_id))
        mysql.connection.commit()
        cur.close()
        # redirect back to Customers page
        return redirect("/customers")


#
# Routes for Studios page
# -----------------------------------------------------------------------------
@app.route("/studios", methods=["POST", "GET"])
def studios():
    """This is to render the studios page to display them from the DB"""

    # Grab studio data so we send it to our template to display
    if request.method == "GET":
        # mySQL query to grab all the Studios in the Studios table
        query = "SELECT studio_id, location, phone_number\
                 FROM Studios"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()
        cur.close()
        return render_template("studios.j2", data=data)

    # Adding a studio using the POST method
    if request.method == "POST":
        location = request.form["location"]
        phone_number = request.form["phone_number"]

        # mySQL query to add a studio to the Studios table
        query = "INSERT INTO Studios (location, phone_number) \
                 VALUES (%s, %s);"
        cur = mysql.connection.cursor()
        cur.execute(query, (location, phone_number))
        mysql.connection.commit()
        cur.close()
        # redirect back to Studios page
        return redirect("/studios")


@app.route("/delete_studio/<int:studio_id>")
def delete_studio(studio_id):
    # mySQL query to delete the person with our passed id
    query = "DELETE FROM Studios WHERE studio_id = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query, (studio_id,))
    mysql.connection.commit()
    cur.close()
    # redirect back to Studios page after the action is taken
    return redirect("/studios")


@app.route("/update_studio/<int:studio_id>", methods=["POST", "GET"])
def update_studio(studio_id):
    # Grab studio data so we send it to our template to display
    if request.method == "GET":
        # mySQL query to grab all the studios in the Ctudios table
        query = "SELECT studio_id, location, phone_number \
                 FROM Studios WHERE studio_id = '%s';"
        cur = mysql.connection.cursor()
        cur.execute(query, (studio_id,))
        data = cur.fetchall()
        cur.close()
        return render_template("update_studio.j2", data=data)

    # Adding a studio using the POST method
    if request.method == "POST":
        location = request.form["location"]
        phone_number = request.form["phone_number"]

        # mySQL query to add a studio to the Studios table
        query = "UPDATE Studios SET location = %s, phone_number = %s \
                 WHERE studio_id = %s;"
        cur = mysql.connection.cursor()
        cur.execute(query, (location, phone_number, studio_id))
        mysql.connection.commit()
        cur.close()
        # redirect back to Studios page
        return redirect("/studios")


#
# Routes for Events Page
#
@app.route("/events", methods=["GET"])
def events():
    """This is to render the studios page to display them from the DB"""

    # Grab studio data so we send it to our template to display
    if request.method == "GET":
        return render_template("events.j2")


#
# Routes for Classes page
# -----------------------------------------------------------------------------
@app.route("/classes", methods=["POST", "GET"])
def classes():
    """This is to render the classes page to display them from the DB"""

    # Grab classes data so we send it to our template to display
    if request.method == "GET":
        # mySQL query to grab all the classes in the Classes table
        query1 = "SELECT C.class_id, C.date, C.name, C.size, C.instructor, \
                    CC.experience_level, S.location \
                  FROM Classes C \
                  INNER JOIN Class_Categories CC ON \
                    C.category_id = CC.category_id \
                  INNER JOIN Studios S ON S.studio_id = C.studio_id"
        cur = mysql.connection.cursor()
        cur.execute(query1)
        data = cur.fetchall()
        cur.close()

        # Adding a query for the categories dropdown
        query2 = "SELECT category_id, experience_level FROM Class_Categories"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        cat_data = cur.fetchall()
        cur.close()

        # Adding a query for the studios dropdown
        query3 = "SELECT studio_id, location FROM Studios"
        cur = mysql.connection.cursor()
        cur.execute(query3)
        s_data = cur.fetchall()
        cur.close()

        return render_template("classes.j2",
                               data=data,
                               categories=cat_data,
                               studios=s_data)

    # Adding a class using the POST method
    if request.method == "POST":
        date = request.form["date"]
        name = request.form["name"]
        size = request.form["size"]
        instructor = request.form["instructor"]
        category_id = request.form["categories"]
        studio_id = request.form["studio"]

        # mySQL query to add a Class to the Classes table
        query = "INSERT INTO Classes (date, name, size, instructor, \
                  category_id, studio_id) \
                 VALUES (%s, %s, %s, %s, %s, %s);"
        cur = mysql.connection.cursor()
        cur.execute(query, (date, name, size, instructor,
                            category_id, studio_id))
        mysql.connection.commit()
        cur.close()
        # redirect back to Classes page
        return redirect("/classes")


@app.route("/delete_class/<int:class_id>")
def delete_class(class_id):
    # mySQL query to delete the person with our passed id
    query = "DELETE FROM Classes \
             WHERE class_id = %s;"
    cur = mysql.connection.cursor()
    cur.execute(query, (class_id,))
    mysql.connection.commit()
    cur.close()
    # redirect back to Classes page after the action is taken
    return redirect("/classes")


#
# Routes for Scheduled page
# -----------------------------------------------------------------------------
@app.route("/scheduled", methods=["POST", "GET"])
def scheduled():
    """This is to render the scheduled page to display them from the DB"""

    # Grab scheduled data so we send it to our template to display
    if request.method == "GET":
        # mySQL query to grab all the items in the Customer_Classes table
        query1 = "SELECT Cust.name, Classes.name, Classes.date \
                  FROM Customer_Classes AS CC \
                  INNER JOIN Customers AS Cust \
                   ON CC.customer_id = Cust.customer_id \
                  INNER JOIN Classes \
                   ON CC.class_id = Classes.class_id \
                  ORDER BY Cust.name;"
        cur = mysql.connection.cursor()
        cur.execute(query1)
        data1 = cur.fetchall()
        cur.close()

        # mySQL query to grab all the items in the Customer_Events table
        query2 = "SELECT C.name, E.name, E.date \
                  FROM Customer_Events CE \
                  INNER JOIN Customers AS C \
                    ON CE.customer_id = C.customer_id \
                  INNER JOIN Events AS E \
                    ON CE.event_id = E.event_id \
                  ORDER BY C.name;"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        data2 = cur.fetchall()
        cur.close()

        # Adding a query for the Customer Name dropdown
        dropdown_query_a = "SELECT customer_id, name FROM Customers;"
        cur = mysql.connection.cursor()
        cur.execute(dropdown_query_a)
        data3 = cur.fetchall()
        cur.close()

        # Adding a query for the Class Name dropdown
        dropdown_query_b = "SELECT class_id, name, date FROM Classes;"
        cur = mysql.connection.cursor()
        cur.execute(dropdown_query_b)
        data4 = cur.fetchall()
        cur.close()

        # Adding a query for the Event Name dropdown
        dropdown_query_c = "SELECT event_id, name, date FROM Events;"
        cur = mysql.connection.cursor()
        cur.execute(dropdown_query_c)
        data5 = cur.fetchall()
        cur.close()

        return render_template("scheduled.j2",
                               data1=data1,
                               data2=data2,
                               data3=data3,
                               data4=data4,
                               data5=data5)

    # Addiing a Scheduled Class using the POST method
    # NOTE (brian): I switched to using the .get so I don't have to do try /
    # except statements to check if the value is there. We should probably
    # switch the other routes to use this method as well.
    if request.method == "POST":
        customer_id = request.form.get("customerName")
        event_id = request.form.get("eventName")
        class_id = request.form.get("className")

        # mySQL query to add a Scheduled Class to the Customer_Classes table
        if class_id:
            query3 = "INSERT INTO Customer_Classes (customer_id, class_id) \
                      VALUES (%s, %s);"
            cur = mysql.connection.cursor()
            cur.execute(query3, (customer_id, class_id))
            mysql.connection.commit()
            cur.close()
        if event_id:
            query4 = "INSERT INTO Customer_Events (customer_id, event_id) \
                      VALUES (%s, %s);"
            cur = mysql.connection.cursor()
            cur.execute(query4, (customer_id, event_id))
            mysql.connection.commit()
            cur.close()

        # redirect back to Scheduled page
        return redirect("/scheduled")


# Note how I include 2 parameters in the route decorator here... It took
# me a while to figure out how to do this.
@app.route("/delete_customer_class/<string:customer_name>/<string:class_name>")
def delete_customer_class(customer_name, class_name):
    # mySQL query to delete the person with our passed id
    query4 = "DELETE Customer_Classes \
              FROM Customer_Classes \
              JOIN Customers AS Cust \
                ON Customer_Classes.customer_id = Cust.customer_id \
              JOIN Classes \
                ON Customer_Classes.class_id = Classes.class_id \
              WHERE Cust.name = %s AND Classes.name = %s;"

    cur = mysql.connection.cursor()
    cur.execute(query4, (customer_name, class_name,))
    mysql.connection.commit()
    cur.close()
    # redirect back to Studios page after the action is taken
    return redirect("/scheduled")


@app.route("/delete_customer_event/<string:customer_name>/<string:event_name>")
def delete_customer_event(customer_name, event_name):
    # mySQL query to delete the person with our passed id
    query5 = "DELETE Customer_Events \
              FROM Customer_Events \
              JOIN Customers AS Cust \
                ON Customer_Events.customer_id = Cust.customer_id \
              JOIN Events \
                ON Customer_Events.event_id = Events.event_id \
              WHERE Cust.name = %s AND Events.name = %s;"

    cur = mysql.connection.cursor()
    cur.execute(query5, (customer_name, event_name,))
    mysql.connection.commit()
    cur.close()
    # redirect back to Studios page after the action is taken
    return redirect("/scheduled")


#
# Routes for Categories page
# -----------------------------------------------------------------------------
@app.route("/categories", methods=["POST", "GET"])
def categories():
    """This is to render the categories page to display them from the DB"""
    # Grab categories data so we send it to our template to display
    if request.method == "GET":
        # mySQL query to grab all the items in the Categories table
        query1 = "SELECT * FROM Class_Categories;"
        cur = mysql.connection.cursor()
        cur.execute(query1)
        data = cur.fetchall()
        cur.close()
        return render_template("categories.j2",
                               data=data)

    # Adding a Category using the POST method
    if request.method == "POST":
        experience_level = request.form.get("experience_level")
        query2 = "INSERT INTO Class_Categories (experience_level) \
                  VALUES (%s);"
        cur = mysql.connection.cursor()
        cur.execute(query2, (experience_level,))
        mysql.connection.commit()
        cur.close()

        # redirect back to Categories page
        return redirect("/categories")


@app.route("/delete_category/<int:category_id>")
def delete_category(category_id):
    # mySQL query to delete the person with our passed id
    query3 = "DELETE FROM Class_Categories \
              WHERE category_id = %s;"
    cur = mysql.connection.cursor()
    cur.execute(query3, (category_id,))
    mysql.connection.commit()
    cur.close()
    # redirect back to Categories page after the action is taken
    return redirect("/categories")


@app.route("/update_category/<int:category_id>", methods=["POST", "GET"])
def update_category(category_id):
    """This is to render the update category page to update them in the DB"""
    # Grab categories data so we send it to our template to display
    if request.method == "GET":
        # mySQL query to grab all the items in the Categories table
        query1 = "SELECT * FROM Class_Categories \
                  WHERE category_id = %s;"
        cur = mysql.connection.cursor()
        cur.execute(query1, (category_id,))
        data = cur.fetchall()
        cur.close()
        return render_template("update_category.j2",
                               data=data)

    # Updating a Category using the POST method
    if request.method == "POST":
        experience_level = request.form.get("experience_level")
        query2 = "UPDATE Class_Categories \
                  SET experience_level = %s \
                  WHERE category_id = %s;"
        cur = mysql.connection.cursor()
        cur.execute(query2, (experience_level, category_id,))
        mysql.connection.commit()
        cur.close()

        # redirect back to Categories page
        return redirect("/categories")


# Listener
# Run python app.py to run locally and then browse to http://localhost:8000
# change the port number if deploying on the flip servers
if __name__ == "__main__":
    app.run(port=8000, debug=True)

# NOTE: You can use gunicorn to start the app instead, run the following::
# gunicorn -b 0.0.0.0:8000 app:app
