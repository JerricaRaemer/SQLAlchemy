# Import the dependencies.
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
import numpy as np


#################################################
# Database Setup
#################################################

# reflect an existing database into a new model
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)
Base.classes.keys()

# Save references to each table
Station = Base.classes.station
Measurement = Base.classes.measurement

# Create our session (link) from Python to the DB
session = Session(engine)

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
        f"/api/v1.0/tobs"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    precipitation = []
    results = session.query(Measurement.date, Measurement.prcp).all()
    session.close()

    for row in results:
        precipitation_dict = {}
        precipitation_dict["date"] = row.date
        precipitation_dict["precipitation"] = row.prcp
        precipitation.append(precipitation_dict)
    return jsonify(precipitation)

@app.route("/api/v1.0/stations")
def stations():

    results = session.query(Station.station).all()
    session.close()
    stations = [list(np.ravel(results))]

    stations = []
    for row in results:
        station_dict = {}
        station_dict["station"] = row.station
        stations.append(station_dict)
    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
    results = session.query(Measurement.station, Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= '2015-04-23').\
        order_by(Measurement.date).all()
    session.close()

    tobs_data = []
    for row in results:
        tobs_dict = {}
        tobs_dict["tobs"] = row.tobs
        tobs_data.append(tobs_dict)
    return jsonify(tobs_data)
    
if __name__ == '__main__':
    app.run(debug=True)
