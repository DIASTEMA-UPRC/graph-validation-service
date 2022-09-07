# Import custom Libraries
from pb_check import playbook_check as pbc

# Import Libraries
from flask import Flask, request, Response, make_response
import os

""" Environment Variables """
# Flask app Host and Port
HOST = os.getenv("HOST", "localhost")
PORT = int(os.getenv("PORT", 5000))

""" Global variables """
# The name of the flask app
app = Flask(__name__)

""" Flask endpoints """
# Start The Graph Validation Service Route
@app.route("/validation", methods=["POST"])
def function_job():
    # Get json body (playbook) to validate a graph
    print("[INFO] Accepted Request.")
    json_body = request.json

    # True / False | playbook valid or not
    pb_validity = pbc(json_body)

    # Reurn the status and the reason if the status is 409
    if(pb_validity[0] == True):
        return pb_validity[1], 200
    else:
        return pb_validity[1], 409

""" Main """
# Main code
if __name__ == "__main__":
    app.run(HOST, PORT, True)