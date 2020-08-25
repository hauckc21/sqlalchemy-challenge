#import dependencies
import numpy as np
import datetime as datetime
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#Create Database
engine = create_engine("sqlite:///hawaii.sqlite")

#reflect existing datebase
base = automap_base()
#reflect tables
base.prepare(engine, reflect=True)

#references for table
measurement = base.classes.measurement
station = base.classes.station

#Flask App Setup
app = Flask(__name__)

# #Flask routes
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"List all available api routes:<br>"
        f"<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api.v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end"
    )

# /api/v1.0/precipitation
# Convert the query results to a dictionary using date as the key and prcp as the value.
# # Return the JSON representation of your dictionary.

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    
    results = session.query(measurement.date, measurement.prcp).all()

    session.close()

    precip_data = []
    for date, prcp in results:
        precip_dict = {}
        precip_dict["Date"] = date
        precip_dict["Precipitation"] = prcp
        precip_data.append(precip_dict)

    return jsonify(precip_data)


# /api/v1.0/stations
# Return a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

    results = session.query(station.station, station.name).all()

    session.close()

    #query list of stations
    station_data = []
    for station, name in results:
        station_dict = {}
        station_dict["station ID"] = station
        station_dict["station name"] = name
        station_data.append(station_data)
    return jsonify(station_data)


# /api/v1.0/tobs
# Query the dates and temperature observations of the most active station for the last year of data.
# Return a JSON list of temperature observations (TOBS) for the previous year.
@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    #date query
    date_query = session.query(measurement.date).order_by(measurement.date.desc()).first()
    last_date = datetime.strptime(latest_date_query[0], '%Y-%m-%d').date()
    one_year = last_date - relativedelta(months= 12)

    #temperature query
    results = session.query(measurement.date, measurement.tobs).filter(measurement.date >= year_ago).all()

    session.close()

    temp_data = []
    for date, tobs in results:
        temp_dict = {}
        temp_dict["Date"] = date
        temp_dict["Temperature"] = tobs
        temp_date.append(temp_dict)

    return jsonify(temp_data)

# /api/v1.0/<start> and /api/v1.0/<start>/<end>
# Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
# When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
# When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.
@app.route("/api/v1.0/start")
def start_date(start):
    # Create session from Python to the DB
    session = Session(engine)
    start_date = datetime.strptime(start, '%Y-%m-%d').date()

    temp_stats = session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).filter(measurement.date >= start_date).all()
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

#-------------------------------------------------------------------

@app.route("/api/v1.0/start/end")
def start_end_date(start, end):
    session = Session(engine)

    start_date = datetime.strptime(start, '%Y-%m-%d').date()
    end_date = datetime.strptime(end, '%Y-%m-%d').date()

    temp_query = session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).\
        filter(measurement.date >= start_date).filter(measurement.date <= end_date).all()
    temps_data_results = list(np.ravel(temp_query))
    
    min_temp = temps_data_results[0]
    max_temp = temps_data_results[1]
    avg_temp = temps_data_results[2]
    
    temp_query_data = []
    temp_data_dict = [{"Start Date": start_date},
                       {"End Date": end_date},
                       {"Minimum Temperature": min_temp},
                       {"Maximum Temperature": max_temp},
                       {"Average Temperature": avg_temp}]

    temp_stats_data.append(temp_data_dict)
    
    return jsonify(temp_query_data)
#------------------------------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True)












