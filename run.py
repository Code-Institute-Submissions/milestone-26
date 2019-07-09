"""
Simple Flask app, which prints whatever POST data it receives
for API testing purposes.
"""

import os
from flask import Flask, request

APP = Flask(__name__)


@APP.route("/", methods=["GET", "POST"])
def index():
    """
    Main route, which simply prints out the JSON content
    and returns a status of 200
    """

    print(request.json)
    return "OK", 200


APP.run(host=os.getenv("IP", "0.0.0.0"),
        port=int(os.getenv("PORT", "5000")), debug=False)
