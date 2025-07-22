"""
This module defines a simple Flask web application that serves a basic
home page and a RESTful API for managing 'Drink' items.

It demonstrates:
- Basic Flask application setup and routing.
- Dynamic configuration loading (SQLite for development, SQL Server for production).
- Defining a SQLAlchemy database model ('Drink').
- CRUD (Create, Read) operations via API endpoints:
    - GET / (home page)
    - GET /drinks (retrieve all drinks)
    - GET /drinks/<id> (retrieve a single drink by ID)
    - POST /drinks (add a new drink)

Key Features:
- Uses Flask for the web framework.
- Uses Flask-SQLAlchemy for Object-Relational Mapping (ORM) to interact with databases.
- Supports both SQLite (file-based) and Microsoft SQL Server connections.
- Includes basic error handling for API requests (e.g., missing data, duplicates, not found).

Usage:
1. Ensure Python required libraries (Flask, Flask-SQLAlchemy, pyodbc/psycopg2-binary) are installed.
2. Create a 'config.py' file in the same directory with 'DevelopmentConfig' and 'ProductionConfig'.
3. Set the FLASK_CONFIG environment variable to 'development' (for SQLite) or 'production' (for SQL Server)
   before running the application.
   - For Bash/Git Bash: `export FLASK_CONFIG=production`
   - For PowerShell: `$env:FLASK_CONFIG="production"`
4. Run the script: `python application.py` (after activating virtual environment).
5. Access API at `http://localhost:5001/` (home) or `http://localhost:5001/drinks` (API endpoints).

Data is stored in either 'data.db' (SQLite) or your configured SQL Server database.

Reference:
        Caleb Curry - youtube
        REST API Crash Course - Introduction+Full Python API Tutorial

Author: David Sanghara
Date : June 25, 2025
Version: 1.0.0
"""

# Core Flask imports
from flask import Flask, jsonify, request       # Flask: The main web application class
                                                # jsonify: Helper to convert Python dicts/lists to JSON responses
                                                # request: Object for accessing incoming request data (e.g., JSON body, form data)


import os # Built-in Python module for interacting with the operating system (used for environment variables)
from datetime import datetime # For handling date/time objects
from decimal import Decimal   # For handling precise decimal numbers (like prices)


# Flask-SQLAlchemy for Object-Relational Mapping (ORM) to interact with databases
from flask_sqlalchemy import SQLAlchemy

# Import your configuration classes from config.py
# This assumes 'config.py' exists in the same directory and defines 'config_by_name'.
from config import config_by_name 


# --------------------------
# Flask App and Database Setup
# --------------------------

# Initialize the Flask application
# __name__ helps Flask locate resources and is used for debugging.
app = Flask(__name__)

'''
# app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///data.db'
# Determine the environment from an environment variable (e.g., FLASK_CONFIG)
# Default to 'development' if FLASK_CONFIG is not set.
'''


# Determine the environment configuration to load.
# It checks the 'FLASK_CONFIG' environment variable.
# If 'FLASK_CONFIG' is not set, it defaults to 'development'.
config_name = os.getenv('FLASK_CONFIG', 'development')


# Load configuration settings from the chosen config object (e.g., DevelopmentConfig or ProductionConfig).
# All uppercase attributes from the selected config class will be applied to app.config.
app.config.from_object(config_by_name[config_name]) # Load config based on environment

# Initialize the SQLAlchemy extension with the Flask app.
# This 'db' object is the bridge between your Python code and the database.
db = SQLAlchemy(app)



# IMPORTANT: Create the database tables if they don't already exist.
# This line is crucial for Flask-SQLAlchemy to translate your 'Drink' model
# into an actual table in your database.
# It needs to be called within the application context.
# If the database file doesn't exist, it will be created.
# If the 'drinks' table doesn't exist within the database, it will be created.


# with app.app_context():
# db.create_all()


# --------------------------
# Database Model Definition
# --------------------------


# Define the 'Drink' database model.
# This class represents the 'drink' table in your database.
# By inheriting from db.Model, SQLAlchemy maps this Python class to a database table.
class Drink(db.Model):

    # FIX: Explicitly set the table name to 'drink' (lowercase)
    # This ensures consistency with the foreign key reference in the Price model.
    __tablename__ = 'drink'


    # 'id': Primary key, unique identifier for each drink.
    # It's an integer and typically auto-increments.
    # IMPORTANT FIX: Added autoincrement=True explicitly for SQL Server compatibility.
    # This ensures the 'id' column is created as an IDENTITY column in SQL Server.
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    
    # 'name': Name of the drink. Must be unique and cannot be empty (nullable=False).
    # String(80) sets a maximum length of 80 characters.
    name = db.Column(db.String(80), unique=True, nullable=False)
    
    # 'description': Optional description of the drink.
    # String(120) sets a maximum length of 120 characters.
    description = db.Column(db.String(120))

    # __repr__ method provides a string representation of a Drink object.
    # This is helpful for debugging and logging, showing object's data clearly.
    def __repr__(self):
        # return f"<Drink {self.name}>"
        return f"Drink(id={self.id}, name='{self.name}', description='{self.description}')"

