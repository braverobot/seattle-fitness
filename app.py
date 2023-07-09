# ### Citation Scope: Flask routers and the mysql database connectivity
  ### Date: 6/1/2023
  ### Originality: Adapted and / or based upon concepts
  ### Sources: See the README in the root directory for more info 

from flask import Flask, render_template, redirect
from flask_mysqldb import MySQL
from flask import request
from flask import flash
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# database connection info
app.config["MYSQL_HOST"] = os.environ.get("cs340DBHOST")
app.config["MYSQL_USER"] = user = os.environ.get("cs340DBUSER")
app.config["MYSQL_PASSWORD"] = passwd = os.environ.get("cs340DBPW")
app.config["MYSQL_DB"] = os.environ.get("cs340DB")
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

# Flash needs this because it uses sessions and sessions require a secret key
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
mysql = MySQL(app)


# ----------------------------------------------------------------------------
# Routes for Home Page (index.html that sits in static folder)
# ----------------------------------------------------------------------------
@app.route("/")
def home():
    """This is to render the home page"""

    return render_template("index.j2")


# ----------------------------------------------------------------------------
# Routes for Customers page
# -----------------------------------------------------------------------------
@app.route("/customers", methods=["POST", "GET"])
def customers():
    """This is to render the customers page to display them from the DB
    as well as add new customers
    """

    # Grab customer data so we send it to our template to display
    if request.method == "GET":
        # mySQL query to grab all the customers in the Customers table
        query = "SELECT customer_id, name, phone_number, address \
                 FROM Customers;"
        try:
            cur = mysql.connection.cursor()
            cur.execute(query)
            data = cur.fetchall()
            cur.close()

        except Exception as e:
            flash(f"Error: {e}", "failure")
            return redirect("/")

        # Render the customers page
        return render_template("customers.j2", data=data)

    # Adding a customer using the POST method
    if request.method == "POST":
        name = request.form["name"]
        phone_number = request.form["phone_number"]
        address = request.form["address"]

        # mySQL query to add a customer to the Customers table
        query = "INSERT INTO Customers (name, phone_number, address) \
                 VALUES (%s, %s, %s);"
        try:
            cur = mysql.connection.cursor()
            cur.execute(query, (name, phone_number, address))
            mysql.connection.commit()
            cur.close()

        except Exception as e:
            flash(f"Error: {e}", "failure")
            return redirect("/customers")

        flash("Customer added successfully", "success")
        return redirect("/customers")


@app.route("/delete_customer/<int:customer_id>")
def delete_customer(customer_id):
    """This is to delete a customer from the DB"""

    query = "DELETE FROM Customers WHERE customer_id = '%s';"
    try:
        cur = mysql.connection.cursor()
        cur.execute(query, (customer_id,))
        mysql.connection.commit()
        cur.close()

    except Exception as e:
        flash(f"Error: {e}", "failure")
        return redirect("/customers")

    flash("Customer deleted successfully", "success")
    return redirect("/customers")


@app.route("/update_customer/<int:customer_id>", methods=["POST", "GET"])
def update_customer(customer_id):
    """This is to update a customer in the DB"""

    # Grab customer data so we send it to our template to display
    if request.method == "GET":
        # mySQL query to grab all the customers in the Customers table
        query = "SELECT customer_id, name, phone_number, address \
                 FROM Customers WHERE customer_id = %s;"
        try:
            cur = mysql.connection.cursor()
            cur.execute(query, (customer_id,))
            data = cur.fetchall()
            cur.close()

        except Exception as e:
            flash(f"Error: {e}", "failure")
            return redirect("/customers")

        # Render the customers page with the updated customer
        return render_template("update_customer.j2", data=data)

    # Adding a customer using the POST method
    if request.method == "POST":
        name = request.form["name"]
        phone_number = request.form["phone_number"]
        address = request.form["address"]

        # mySQL query to add a customer to the Customers table
        query = "UPDATE Customers SET name = %s, phone_number = %s, \
                 address = %s WHERE customer_id = %s;"
        try:
            cur = mysql.connection.cursor()
            cur.execute(query, (name, phone_number, address, customer_id))
            mysql.connection.commit()
            cur.close()

        except Exception as e:
            flash(f"Error: {e}", "failure")
            return redirect("/customers")

        return redirect("/customers")


