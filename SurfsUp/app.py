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
engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)
# Base.classes.keys()

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
# @app.route("/precipitation")
# def precipitation():
#     precipitation = []
#     for row in session.query(Measurement.date, Measurement.prcp).all():
#         precipitation_dict = {}
#         precipitation_dict["date"] = row.date
#         precipitation_dict["precipitation"] = row.prcp
#         precipitation.append(precipitation_dict)
#     return jsonify(precipitation)

@app.route("/stations")
def stations():
    results = session.query(Station.station).all()
    session.close()
    stations = [list(np.ravel(results))]
    # stations = []
    # for row in session.query(Station.station).all():
    #     station_dict = {}
    #     station_dict["station"] = row.station
    #     stations.append(station_dict)
    # return jsonify(stations)

# @app.route("/tobs")
# def tobs():
#     results = session.query(Measurement.station, Measurement.date, Measurement.tobs).\
#         filter(Measurement.date >= '2023-04-23').\
#         order_by(Measurement.date).all()

#     tobs_data = []
#     for row in results:
#         tobs_dict = {}
#         tobs_dict["station"] = row.station
#     return jsonify(tobs_data)
    
if __name__ == '__main__':
    app.run(debug=True)
