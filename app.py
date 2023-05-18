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

app = Flask(__name__)

# database connection info
app.config["MYSQL_HOST"] = os.environ.get("cs340DBHOST")
app.config["MYSQL_USER"] = user = os.environ.get("cs340DBUSER")
app.config["MYSQL_PASSWORD"] = passwd = os.environ.get("cs340DBPW")
app.config["MYSQL_DB"] = os.environ.get("cs340DB")
app.config["MYSQL_CURSORCLASS"] = "DictCursor"
mysql = MySQL(app)


# Routes
# have homepage route to /seattle-fitness by default for convenience
@app.route("/")
def home():
    return send_from_directory('static', 'index.html')


# route for Customers page
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


# This is the route for delete customers functionality. We want to pass the
# 'customer_id' value of that person on button click (see HTML) via the route
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

# This is the route to update a customer's information. We want to pass the
# 'customer_id' value of that person on button click (see HTML) via the route
@app.route("/update_customer/<int:customer_id>", methods=["POST", "GET"])
def update_customer(customer_id):
    # Grab customer data so we send it to our template to display
    if request.method == "GET":
        # mySQL query to grab all the customers in the Customers table
        query = "SELECT customer_id, name, phone_number, address \
                 FROM Customers WHERE customer_id = '%s';"
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


@app.route("/studios", methods=["GET"])
def studios():
    if request.method == "GET":
        return render_template("studios.j2")
    # TODO (Brian): Add POST method for adding a studio and format the
    # .j2 template better

# Listener
# Run python app.py to run locally and then browse to http://localhost:8000
# change the port number if deploying on the flip servers


if __name__ == "__main__":
    app.run(port=8000, debug=True)

# NOTE: You can use gunicorn to start the app instead, run the following::
# gunicorn -b 0.0.0.0:8000 app:app
