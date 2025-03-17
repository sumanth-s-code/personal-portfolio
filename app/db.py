"""
Database module for the Personal Portfolio app.

Provides functions to connect to the SQLite database, initialize tables,
and close the connection.
"""

import sqlite3
import click
from flask import current_app, g


def get_db():
    """
    Get a database connection for the current application context.

    Returns:
        sqlite3.Connection: The database connection.
    """
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        # Return rows as dictionaries
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    """
    Close the database connection if it exists.

    Args:
        e (Exception, optional): Error, if any.
    """
    db = g.pop('db', None)
    if db is not None:
        db.close()


def init_db():
    """
    Initialize the database by creating the 'projects' and 'blog_posts' tables.
    """
    db = get_db()
    db.executescript("""
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            link TEXT,
            created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE TABLE IF NOT EXISTS blog_posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    db.commit()

def init_app(app):
    """
    Register database functions with the Flask app.

    Args:
        app (Flask): The Flask application instance.
    """
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

@click.command('init-db')
def init_db_command():
    """
    Command to initialize the database.

    Run with: flask init-db
    """
    init_db()
    click.echo('Initialized the database.')

