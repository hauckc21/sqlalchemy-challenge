import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from datetime import datetime, date, time
from dateutil.relativedelta import relativedelta

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
        f"List all available api routes:<br/>"
        f" <br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end"
    )

#------------------------------------------------

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create session (link) from Python to the DB
    session = Session(engine)

    # Query all precipitation data
    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()
    
    precip_data = []
    for date, prcp in results:
        precip_dict = {}
        precip_dict["Date"] = date
        precip_dict["Precipitation"] = prcp
        precip_data.append(precip_dict)  

    return jsonify(precip_data)

#------------------------------------------------

@app.route("/api/v1.0/stations")
def stations():
    # Create session (link) from Python to the DB
    session = Session(engine)

    # Query for list of stations
    results = session.query(Station.station, Station.name).all()

    session.close()
    
    station_data = []
    for station, name in results:
        station_dict = {}
        station_dict["Station ID"] = station
        station_dict["Station Name"] = name
        station_data.append(station_dict)
    
    return jsonify(station_data)

#------------------------------------------------

@app.route("/api/v1.0/tobs")
def tobs():
    # Create session from Python to the DB
    session = Session(engine)
    
    # Latest date
    recent_date_query = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    recent_date = datetime.strptime(recent_date_query[0], '%Y-%m-%d').date()
    # Date 12 months ago
    one_year = recent_date - relativedelta(months= 12)

    # Query for temperature in the last 12 months
    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= one_year).all()

    session.close()
    
    temp_data = []
    for date, tobs in results:
        temp_dict = {}
        temp_dict["Date"] = date
        temp_dict["Temperature"] = tobs
        temp_data.append(temp_dict)  

    return jsonify(temp_data)

#------------------------------------------------

@app.route("/api/v1.0/<start>")
def start_date(start):
    # Create session from Python to the DB
    session = Session(engine)

    start_date = datetime.strptime(start, '%Y-%m-%d').date()

    temp_stats = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start_date).all()
    temps_stats_results = list(np.ravel(temp_stats))
    
    min_temp = temps_stats_results[0]
    max_temp = temps_stats_results[1]
    avg_temp = temps_stats_results[2]
    
    temp_stats_data= []
    temp_stats_dict = [{"Start Date": start},
                       {"Minimum Temperature": min_temp},
                       {"Maximum Temperature": max_temp},
                       {"Average Temperature": avg_temp}]

    temp_stats_data.append(temp_stats_dict)
    
    return jsonify(temp_stats_data)


#------------------------------------------------

@app.route("/api/v1.0/start/end")
def start_end_date(start, end):
    # Create session from Python to the DB
    session = Session(engine)

    start_date = datetime.strptime(start, '%Y-%m-%d').date()
    end_date = datetime.strptime(end, '%Y-%m-%d').date()

    temp_stats = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    temps_stats_results = list(np.ravel(temp_stats))
    
    min_temp = temps_stats_results[0]
    max_temp = temps_stats_results[1]
    avg_temp = temps_stats_results[2]
    
    temp_stats_data = []
    temp_stats_dict = [{"Start Date": start_date},
                       {"End Date": end_date},
                       {"Minimum Temperature": min_temp},
                       {"Maximum Temperature": max_temp},
                       {"Average Temperature": avg_temp}]

    temp_stats_data.append(temp_stats_dict)
    
    return jsonify(temp_stats_data)

























#------------------------------------------------

if __name__ == '__main__':
    app.run(debug=True)