# ----------------------------------------------------------------------------
# Routes for Studios page
# ----------------------------------------------------------------------------
@app.route("/studios", methods=["POST", "GET"])
def studios():
    """This is to render the studios page to display them from the DB
    as well as add new studios
    """

    # Grab studio data so we send it to our template to display
    if request.method == "GET":
        # mySQL query to grab all the Studios in the Studios table
        query = "SELECT studio_id, location, phone_number\
                 FROM Studios;"
        try:
            cur = mysql.connection.cursor()
            cur.execute(query)
            data = cur.fetchall()
            cur.close()

        except Exception as e:
            flash(f"Error: {e}", "failure")
            return redirect("/")

        # Render the studios page
        return render_template("studios.j2", data=data)

    # Adding a studio using the POST method
    if request.method == "POST":
        location = request.form["location"]
        phone_number = request.form["phone_number"]

        # mySQL query to add a studio to the Studios table
        query = "INSERT INTO Studios (location, phone_number) \
                 VALUES (%s, %s);"
        try:
            cur = mysql.connection.cursor()
            cur.execute(query, (location, phone_number))
            mysql.connection.commit()
            cur.close()

        except Exception as e:
            flash(f"Error: {e}", "failure")
            return redirect("/studios")

        flash("Studio added successfully", "success")
        # redirect back to Studios page
        return redirect("/studios")


@app.route("/delete_studio/<int:studio_id>")
def delete_studio(studio_id):
    """This is to delete a studio from the DB"""

    query = "DELETE FROM Studios WHERE studio_id = '%s';"
    try:
        cur = mysql.connection.cursor()
        cur.execute(query, (studio_id,))
        mysql.connection.commit()
        cur.close()

    except Exception as e:
        flash(f"Error: {e}", "failure")
        return redirect("/studios")

    flash("Studio deleted successfully", "success")
    # redirect back to Studios page after deleting the studio
    return redirect("/studios")


@app.route("/update_studio/<int:studio_id>", methods=["POST", "GET"])
def update_studio(studio_id):
    """This is to update a studio in the DB"""

    if request.method == "GET":
        # mySQL query to grab all the studios in the Ctudios table
        query = "SELECT studio_id, location, phone_number \
                 FROM Studios WHERE studio_id = '%s';"
        try:
            cur = mysql.connection.cursor()
            cur.execute(query, (studio_id,))
            data = cur.fetchall()
            cur.close()

        except Exception as e:
            flash(f"Error: {e}", "failure")
            return redirect("/studios")

        flash("Studio updated successfully", "success")
        return render_template("update_studio.j2", data=data)

    # Adding a studio using the POST method
    if request.method == "POST":
        location = request.form["location"]
        phone_number = request.form["phone_number"]

        # mySQL query to add a studio to the Studios table
        query = "UPDATE Studios SET location = %s, phone_number = %s \
                 WHERE studio_id = %s;"
        try:
            cur = mysql.connection.cursor()
            cur.execute(query, (location, phone_number, studio_id))
            mysql.connection.commit()
            cur.close()

        except Exception as e:
            flash(f"Error: {e}", "failure")
            return redirect("/studios")

        # redirect back to Studios page
        return redirect("/studios")


