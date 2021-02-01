'''
Uses Python + Flask to handle all HTTP request and application routes. The main
idea behind the implementation is to retrieve specifications from a formatted
HTML form and make query to the NCLC archive of meteorological data and return
the output as json. The user can choose either a visualization of long term trends
or query data from a specific date and location.
'''
from flask import Flask, render_template, request, session, jsonify
from flask_session import Session
import sqlite3

# Initialize Flask and give cookie to browser to start session.
app = Flask(__name__)
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# Defines file name of database.
DATABASE = 'climate_index'

conn = sqlite3.connect(f'static/{DATABASE}.db')
db = conn.cursor()

# Match name of the month with its numeric value through a list comprehension
# that enumerates the month names.
MONTHS = [{'name': month, 'numeric': index + 1} for index, month in enumerate(
    ('January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December')
)]

# Matches human readable data field name with database column name through
# list comprehension that zips an in-line tuple of names with a generator
# expression that selects column name from an SQL query that returns all
# column information.
FIELDS = [{'client': client, 'database': database} for client, database in zip(
    ('Station', 'Name', 'Date', 'Average Cloud Cover', 'Precipitation', 'Percent Sun',
        'Snowfall', 'Snow Depth', 'Average Temp', 'Max Temp', 'Min Temp', 'Total Sun'),
    (column[1] for column in 
        db.execute(
            'PRAGMA table_info ("climate")'
        ).fetchall())
    )
]

# Selects all station names.
STATIONS = db.execute(
    'SELECT DISTINCT name '
    'FROM climate'
).fetchall()

# Connection must be closed as same object cannot be reused in multiple functions.
conn.close()

@app.route('/')
def index():
    'Renders main HTML page and creates browser cookie if not already in session.'
    if 'history' not in session:
        session['history'] = []
    return render_template('index.html', months=MONTHS, fields=FIELDS, stations=STATIONS)

@app.route('/query')
def query():
    '''
    Returns row from database where the station name and date match with
    input given via URL variables.
    '''
    # Matches the variable field name with GET request from client via dictionary comprehension.
    fields = {field: request.args.get(field) for field in {'day', 'month', 'year'}}
    # Formats the date using an f-string, but fields must be int-casted before forcing fixed width.
    date = f"{fields['year']}-{int(fields['month']):02}-{int(fields['day']):02}"
    db = sqlite3.connect(f'static/{DATABASE}.db').cursor()

    # # Use this to canonicalize the data from GET request since spaces are not allowed in URL.
    # # Note: instead I can add another value to 'fields' that associates field with an index
    # fields['station'] = [letter if letter != ' ' else '_' for letter in fields['station']]

    # Matches type of input with database output through list comprehension
    # that zips client names with select query, and returns list as json.
    return jsonify([{'name': name, 'value': value} for name, value in zip(
        (field['client'] for field in FIELDS),
        db.execute(
            'SELECT * '
            'FROM climate '
           f'WHERE name LIKE "%{fields["station"][2:-3]}%" '
           f'AND date LIKE "%{date}%" '
            'ORDER BY name DESC '
            'LIMIT 1'
        ).fetchone()
    )])

@app.route('/history')
def history():
    'Returns past queries from brower cookie via environmental variable.'
    return jsonify(session['history'] if 'history' in session else 'Empty')
