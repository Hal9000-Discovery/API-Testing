# add_drinks.py

from application import app, db, Drink # Import app, db, and your Drink model from application.py
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

def add_new_drink(name, description):
    """Adds a new drink to the database."""
    # All database operations must be done within the Flask application context
    with app.app_context():
        try:
            # 1. Create an instance of the Drink model
            new_drink = Drink(name=name, description=description)

            # 2. Add the new drink object to the database session
            db.session.add(new_drink)

            # 3. Commit the session to save the changes to the database
            db.session.commit()
            print(f"Successfully added drink: {new_drink.name}")
            return new_drink
        except IntegrityError:
            # This catches cases where 'name' is not unique (due to unique=True constraint)
            db.session.rollback() # Important: rollback the session on error
            print(f"Error: Drink '{name}' already exists (name must be unique).")
            return None
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"An SQLAlchemy error occurred: {e}")
            return None
        except Exception as e:
            db.session.rollback()
            print(f"An unexpected error occurred: {e}")
            return None

if __name__ == '__main__':
    print("--- Adding Drinks to the Database ---")

    # Add some example drinks
    add_new_drink("Coff", "A hot beverage made from roasted coffee beans.")
    add_new_drink("Te", "An aromatic beverage prepared by pouring hot or boiling water over cured or fresh leaves of Camellia sinensis.")
    add_new_drink("Orange", "A sweet and tangy citrus juice.")

    # Try adding a duplicate name to see error handling
    add_new_drink("Coffee", "A different kind of coffee.") # This should trigger an error

    print("\nFinished adding drinks.")