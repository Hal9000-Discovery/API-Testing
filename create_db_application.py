"""
This module creates the database for api.py REST API

Author: David Sanghara
Date : June 25, 2025
Version: 1.0.0
"""

from application import app, db

# This block ensures that we are operating within the Flask application context.
# This context is necessary for SQLAlchemy operations like `db.create_all()`
# to function correctly, as they rely on the Flask application's configuration
# and database bindings.
with app.app_context():
    # This line creates all database tables defined by the SQLAlchemy models
    # (e.g., UserModel) if they do not already exist in the 'database.db' file.
    # It's typically used for initial database setup or schema updates during development.

    db.create_all()
