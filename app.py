# Dependencies
import datetime as dt
import numpy as np
import pandas as pd
from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt

# Dependencies from SQLAlchemy
import sqlalchemy
from sqlalchemy import create_engine, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

# Dependencies from Flask
from flask import Flask, jsonify

# Set up Database =============================
# Setting up engine and Base
engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()

# Reflecting the tables
Base.prepare(engine, reflect = True)

# References and session query link
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)

app = Flask(__name__)

@app.route('/')
def welcome():
    return(
        '''Welcome to the Climate Analysis API!! <br/><br/>
        Available Routes:<br/>
        /api/v1.0/precipitation<br/>
        /api/v1.0/stations<br/>
        /api/v1.0/tobs<br/>
        /api/v1.0/temp/start/end
        '''
    )

@app.route('/api/v1.0/precipitation')
def precipitation():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days = 365)
    precipitation = dict(session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= prev_year).all())
    #precip = {date: prcp for date, prcp in precipitation}
    return jsonify(precipitation)

@app.route('/api/v1.0/stations')
def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations = stations)


@app.route('/api/v1.0/tobs')
def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days = 365)
    results = list(np.ravel(session.query(Measurement.tobs).filter(Measurement.station == 'USC00519281').filter(Measurement.date >= prev_year).all()))
    return jsonify(temps = results)

@app.route('/api/v1.0/temp/<start>')
@app.route('/api/v1.0/temp/<start>/<end>')
def stats(start = None, end = None):
    #sel = [func.min(Measurement.tobs, func.avg(Measurement.tobs, func.max(Measurement.tobs)))]

    if not end:
        results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps = temps)

    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(min = temps[0], avg = temps[1], max = temps[2])