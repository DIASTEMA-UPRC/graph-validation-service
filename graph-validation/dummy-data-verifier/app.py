# Import Libraries
from flask import Flask, request, jsonify
import os

""" Environment Variables """
# Flask app Host and Port
HOST = os.getenv("HOST", "localhost")
PORT = int(os.getenv("PORT", 5001))

""" Global variables """
# The name of the flask app
app = Flask(__name__)

""" Flask endpoints """
# Start The Graph Validation Service Route
@app.route("/", methods=["POST"])
def function_job():
    # Get json body (playbook) to validate a graph
    print("[INFO] Accepted Request.")
    json_body = request.json
    print(json_body)

    cleaning_results = {"result": "valid", "reason" : "No reason."}
    # cleaning_results = {"result": "suggested", "reason" : "An okey reason."}
    # cleaning_results = {"result": "invalid", "reason" : "Big reason!!!"}
    return jsonify(cleaning_results)

""" Main """
# Main code
if __name__ == "__main__":
    app.run(HOST, PORT, True)