class Price(db.Model):

    # FIX: Explicitly set the table name to 'drink' (lowercase)
    # This ensures consistency with the foreign key reference in the Price model.
    __tablename__ = 'Price'


    # price_id: Primary Key, Integer, Auto-incrementing
    # INT IDENTITY(1,1) PRIMARY KEY in SQL Server maps to:
    # db.Integer: Python integer type.
    # primary_key=True: Designates this as the primary key.
    # autoincrement=True: Essential for SQL Server's IDENTITY property.
    price_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    

    # drink_id: Foreign Key, Integer, Not Null
    # db.ForeignKey('drink.id'): Establishes the foreign key relationship.
    #   'drink.id' refers to the 'id' column of the 'Drink' model (and its corresponding table name).
    #   This was the crucial fix for the InvalidRequestError.
    drink_id = db.Column(db.Integer, db.ForeignKey('drink.id'), nullable=False)





    # price_amount: Decimal (Numeric), Not Null
    # DECIMAL(10, 2) NOT NULL in SQL Server maps to:
    # db.Numeric(10, 2): Python Decimal type, with 10 total digits and 2 decimal places.
    # nullable=False: Corresponds to NOT NULL in SQL.
    price_amount = db.Column(db.Numeric(10, 2), nullable=False)


    # effective_date: Date, Not Null
    # DATE NOT NULL in SQL Server maps to:
    # db.Date: Python datetime.date object.
    # nullable=False: Corresponds to NOT NULL in SQL.
    effective_date = db.Column(db.Date, nullable=False)

    # end_date: Date, Nullable
    # DATE in SQL Server maps to:
    # db.Date: Python datetime.date object.
    # (nullable=True by default if not specified): Corresponds to NULL in SQL.
    end_date = db.Column(db.Date, nullable=True) # Explicitly setting nullable=True for clarity
    # created_at: DateTime with default value
    # DATETIME DEFAULT GETDATE() in SQL Server maps to:
    # db.DateTime: Python datetime.datetime object.
    # default=db.func.now(): SQLAlchemy's way to use the database's current timestamp function.
    #                        For SQL Server, this will translate to GETDATE() or SYSDATETIME().
    created_at = db.Column(db.DateTime, default=db.func.now())
    # Relationship to the Drink model:
    # This creates a back-reference from Price to Drink.
    # 'drink': This attribute on a Price object will allow you to access the related Drink object.
    # db.backref('prices', lazy=True): Creates a 'prices' attribute on the Drink object.
    #   'prices': On a Drink object, you can access a list of all associated Price objects (e.g., my_drink.prices).
    #   lazy=True: Specifies when SQLAlchemy should load the related objects. lazy=True means they are
    #              loaded "on first access" (when you first try to use my_drink.prices), which is efficient.
    #              Other options include 'joined' (load immediately with the parent) or 'dynamic'.
    drink = db.relationship('Drink', backref=db.backref('prices', lazy=True))


    def __repr__(self):
        return (f"<Price(price_id={self.price_id}, drink_id={self.drink_id}, "
                f"amount={self.price_amount}, effective='{self.effective_date}', "
                f"end='{self.end_date}', created='{self.created_at}')>")




# IMPORTANT: Create the database tables if they don't already exist.
# This block ensures that your SQLAlchemy models (Drink and Price) are translated
# into actual tables in the connected database.
# It must be called within an application context to access app.config.
# Consolidated the db.create_all() call to happen once after all models are defined.
with app.app_context():
    db.create_all()  # This will create the 'price' table in the database if it doesn't exist.




# -------------------------
# Web Routes
# --------------------------

# Define a basic Flask route for the root URL ('/').
# When a user navigates to http://localhost:5001/, this function will be executed.
@app.route('/')
def index():
        """
        Renders a simple greeting for the home page.
        """
        return 'Hello from application.py'


'''
@app.route('/drinks')
def get_drinks():
        return {"drinks": "drink data"}
'''

'''
# This route now retrieves actual data
@app.route('/drinks')
def get_drinks():
    """
    Handles GET requests to /drinks.
    Retrieves all drinks from the database.
    """
    with app.app_context(): # Ensure context for DB query
        drinks = Drink.query.all()
        # Convert list of Drink objects to a list of dictionaries for JSON response
        drinks_list = [{"id": drink.id, "name": drink.name, "description": drink.description} for drink in drinks]
        return jsonify({"drinks": drinks_list}) # Use jsonify for proper JSON response
'''



# This route now retrieves actual data
@app.route('/drinks')
def get_drinks():
    """
    Handles GET requests to /drinks.
    Retrieves all drinks from the database.
    """
    drinks = Drink.query.all()

    output = []
    for drink in drinks:
        drink_data = {'name': drink.name, 'description': drink.description}
        
        output.append(drink_data)
    
    return {"drinks": output}

