"""Create the SQLite database ecommerce.db and seed the product catalog.

The app creates the tables on start, so this script is optional.
It is useful to prepare the database before the first run.
Account rows are not seeded, so the repository holds no account password.
"""
from database import init_db

if __name__ == '__main__':
    init_db()
    print('ecommerce.db is ready')
