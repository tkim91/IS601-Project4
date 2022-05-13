import click
import os
from flask.cli import with_appcontext
from app.db import db


@click.command(name='create-db')
@with_appcontext
def create_database():
    root = os.path.dirname(os.path.abspath(__file__))
    # set the name of the apps log folder to logs
    dbdir = os.path.join(root, '../../database')
    # make a directory if it doesn't exist
    if not os.path.exists(dbdir):
        os.mkdir(dbdir)
    db.create_all()