# ----------------------------------------------------------------------------
# Routes for Events Page
# ----------------------------------------------------------------------------
@app.route("/events", methods=["POST", "GET"])
def events():
    """ This is to render the events page to display them from the DB
        as well as add new events
    """

    if request.method == "GET":
        # mySQL query to grab all the events in the Events table
        query1 = "SELECT E.event_id, E.date, E.name, \
                    E.description, S.location \
                  FROM Events E \
                  LEFT JOIN Studios S ON S.studio_id = E.studio_id;"
        try:
            cur = mysql.connection.cursor()
            cur.execute(query1)
            data = cur.fetchall()
            cur.close()

        except Exception as e:
            flash(f"Error: {e}", "failure")
            return redirect("/")

        # Adding a query for the studios dropdown
        query3 = "SELECT studio_id, location FROM Studios;"
        cur = mysql.connection.cursor()
        cur.execute(query3)
        s_data = cur.fetchall()
        cur.close()

        return render_template("events.j2",
                               data=data,
                               studios=s_data)

    # Adding a event using the POST method
    if request.method == "POST":
        date = request.form["date"]
        name = request.form["name"]
        description = request.form["description"]
        studio_id = request.form["studios"]

        # mySQL query to add a event to the Events table
        query = "INSERT INTO Events (date, name, description, studio_id) \
                 VALUES (%s, %s, %s, %s);"
        try:
            cur = mysql.connection.cursor()
            cur.execute(query, (date, name, description, studio_id))
            mysql.connection.commit()
        except Exception as e:
            flash(f"Error: {e}", "failure")
            return redirect("/events")
        cur.close()

        flash("Event added successfully", "success")
        # redirect back to Events page
        return redirect("/events")


@app.route("/delete_event/<int:event_id>")
def delete_event(event_id):
    """ This is to delete an event from the DB"""

    query = "DELETE FROM Events WHERE event_id = %s;"
    try:
        cur = mysql.connection.cursor()
        cur.execute(query, (event_id,))
        mysql.connection.commit()
        cur.close()

    except Exception as e:
        flash(f"Error: {e}", "failure")
        return redirect("/events")

    flash("Event deleted successfully", "success")
    # redirect back to Events page after the action is taken
    return redirect("/events")


@app.route("/update_event/<int:event_id>", methods=["POST", "GET"])
def update_event(event_id):
    """ This is to update an event in the DB"""

    if request.method == "GET":
        query = "SELECT E.event_id, E.date, E.name, E.description, S.location \
                  FROM Events E \
                  LEFT JOIN Studios S ON S.studio_id = E.studio_id\
                  WHERE E.event_id = %s;"
        try:
            cur = mysql.connection.cursor()
            cur.execute(query, (event_id,))
            data = cur.fetchall()
            cur.close()

        except Exception as e:
            flash(f"Error: {e}", "failure")
            return redirect("/events")

    # Adding a query for the studios dropdown
        query2 = "SELECT studio_id, location FROM Studios;"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        data1 = cur.fetchall()
        cur.close()
        return render_template("update_event.j2", data=data,
                               studios=data1)
    # Updating a event using the POST method
    if request.method == "POST":
        date = request.form["date"]
        name = request.form["name"]
        description = request.form["description"]
        studio_id = request.form["studio"]

        query4 = "UPDATE Events SET date = %s,name = %s, \
                   description = %s, studio_id = %s  \
                  WHERE event_id = %s;"
        try:
            cur = mysql.connection.cursor()
            cur.execute(query4, (date, name, description,
                                 studio_id, event_id))
            mysql.connection.commit()
            cur.close()

        except Exception as e:
            flash(f"Error: {e}", "failure")
            return redirect("/events")

        flash("Event updated successfully", "success")
        # redirect back to Events page
        return redirect("/events")


# ----------------------------------------------------------------------------
# Routes for Classes page
# ----------------------------------------------------------------------------
@app.route("/classes", methods=["POST", "GET"])
def classes():
    """This is to render the classes page to display them from the DB
        as well as add new classes
    """

    if request.method == "GET":
        query1 = "SELECT C.class_id, C.date, C.name, C.size, C.instructor, \
                    CC.experience_level, S.location \
                  FROM Classes C \
                  LEFT JOIN Class_Categories CC ON \
                    C.category_id = CC.category_id \
                  LEFT JOIN Studios S ON S.studio_id = C.studio_id;"
        try:
            cur = mysql.connection.cursor()
            cur.execute(query1)
            data = cur.fetchall()
            cur.close()

        except Exception as e:
            flash(f"Error: {e}", "failure")
            return redirect("/")

        # Adding a query for the categories dropdown
        query2 = "SELECT category_id, experience_level FROM Class_Categories;"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        cat_data = cur.fetchall()
        cur.close()

        # Adding a query for the studios dropdown
        query3 = "SELECT studio_id, location FROM Studios;"
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
        try:
            cur = mysql.connection.cursor()
            cur.execute(query, (date, name, size, instructor,
                                category_id, studio_id))
            mysql.connection.commit()
        except Exception as e:
            flash(f"Error: {e}", "failure")
            return redirect("/classes")
        cur.close()

        flash("Class added successfully!", "success")
        # redirect back to Classes page
        return redirect("/classes")


