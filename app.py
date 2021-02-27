from flask import Flask, jsonify
import datetime as dt
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# SQLite Setup -----------------------------------------------------

# Create our database connections
engine = create_engine("sqlite:///hawaii.sqlite")

# Reflect our database into classes
Base = automap_base()
Base.prepare(engine, reflect=True)

# Alias each class for easier access
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create a session link from Python to our database
session = Session(engine)

# Flask Setup -----------------------------------------------------

# Create a new instance of Flask

# __name__ variable denotes the location of the current function; by accessing this, we can tell WHERE our function is being run
 # Ex: command line, # imported into another script etc
# For more info on Dunder/magic methods: https://www.geeksforgeeks.org/dunder-magic-methods-python/

# Define the app

# If we wanted to import <this> file into another script, like example.py, we would instead write: app = Flask(example)
# In this case, the magic variable __name__ indicates we are calling Flask on THIS file, "app.py";
# the name can change, but __name__ means the location will be automatically set to __main__, which is the currently open file
app = Flask(__name__)

# Create the first route, the root:

# Creating a route
# Declare starting point of route, known as ROOT
# Forward slash / indicates the data is at the HIGHEST POINT OF THE ROUTE, the ROOT
# '''@app.route('/')'''

@app.route("/")

# Create a welcoming route that links to all other routes:
# Note that /api/vX.X/xxxxxx convention is standard for routes
def welcome():
    return (
        """
        Welcome to the Climate Analysis API!\
        Available routes:\
        /api/v1.0/precipitation\
        /api/v1.0/stations\
        /api/v1.0/tobs\
        /api/v1.0/temp/start/end\
        """
        )

# Create a route for precipitation:
@app.route("/api/v1.0/precipitation")
def precipitation():
    # calculate the previous year date limit as a datetime object
    prev_year = dt.date(2017,8,23) - dt.timedelta(days=365)
    # Store all values greater than the previous year limit, columns date and precipitation on that date
    precipitation = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= prev_year).all()
    # Combine the Jsonify() function and dictionary structures to create a JSON output for web display:
    # Dictionary comprehension: for the date, prcp columns in precipitation (above), assign date as key and prcp as value in format date:prcp
    precip = {date: prcp for date, prcp in precipitation}
    # Return a JSON of the precip dictionary
    return jsonify(precip)

# Create a route for stations:
@app.route("/api/v1.0/stations")
def stations():
    # get all station names from the database
    results = session.query(Station.station).all()
    # The ravel() function from NumPy converts the list of tuples (standard SQLAlchemy output) into a single list
    stations = list(np.ravel(results))
    # stations=stations formats the list into a JSON
    return jsonify(stations=stations)

# Create a route for temperature observations:
@app.route("/api/v1.0/tobs")
def temp_monthly():
    # Calculate lower year limit:
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    # Query the primary station (most observations) to return temperature observations for the past year:
    results = session.query(Measurement.tobs).\
      filter(Measurement.station == 'USC00519281').\
      filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

# Create a route for the statistics analysis:
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
# Create a function to be run with parameters start and end
def stats(start=None, end=None):
    # Create a list with the minimum, average, and maximum temperature observations from the Measurement table
    # We will use this to query the database
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        # The wildcard * in *sel indicates the query function should expect multiple results to be returned (minimum, maximum, and average)
        results = session.query(*sel).\
            filter(Measurement.date >= start).\
            filter(Measurement.date <= end).all()
        temps = list(np.ravel(results))
        return jsonify(temps=temps)

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

