"""
 This block demonstrates how to make a GET request to retrieve a specific user
 by their ID (e.g., user with ID 1).
 response = requests.get('http://localhost:5000/api/users/1')
 print(response.json()['name'])

 Explanation:
 - requests.get(...): Sends an HTTP GET request to the specified URL.
 - .json(): Parses the JSON response body into a Python dictionary.
 - ['name']: Accesses the 'name' key from the resulting user dictionary.
 -----------------------------------------------------------------------------

Key Features:
- User authentication model (though simple for demo)
- CRUD operations for resources
- Uses Flask and Flask-Restful for API creation
- Uses Flask-SQLAlchemy for ORM (configured with SQLite in-memory db)

Usage:
1. Ensure Python required libraries (Flask, Flask-RESTful, Flask-SQLAlchemy)
2. Run the script: 'python app.py' (after activating virtual environment)
3. Access API at 'http://localhost:5000/api/users/' (or related endpoints)

Data is stored in a SQLite database file named 'database.db'

Reference: 
        Caleb Curry - youtube
        REST API Crash Course - Introduction+Full Python API Tutorial

Author: David Sanghara
Date : June 25, 2025
Version: 1.0.0
"""

# Core Flask imports
import requests
import json


'''
# prints out the first record
response = requests.get('http://localhost:5000/api/users/1')
print(response.json()['name'])


#response = requests.get('http://localhost:5000/api/users')
for data in response.json()['name']:
    print(data[])
'''

    
# 1. Make the GET request to your API endpoint for all users.
# The trailing slash is important as defined in your Flask API routing.
response = requests.get('http://localhost:5000/api/users/') # Added trailing slash as per your API


# Raise an HTTPError for bad responses (4xx client errors or 5xx server errors).
# This is good practice for robust error handling in client applications.
response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)

# 2. Parse the JSON response
# It's expected to be a list of dictionaries, e.g., [{"id": 1, "name": "Alice", ...}, ...]
users_data = response.json()


# 3. Iterate through each user dictionary in the list
# Each 'user' variable in this loop will be a dictionary representing one user.

for user in users_data:
        # Access the 'id', 'name', and 'email' keys from each 'user' dictionary
        # and print them individually.
        print('user: '+ str(user['id']))
        print(user['name'])
        print(user['email'])


        # Using an f-string for a more readable and formatted output.
        # It directly embeds variable values and expressions into the string.
        print(f"The name of user# {str(user['id'])} is {user['name']} and their email address is {user['email']}.")

        # Print an empty line for better readability between user entries.       
        print()