@app.route("/delete_class/<int:class_id>")
def delete_class(class_id):
    """ This is to delete a class from the DB"""

    query = "DELETE FROM Classes \
             WHERE class_id = %s;"
    try:
        cur = mysql.connection.cursor()
        cur.execute(query, (class_id,))
        mysql.connection.commit()
    except Exception as e:
        flash(f"Error: {e}", "failure")
        return redirect("/classes")
    cur.close()

    flash("Class deleted successfully!", "success")
    # redirect back to Classes page after the action is taken
    return redirect("/classes")


@app.route("/update_class/<int:class_id>", methods=["POST", "GET"])
def update_class(class_id):
    """ This is to update a class in the DB"""

    if request.method == "GET":
        query = "SELECT C.class_id, C.date, C.name, C.size, C.instructor, \
                    CC.experience_level, S.location \
                  FROM Classes C \
                  LEFT JOIN Class_Categories CC \
                    ON C.category_id = CC.category_id \
                  LEFT JOIN Studios S \
                    ON S.studio_id = C.studio_id \
                  WHERE C.class_id = %s;"
        try:
            cur = mysql.connection.cursor()
            cur.execute(query, (class_id,))
            data = cur.fetchall()
            cur.close()

        except Exception as e:
            flash(f"Error: {e}", "failure")
            return redirect("/classes")

        # Adding a query for the studios dropdown
        query2 = "SELECT studio_id, location FROM Studios"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        data1 = cur.fetchall()
        cur.close()

        # Adding a query for the categories dropdown
        query5 = "SELECT category_id, experience_level FROM Class_Categories;"
        cur = mysql.connection.cursor()
        cur.execute(query5)
        data2 = cur.fetchall()
        cur.close()

        return render_template("update_class.j2", data=data,
                               studios=data1, categories=data2)

    # Updating a class using the POST method
    if request.method == "POST":
        date = request.form["date"]
        name = request.form["name"]
        size = request.form["size"]
        instructor = request.form["instructor"]
        category_id = request.form["category"]
        studio_id = request.form["studio"]

        query4 = "UPDATE Classes SET date = %s,name = %s, \
                   size = %s, instructor = %s, \
                   category_id = %s, studio_id = %s \
                 WHERE class_id = %s;"
        try:
            cur = mysql.connection.cursor()
            cur.execute(query4, (date, name, size, instructor,
                                 category_id, studio_id, class_id))
            mysql.connection.commit()
            cur.close()

        except Exception as e:
            flash(f"Error: {e}", "failure")
            return redirect("/classes")

        flash("Class updated successfully!", "success")
        # redirect back to Customers page
        return redirect("/classes")


# ----------------------------------------------------------------------------
# Routes for Scheduled page
# ----------------------------------------------------------------------------
@app.route("/scheduled", methods=["POST", "GET"])
def scheduled():
    """This is to render the scheduled page to display them from the DB
        and to add a scheduled item to the DB. This can be either a class or
        an event.
    """

    if request.method == "GET":
        query1 = "SELECT Cust.name, Classes.name, Classes.date \
                  FROM Customer_Classes AS CC \
                  INNER JOIN Customers AS Cust \
                   ON CC.customer_id = Cust.customer_id \
                  INNER JOIN Classes \
                   ON CC.class_id = Classes.class_id \
                  ORDER BY Cust.name;"
        try:
            cur = mysql.connection.cursor()
            cur.execute(query1)
            data1 = cur.fetchall()
            cur.close()

        except Exception as e:
            flash(f"Error: {e}", "failure")
            return redirect("/")

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
            try:
                cur = mysql.connection.cursor()
                cur.execute(query3, (customer_id, class_id))
                mysql.connection.commit()
            except Exception:
                flash('Error: Duplicate class entry for that customer \
                    Please try again.', 'failure')
                return redirect("/scheduled")
            cur.close()

        if event_id:
            query4 = "INSERT INTO Customer_Events (customer_id, event_id) \
                      VALUES (%s, %s);"
            try:
                cur = mysql.connection.cursor()
                cur.execute(query4, (customer_id, event_id))
                mysql.connection.commit()
                cur.close()

            except Exception:
                flash('Error: Duplicate class entry for that customer \
                    Please try again.', 'failure')
                return redirect("/scheduled")

        flash("Customer schedule added successfully!", "success")
        # redirect back to Scheduled page
        return redirect("/scheduled")


