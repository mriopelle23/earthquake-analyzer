#!/usr/bin/env python3
#Web application

from flask import Flask, request
from analyzer import get_earthquake_summary
from collector import db, app as collector_app
from sqlalchemy import text

request_count = 0

app = Flask(__name__)

@app.before_request
def count_request():
    global request_count
    request_count += 1

app.config.update(collector_app.config)
db.init_app(app)

@app.route("/")
def main():
    return '''
    <h2> Earthquake Analyzer</h2>
     <form action="/echo_user_input" method="POST">
         <input name="user_input">
         <input type="submit" value="Submit!">
     </form>

     <br>
     <a href="/report">View Earthquake Report</a>
     '''

@app.route("/echo_user_input", methods=["POST"])
def echo_input():
    input_text = request.form.get("user_input", "")
    return "You entered: " + input_text

@app.route("/report")
def report():
    with app.app_context():
        summary = get_earthquake_summary()
    
    return f"""
    <h2>Earthquake Report</h2>
    <p>Total Earthquakes: {summary['total_earthquakes']}</p>
    <p>Average Magnitude: {summary['average_magnitude']}</p>
    <p>Largest Earthquake: {summary['largest_magnitude']}</p>
    <p>Largest Location: {summary['largest_location']}</p>
    <br>
    <a href="/">Back</a>
    """

#Production monitoring
@app.route("/health")
def health():
    try:
        db.session.execute(text("SELECT 1"))
        return {
            "status": "healthy",
            "database": "connected",
            "service": "earthquake_analyzer"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "service": "earthquake_analyzer",
            "error": str(e)
        }, 500

#instrumentation
@app.route("/metrics")
def metrics():
    return {
        "total_requests": request_count
    }