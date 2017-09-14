from flask import Flask, request, redirect, render_template, session, flash
import pprint
from mysqlconnection import MySQLConnector
app = Flask(__name__)
mysql = MySQLConnector(app,'myfriends')

@app.route('/')
def index():
    query = "select concat_ws(' ', first_name, last_name) as name, age, date_format(created_at, '%M %d') as date, date_format(created_at, '%Y') as year from myfriends;"  
    friends = mysql.query_db(query)
    # pp = pprint.PrettyPrinter(indent=4)
    # pp.pprint(friends)
    return render_template('index.html',all_friends=friends)


@app.route('/friends', methods=['POST'])
def create():
    # Write query as a string. Notice how we have multiple values
    # we want to insert into our query.
    query = "INSERT INTO myfriends (first_name, last_name, age, created_at, updated_at) VALUES (:first_name, :last_name, :age, NOW(), NOW())"
    # We'll then create a dictionary of data from the POST data received.
    the_name = request.form['name'].split()

    first = the_name[0]
    last = the_name[1]

    data = {
             'first_name': first,
             'last_name':  last,
             'age': request.form['age']
           }
    # Run query, with dictionary values injected into the query.
    mysql.query_db(query, data)
    return redirect('/')


app.run(debug=True)