# Note how I include 2 parameters in the route decorator here... It took
# me a while to figure out how to do this.
@app.route("/delete_customer_class/<string:customer_name>/<string:class_name>")
def delete_customer_class(customer_name, class_name):
    """This is to delete a scheduled class from the DB"""

    query4 = "DELETE Customer_Classes \
              FROM Customer_Classes \
              JOIN Customers AS Cust \
                ON Customer_Classes.customer_id = Cust.customer_id \
              JOIN Classes \
                ON Customer_Classes.class_id = Classes.class_id \
              WHERE Cust.name = %s AND Classes.name = %s;"
    try:
        cur = mysql.connection.cursor()
        cur.execute(query4, (customer_name, class_name,))
        mysql.connection.commit()
        cur.close()

    except Exception as e:
        flash(f"Error: {e}", "failure")
        return redirect("/scheduled")

    flash("Customer schedule deleted successfully!", "success")
    # redirect back to Studios page after the action is taken
    return redirect("/scheduled")


@app.route("/delete_customer_event/<string:customer_name>/<string:event_name>")
def delete_customer_event(customer_name, event_name):
    """This is to delete a scheduled event from the DB"""

    query5 = "DELETE Customer_Events \
              FROM Customer_Events \
              JOIN Customers AS Cust \
                ON Customer_Events.customer_id = Cust.customer_id \
              JOIN Events \
                ON Customer_Events.event_id = Events.event_id \
              WHERE Cust.name = %s AND Events.name = %s;"
    try:
        cur = mysql.connection.cursor()
        cur.execute(query5, (customer_name, event_name,))
        mysql.connection.commit()
        cur.close()

    except Exception as e:
        flash(f"Error: {e}", "failure")
        return redirect("/scheduled")
    cur.close()

    flash("Customer schedule deleted successfully!", "success")
    # redirect back to Studios page after the action is taken
    return redirect("/scheduled")


@app.route("/update_customer_class/<string:customer_name>/<string:class_name>",
           methods=["GET"])
def update_customer_class(customer_name, class_name):
    """This is to populate the update a scheduled class from the DB"""

    if request.method == "GET":
        query = "SELECT Cust.customer_id, CC.class_id, Cust.name, Classes.name, Classes.date \
                FROM Customer_Classes AS CC \
                INNER JOIN Customers AS Cust \
                ON CC.customer_id = Cust.customer_id \
                INNER JOIN Classes \
                ON CC.class_id = Classes.class_id \
                WHERE Cust.name = %s AND Classes.name = %s;"
        try:
            cur = mysql.connection.cursor()
            cur.execute(query, (customer_name, class_name,))
            data = cur.fetchall()
            cur.close()

        except Exception as e:
            flash(f"Error: {e}", "failure")
            return redirect("/scheduled")

        # query for list of customer names to populate in dropdown
        query1 = "SELECT customer_id, name FROM Customers;"
        cur = mysql.connection.cursor()
        cur.execute(query1)
        customer_names = cur.fetchall()
        cur.close()

        # query for list of class names + Class Time & Date to populate in dropdown
        query2 = "SELECT class_id, name, date FROM Classes;"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        class_names = cur.fetchall()
        cur.close()

        return render_template("update_customer_class.j2", data=data,
                               customer_dropdown=customer_names,
                               class_dropdown=class_names)


