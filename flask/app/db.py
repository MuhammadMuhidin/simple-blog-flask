# db.py
from flask_sqlalchemy import SQLAlchemy
import click

db = SQLAlchemy()

@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    from models import db
    db.drop_all()
    db.create_all()
    click.echo('Initialized the database.')

def init_app(app):
    db.init_app(app)
    app.cli.add_command(init_db_command)
