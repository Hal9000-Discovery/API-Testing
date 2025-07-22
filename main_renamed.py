# main_renamed.py
# This file is part of the REST API project.
# It is a simple Flask application that serves as the main entry point.
# It has been renamed from 'main.py' to 'main_renamed.py' to avoid conflicts.


from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "Home"


if __name__ == "__main__":
    app.run(debug=True)