# update customer class using the POST method. This is to slim down on the code
# in the update_customer_class route and to make it easier to read.
@app.route("/cc_updating", methods=["POST"])
def cc_updating():
    """This is to update a scheduled class from the DB"""

    current_class_id = request.form.get('current_class_id')
    new_class_id = request.form.get('class_dropdown')
    current_user = request.form.get('current_customer_id')
    cur_class_name = request.form.get('current_class_name')
    cur_cust_name = request.form.get('current_customer_name')

    # update the database with the new class id and current customer id
    query = "UPDATE Customer_Classes \
                SET class_id = %s \
                WHERE customer_id = %s AND class_id = %s;"

    # try-except to prevent a duplicate entry of classes for a customer
    try:
        cur = mysql.connection.cursor()
        cur.execute(query, (new_class_id, current_user, current_class_id,))
        mysql.connection.commit()
        cur.close()

    except Exception as e:
        print(f'Error: {e}')
        #  this will flash a message to the customer for dupped entries
        # and then redirect them back to the page they were on
        # CITATION: https://flask.palletsprojects.com/en/1.1.x/api/#flask.flash
        flash(f"Error: there was a duplicate entry for customer \
              {cur_cust_name}. Please try again.", "failure")
        return redirect(f"/update_customer_class/{cur_cust_name}/{cur_class_name}")

    flash("Customer schedule updated successfully!", "success")
    # redirect back to Scheduled page
    return redirect("/scheduled")


@app.route("/update_customer_event/<string:customer_name>/<string:event_name>",
           methods=["GET"])
def update_customer_event(customer_name, event_name):
    """This is to populate the update a scheduled event from the DB"""

    if request.method == "GET":
        query = "SELECT Cust.customer_id, CE.event_id, Cust.name, Events.name, Events.date \
                FROM Customer_Events AS CE \
                INNER JOIN Customers AS Cust \
                ON CE.customer_id = Cust.customer_id \
                INNER JOIN Events \
                ON CE.event_id = Events.event_id \
                WHERE Cust.name = %s AND Events.name = %s;"
        try:
            cur = mysql.connection.cursor()
            cur.execute(query, (customer_name, event_name,))
            data = cur.fetchall()
            cur.close()

        except Exception as e:
            flash(f"Error: {e}", "failure")
            return redirect("/scheduled")

        # query for list of customer names to populate in dropdown
        query1 = "SELECT customer_id, name FROM Customers;"
        cur = mysql.connection.cursor()
        cur.execute(query1)
        customer_names = cur.fetchall()
        cur.close()

        # query for list of event names + Event Time & Date to populate in dropdown
        query2 = "SELECT event_id, name, date FROM Events;"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        event_names = cur.fetchall()
        cur.close()

        return render_template("update_customer_event.j2", data=data,
                               customer_dropdown=customer_names,
                               event_dropdown=event_names)


# update customer event using the POST method. This is to slim down on the code
# in the update_customer_event route and to make it easier to read.
@app.route("/ce_updating", methods=["POST"])
def ce_updating():
    """This is to update a scheduled event from the DB"""

    current_event_id = request.form.get('current_event_id')
    new_event_id = request.form.get('event_dropdown')
    current_user = request.form.get('current_customer_id')
    cur_event_name = request.form.get('current_event_name')
    cur_cust_name = request.form.get('current_customer_name')

    query = "UPDATE Customer_Events \
                SET event_id = %s \
                WHERE customer_id = %s AND event_id = %s;"
    # try-except to prevent a duplicate entry of events for a customer
    try:
        cur = mysql.connection.cursor()
        cur.execute(query, (new_event_id, current_user, current_event_id,))
        mysql.connection.commit()
        cur.close()

    except Exception as e:
        print(f'Error: {e}')
        #  this will flash a message to the customer for dupped entries
        # and then redirect them back to the page they were on
        # CITATION: https://flask.palletsprojects.com/en/1.1.x/api/#flask.flash

        flash(f"Error: there was a duplicate entry for customer \
              {cur_cust_name}. Please try again.", "failure")
        return redirect(f"/update_customer_event/{cur_cust_name}/{cur_event_name}")

    flash("Customer schedule updated successfully!", "success")
    # redirect back to Scheduled page
    return redirect("/scheduled")