@app.route('/drinks/<id>')
def get_drink(id):
        """
        Handles GET requests to /drinks/<id>.
        Retrieves a single drink record by its ID and returns it as JSON.
        Returns a 404 Not Found error if the drink does not exist.
        """
        drink = Drink.query.get_or_404(id)
        return jsonify({"name": drink.name, "description":drink.description})



# Route to add a new drink to the database.
# Handles HTTP POST requests to /drinks.
@app.route('/drinks', methods=['POST'])
def add_drink():
     """
     Handles POST requests to /drinks.
     Adds a new drink record to the database.
     Expects a JSON request body containing 'name' and 'description'.
     Returns the newly created drink's ID and data with a 201 Created status on success.
     Handles errors for missing data, duplicate names, and other database issues.
     """
     

     drink = Drink(name=request.json['name'], description=request.json['description'])
     db.session.add(drink)
     db.session.commit()

     # Return the found drink's data as a JSON object.
     return {'id': drink.id}



# New route to add a price record
@app.route('/prices', methods=['POST'])
def add_price():
    """
    Handles POST requests to /prices.
    Adds a new price record to the database.
    Expects a JSON body with 'drink_id', 'price_amount', 'effective_date',
    and optionally 'end_date'.
    """
    if not request.json:
        return jsonify({"message": "Request must be JSON"}), 400

    required_fields = ['drink_id', 'price_amount', 'effective_date']
    for field in required_fields:
        if field not in request.json:
            return jsonify({"message": f"Missing required field: '{field}'"}), 400

    try:
        drink_id = request.json['drink_id']
        price_amount = request.json['price_amount']
        effective_date_str = request.json['effective_date']
        end_date_str = request.json.get('end_date') # Optional field

        # Convert price_amount to Decimal for precise financial calculations
        price_amount = Decimal(str(price_amount))

        # Convert date strings (e.g., 'YYYY-MM-DD') to Python date objects
        effective_date = datetime.strptime(effective_date_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date() if end_date_str else None

    except ValueError as ve:
        # Catch errors if date strings are in the wrong format or price_amount is not convertible
        return jsonify({"message": f"Invalid data type or format in request: {str(ve)}"}), 400
    except Exception as e:
        # Catch any other unexpected errors during request parsing
        return jsonify({"message": f"Error parsing request data: {str(e)}"}), 400

    with app.app_context(): # Ensure database operations are within an application context
        try:
            # Validate foreign key: Check if the referenced drink_id actually exists in the Drink table
            if not Drink.query.get(drink_id):
                return jsonify({"message": f"Drink with ID {drink_id} not found. Cannot add price."}), 404

            # Create a new Price object with the parsed data
            price = Price(
                drink_id=drink_id,
                price_amount=price_amount,
                effective_date=effective_date,
                end_date=end_date
            )
            db.session.add(price)    # Add the new price object to the database session
            db.session.commit()      # Commit the transaction to save the new price to the database

            # Return the newly created price's details with a 201 Created status
            # Convert Decimal and date objects back to string for JSON serialization
            return jsonify({
                'price_id': price.price_id,
                'drink_id': price.drink_id,
                'price_amount': str(price.price_amount), # Convert Decimal to string for JSON output
                'effective_date': price.effective_date.isoformat(), # Convert date to ISO format string
                'end_date': price.end_date.isoformat() if price.end_date else None, # Handle optional end_date
                'created_at': price.created_at.isoformat() # Convert datetime to ISO format string
            }), 201

        except Exception as e:
            db.session.rollback() # Rollback the session on any error to prevent partial commits
            # Check for specific database integrity errors (e.g., if a foreign key constraint was violated
            # in a way not caught by the initial Drink.query.get check, or other DB constraints)
            if "IntegrityError" in str(type(e)):
                 return jsonify({"message": f"Database integrity error: {str(e)}. Check foreign keys or constraints."}), 400
            return jsonify({"message": f"An unexpected error occurred while adding price: {str(e)}"}), 500








# --------------------------
# Application Entry Point
# --------------------------

# This standard Python idiom ensures that the Flask development server runs only
# when this script is executed directly (e.g., `python application.py`),
# and not when it's imported as a module into another script.
if __name__ == '__main__':
    # explicitly set the port when running this
    # Run the Flask application in debug mode.
    # debug=True:
    # - Enables an interactive debugger in the browser on error.
    # - Auto-reloads the server when code changes are detected.
    # IMPORTANT: Never use debug=True in a production environment due to security risks.
    # We'll set it to run on port 5001 so it doesn't conflict with api.py (which uses 5000).

    # Run the Flask application.
    # debug=app.config['DEBUG']: Sets debug mode based on the 'DEBUG' setting
    #                            loaded from your 'config.py' (True for development, False for production).
    # port=5001: Specifies the port on which the Flask server will listen.
    # IMPORTANT: Never run with debug=True in a production deployment due to security risks.
    app.run(debug=True, port=5001)
    