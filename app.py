import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import pandas as pd
import datetime as dt

from flask import Flask, jsonify

# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Flask Setup
app = Flask(__name__)

# Flask Routes
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/2017-07-01<br/>"
        f"/api/v1.0/2017-07-01/2017-07-10<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    last_date = dt.date(2017, 8 ,23)
    year_ago = last_date - dt.timedelta(days=365)
    session = Session(engine)
    date_precip = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date.between(year_ago, last_date)).all()
    session.close()
    date_precipitation = {date: prcp for date, prcp in date_precip}
    return jsonify(date_precipitation)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    all_stations = session.query(Station.station).all()
    session.close()
    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    last_date = dt.date(2017, 8 ,23)
    year_ago = last_date - dt.timedelta(days=365)
    session = Session(engine)
    date_tobs = session.query(Measurement.tobs).\
    filter(Measurement.station == "USC00519281").\
    filter(Measurement.date.between(year_ago, last_date)).all()
    session.close()
    return jsonify(date_tobs)

@app.route("/api/v1.0/2017-07-01")
def start():
    session = Session(engine)
    start_date = '2017-07-01'
    max_tobs1 = (session.query(func.max(Measurement.tobs))).filter(Measurement.date >= start_date).all()
    min_tobs1 = (session.query(func.min(Measurement.tobs))).filter(Measurement.date >= start_date).all()
    avg_tobs1 = (session.query(func.avg(Measurement.tobs))).filter(Measurement.date >= start_date).all()
    session.close()
    temperatures1 = {
        "Maximum Temperature" : max_tobs1,
        "Minimum Temperature": min_tobs1,
        "Average Temperature": avg_tobs1
    }
    return jsonify(temperatures1)

@app.route("/api/v1.0/2017-07-01/2017-07-10")
def end():
    session = Session(engine)
    start_date = '2017-07-01'
    end_date = '2017-07-10'
    max_tobs_2 = (session.query(func.max(Measurement.tobs))).filter(Measurement.date > start_date).filter(Measurement.date < end_date).all()
    min_tobs_2 = (session.query(func.min(Measurement.tobs))).filter(Measurement.date > start_date).filter(Measurement.date < end_date).all()
    avg_tobs_2 = (session.query(func.avg(Measurement.tobs))).filter(Measurement.date > start_date).filter(Measurement.date < end_date).all()
    session.close()
    temperatures_2 = {
        "Maximum Temperature" : max_tobs_2,
        "Minimum Temperature": min_tobs_2,
        "Average Temperature": avg_tobs_2
    }
    return jsonify(temperatures_2)

if __name__ == "__main__":
    app.run(debug=True)