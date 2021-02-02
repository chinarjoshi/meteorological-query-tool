'''
Uses Python + Flask to handle all HTTP request and application routes. The main
idea behind the implementation is to retrieve specifications from a formatted
HTML form and make queries to the NCLC archive of meteorological data and return
the output as json. The user can choose either a visualization of long term trends
or query data from a specific date and location.
'''
from flask import Flask, render_template, request, session, jsonify
from flask_session import Session
from sqlite3.dbapi2 import OperationalError
import sqlite3
import csv

# Initialize Flask and give cookie to browser to start session.
app = Flask(__name__)
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

class Constants:
    '''
    Creates useful data associations using python's powerful data structure
    comprehensions. Acts as a container for months, station names, and all
    mandatory and optional data fields for HTML form.
    '''
    def __init__(self, database):
        'Takes name of the SQL index as constructor parameter and assembles the constants.'
        db = sqlite3.connect(f'static/{database}.db').cursor()
        self.commands = self.get_commands()
        # Associates name of the month with its numeric value through a list comprehension
        # that enumerates the month names.
        self.months = [{'name': month, 'numeric': index + 1} for index, month in enumerate(
            ('January', 'February', 'March', 'April', 'May', 'June',
                'July', 'August', 'September', 'October', 'November', 'December')
        )]
        # Associates human readable data field name with database column name through
        # list comprehension that zips an in-line tuple of names with a generator
        # expression that selects column name from an SQL query that returns all
        # column information.
        self.fields = [{'client': client, 'database': database} for client, database in zip(
            ('Station', 'Name', 'Date', 'Average Cloud Cover', 'Precipitation', 'Percent Sun',
                'Snowfall', 'Snow Depth', 'Average Temp', 'Max Temp', 'Min Temp', 'Total Sun'),
            [column for column in db.execute(self.commands['columns'])]
        )]
        # Selects all station names.
        self.stations = [station for station in db.execute(self.commands['stations'])]
    
    def get_commands(self):
        'Opens SQL file and returns dictionary comprehension of all rows'
        with open('queries.sql') as file:
            return {row['name']: row['command'] for row in csv.DictReader(file)}

constants = Constants('climate_index')

@app.route('/')
def index():
    'Renders main HTML page and creates browser cookie if not already in session.'
    if 'history' not in session:
        session['history'] = []
    return render_template('index.html', months=constants.months, 
                            fields=constants.fields, stations=constants.stations)

@app.route('/query')
def query():
    '''
    Returns row from database where the station name and date match with
    input given via URL variables.
    '''
    # Associates the variable field name with GET request from client via
    # dictionary comprehension, looping through a set of fields.
    fields = {field: request.args.get(field) for field in {'day', 'month', 'year'}}
    # Formats the date using an f-string, but fields must be int-casted before
    # forcing fixed width.
    date = f"{fields['year']}-{int(fields['month']):02}-{int(fields['day']):02}"
    db = sqlite3.connect('static/climate.db').cursor()
    # Associates type of input with database output through list comprehension
    # that zips client names with select query, and returns list as json.
    return jsonify([{'name': name, 'value': value} for name, value in zip(
        (field['client'] for field in constants.fields),
        db.execute(constants.commands('output'), fields, date).fetchone()
    )])

@app.route('/history')
def history():
    'Returns past queries from brower cookie via environmental variable.'
    return jsonify(session['history'] if 'history' in session else 'Empty')
