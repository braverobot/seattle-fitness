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
# -----------------------------------------------------------------------------------
@app.route("/")
def home():
    return send_from_directory('static', 'index.html')


#
# Routes for Customers page
# -----------------------------------------------------------------------------------
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


#
# Routes for Studios page
# -----------------------------------------------------------------------------------
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
    # redirect back to Customers page after the action is taken
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
        query = "UPDATE Studios SET location = %s, phone_number = %s, \
                 WHERE studio_id = %s;"
        cur = mysql.connection.cursor()
        cur.execute(query, (location, phone_number, studio_id))
        mysql.connection.commit()
        cur.close()
        # redirect back to Studios page
        return redirect("/studios")




# Listener
# Run python app.py to run locally and then browse to http://localhost:8000
# change the port number if deploying on the flip servers


if __name__ == "__main__":
    app.run(port=8000, debug=True)

# NOTE: You can use gunicorn to start the app instead, run the following::
# gunicorn -b 0.0.0.0:8000 app:app