# ----------------------------------------------------------------------------
# Routes for Categories page
# ----------------------------------------------------------------------------
@app.route("/categories", methods=["POST", "GET"])
def categories():
    """This is to display the categories page
        and to add a new category to the DB
    """

    if request.method == "GET":
        query1 = "SELECT * FROM Class_Categories;"

        try:
            cur = mysql.connection.cursor()
            cur.execute(query1)
            data = cur.fetchall()
            cur.close()

        except Exception as e:
            flash(f"Error: {e}", "failure")
            return redirect("/")

        return render_template("categories.j2",
                               data=data)

    # Adding a Category using the POST method
    if request.method == "POST":
        experience_level = request.form.get("experience_level")
        query2 = "INSERT INTO Class_Categories (experience_level) \
                  VALUES (%s);"
        try:
            cur = mysql.connection.cursor()
            cur.execute(query2, (experience_level,))
            mysql.connection.commit()
            cur.close()

        except Exception as e:
            flash(f"Error: {e}", "failure")
            return redirect("/categories")

        flash("Category added successfully!", "success")
        # redirect back to Categories page
        return redirect("/categories")


@app.route("/delete_category/<int:category_id>")
def delete_category(category_id):
    """This is to delete a category from the DB"""

    query3 = "DELETE FROM Class_Categories \
              WHERE category_id = %s;"
    try:
        cur = mysql.connection.cursor()
        cur.execute(query3, (category_id,))
        mysql.connection.commit()
        cur.close()

    except Exception as e:
        flash(f"Error: {e}", "failure")
        return redirect("/categories")

    flash("Category deleted successfully!", "success")
    # redirect back to Categories page after the action is taken
    return redirect("/categories")


@app.route("/update_category/<int:category_id>", methods=["POST", "GET"])
def update_category(category_id):
    """This is to render the update category page to update them in the DB"""

    if request.method == "GET":
        query1 = "SELECT * FROM Class_Categories \
                  WHERE category_id = %s;"
        try:
            cur = mysql.connection.cursor()
            cur.execute(query1, (category_id,))
            data = cur.fetchall()
            cur.close()

        except Exception as e:
            flash(f"Error: {e}", "failure")
            return redirect("/categories")

        return render_template("update_category.j2",
                               data=data)

    # Updating a Category using the POST method
    if request.method == "POST":
        experience_level = request.form.get("experience_level")
        query2 = "UPDATE Class_Categories \
                  SET experience_level = %s \
                  WHERE category_id = %s;"
        try:
            cur = mysql.connection.cursor()
            cur.execute(query2, (experience_level, category_id,))
            mysql.connection.commit()
            cur.close()

        except Exception as e:
            flash(f"Error: {e}", "failure")
            return redirect("/categories")

        flash("Category updated successfully!", "success")
        # redirect back to Categories page
        return redirect("/categories")


# ----------------------------------------------------------------------------
# Routes for Database Refresh
# ----------------------------------------------------------------------------
@app.route("/refresh_db")
def refresh_db():
    """This is to refresh the database with the DDL file
        This is for testing purposes only for us and the TA's. Essentially it
        saves us from having to log into the database and run the source
        command to refresh the database.
    """
    try:
        with open("sql/studio_ddl.sql", "r") as file:
            sql_script = file.read()

        # Split script into individual statements and execute them
        cur = mysql.connection.cursor()
        for statement in sql_script.split(';'):
            if statement.strip():  # if a line exists, execute it
                cur.execute(statement)
        mysql.connection.commit()
        cur.close()

    except Exception as e:
        flash(f'There is an error refreshing the database: {e}', 'failure')
        return redirect("/")

    # flash a response that shows the database was refreshed
    flash('The database has been refreshed with the original test data \
           and relationships!', 'success')
    return redirect("/")


# Listener
# Run python app.py to run locally and then browse to http://localhost:8000
# change the port number if deploying on the flip servers
if __name__ == "__main__":
    app.run(port=8000, debug=True)

# NOTE: You can use gunicorn to start the app instead, run the following::
# gunicorn -b 0.0.0.0:8000 app:app
# NOTE: We run this on port 17001 on flip
