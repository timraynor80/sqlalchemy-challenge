import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/&ltStartDate&gt<br/>"
        f"/api/v1.0/&ltStartDate&gt/&ltEndDate&gt<br/>"
        f"<b>Use yyyy-mm-dd format for dates</b>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a dictionary of the last year of precipitation stats"""
    # Query precipitation data
    date = dt.datetime(2016, 8, 22)

    last_year = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date > date).all()

    session.close()

    # Create a dictionary from the row data
    prcp_dict = {}

    for date, precipitation in last_year:
        prcp_dict[date] = precipitation

    return jsonify(prcp_dict)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all of the stations"""
    # Query all stations
    results = session.query(Station.station).all()

    session.close()

    # Create a list of the stations
    station_list = list(np.ravel(results))

    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def temperatures():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a dictionary of the last year of temperature stats"""
    # Query temperature info
    tobs_date = dt.datetime(2016, 8, 17)
    active_year = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station=='USC00519281').\
        filter(Measurement.date > tobs_date).all()

    session.close()

    # Create a dictionary from the row data
    temp_dict = {}

    for date, temperature in active_year:
        temp_dict[date] = temperature

    return jsonify(temp_dict)


@app.route("/api/v1.0/<start>")

def calc_temps(start):
    session = Session(engine)

    """TMIN, TAVG, and TMAX for a list of dates.
    
    Args:
        start_date (string): A date string in the format %Y-%m-%d
        end_date (string): A date string in the format %Y-%m-%d
        
    Returns:
        TMIN, TAVE, and TMAX
    """
    
    temp_data = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= '2017-08-23').all()
    
    # Create a list of the stations
    temp_list = list(np.ravel(temp_data))
    
    return jsonify(temp_list)

@app.route("/api/v1.0/<start>/<end>")

def calc_temps_end(start, end):
    session = Session(engine)

    """TMIN, TAVG, and TMAX for a list of dates.
    
    Args:
        start_date (string): A date string in the format %Y-%m-%d
        end_date (string): A date string in the format %Y-%m-%d
        
    Returns:
        TMIN, TAVE, and TMAX
    """
    
    temp_data_end = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    
    # Create a list of the stations
    temp_list_end = list(np.ravel(temp_data_end))
    
    return jsonify(temp_list_end)


if __name__ == '__main__':
    app.run(debug=True)