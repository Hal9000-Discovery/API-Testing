"""
This module defines a simple REST API for managing users

It provides a set of endpoints (GET, POST, PUT, DELETE) to interact with a collection stored in-memory dictionary 
for demonstration purposes.
- Retrieving all users (GET /api/users/)
- Creating a new user (POST /api/users/)
- Retrieving a specific suer by ID (GET /api/users/<int:id>)

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
        Dave Gray - youtube
        Python REST API Tutorial for Beginners | How to Build a Flask REST API

Author: David Sanghara
Date : June 25, 2025
Version: 1.0.0
"""

# Core Flask imports
from flask import Flask, request, jsonify

# Flask-SQLAlchemy for Object-Relational Mapping (ORM) to interact with databases
from flask_sqlalchemy import SQLAlchemy

# Flask-RESTful for building REST APIs easily
# Resource: Base class for API endpoints
# Api: Manages routing for API resources
# reqparse: For parsing and validating request arguments (e.g., from JSON body)
# fields: Helper for defining how Python objects should be serialized to API output
# marshal_with: Decorator to apply output formatting (serialization)
# abort: Helper for sending HTTP error responses
from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort


# Import from other files ------------
#from application import names



# --------------------------
# Flask App and Database Setup
# --------------------------

# Initialize the Flask application
app = Flask(__name__)

# Configure SQLAlchemy to use a SQLite database.
# 'sqlite:///database.db' means a file-based SQLite database in the project directory.
# For production, this would typically be a more robust database like PostgreSQL or MySQL.
app.config['SQLALCHEMY_DATABASE_URI']  = 'sqlite:///database.db'

# Disable SQLAlchemy event system for better performance if not needed,
# or to suppress a common warning.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the SQLAlchemy extension with the Flask app
db = SQLAlchemy(app)

# Initialize the Flask-RESTful API extension with the Flask app
api = Api(app)


# --------------------------
# Database Model Definition
# --------------------------

# Define a dictionary to specify how the UserModel objects should be serialized (marshaled)
# when returned as API responses. This ensures consistent output format.
userFields  =  {
        'id': fields.Integer,    # The 'id' field will be an integer
        'name': fields.String,   # The 'name' field will be a string
        'email': fields.String   # The 'email' field will be a string 
}

# Define the User database model.
# This class represents a table in our database.
class UserModel(db.Model):
        # Set the table name explicitly (optional, defaults to class name lowercase)
        __tablename__ = 'users'

        # Define table columns
        # id: Primary key, automatically increments (Integer)
        id =   db.Column(db.Integer,  primary_key=True)
        # name: String up to 80 chars, must be unique, cannot be null
        name = db.Column(db.String(80), unique=True, nullable=False)
        # email: String up to 80 chars, must be unique, cannot be null
        email = db.Column(db.String(80), unique=True, nullable=False)

        # __repr__ method provides a string representation of a UserModel object.
        # This is helpful for debugging and logging.
        def __repr__(self):
               return f"User(name  =  {self.name}, email =  {self.email})"


# Create the database tables if they don't already exist.
# This should be run once when setting up the database, or in a migration script.
# For this simple example, it's placed here to run on app startup if debug=True.
# In production, use Flask-Migrate or similar tools.
with app.app_context():
    db.create_all()






# --------------------------
# Request Argument Parsing and Validation
# --------------------------

# Create a RequestParser instance to define and validate expected arguments
# from incoming API requests (e.g., for POST and PUT methods).
user_args = reqparse.RequestParser()

# Add expected arguments for user creation/update
# 'name': Expects a string, is required, and provides a help message if missing.
user_args.add_argument(
        'name', 
        type =   str, 
        required =True, 
        help="Email cannot be blank"
)
# 'email': Expects a string, is required, and provides a help message if missing.
user_args.add_argument(
        'email',
        type=str, 
        required =  True, 
        help="Email cannot be blank"
)

# --------------------------
# API Resources (Endpoints)
# --------------------------

# Resource for handling operations on the collection of users (/api/users/)
class Users(Resource):
        # Decorator that automatically serializes the returned Python object
        # into a JSON response based on the 'userFields' definition.
        @marshal_with(userFields)
        def get(self):
                """
                Handles GET requests to /api/users/.
                Retreives and returns a list of all user records from the databased.
                """    

                 # Query all users from the UserModel table
                users = UserModel.query.all()
                return users,  200 # Return the list of users with a 200 OK status
        
        @marshal_with(userFields)
        def  post(self):
                """
                Handles POST requests to /api/users/.
                Creates a new user record in the database.
                Expects a JSON body with 'name' and 'email'.     
                """

                # Parse and validate arguments from the request body using the defined parser.
                # If required arguments are missing, Flask-RESTful automatically sends a 400 error.              
                args = user_args.parse_args()  
                
                '''
                
                '''
                
                
                # Create a new UserModel instance with data from the parsed arguments      
                user = UserModel(name=args["name"], email=args["email"])
                
                # Add the new user object to the database session                
                db.session.add(user)
                # Commit the transaction to save the new user to the database               
                db.session.commit()


                users = UserModel.query.all()
                return users, 201
        



class User(Resource):
       @marshal_with(userFields )
       def get(self,id):
                user =  UserModel.query.filter_by(id=id).first()
                if not user:
                        abort(404, "User not found")
                return user


# --------------------------
# API Routing
# --------------------------

# Add the 'Users' resource to the API, accessible via '/api/users/'.
# This handles GET (all users) and POST (create user).
api.add_resource(Users, '/api/users/')


# Add the 'User' resource to the API, accessible via '/api/users/<int:id>'.
# The <int:id> part indicates a variable path segment that should be an integer,
# which Flask-RESTful will pass as the 'id' argument to the User resource methods.
# This handles GET (single user by ID), and would handle PUT/DELETE if implemented.
api.add_resource(User, '/api/users/<int:id>')
                
# --------------------------
# Home Route (Basic Web Route)
# --------------------------

# Define a basic Flask route for the root URL ('/').
# This is separate from the Flask-RESTful API resources.
@app.route('/')
def home():
        """
        Render a simple HTML heading for the home page.
        """
        return '<h1>Flask REST API</h1>'



# --------------------------
# Application Entry Point
# --------------------------

# This block ensures that the Flask development server runs only when the script
# is executed directly (e.g., `python your_script_name.py`), not when it's imported
# as a module into another script.
if __name__ ==  '__main__':
    # Run the Flask application in debug mode.
    # debug=True:
    # - Enables an interactive debugger in the browser on error.
    # - Auto-reloads the server when code changes are detected.
    # IMPORTANT: Never use debug=True in a production environment due to security risks.
    app.run(debug=True, port=5000) # You can specify a port; 5000 is default.

    