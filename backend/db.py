import os
import sqlite3
import click
from flask import current_app, g
from flask.cli import with_appcontext


# basic database operations
# get the handler of database, creating one if it does not exist
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
                current_app.config['DATABASE'],
                detect_types=sqlite3.PARSE_DECLTYPES
                )
        g.db.row_factory = sqlite3.Row

    return g.db

# close the connection to database
def close_db(e = None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

# initialize a database
def init_db():
    # backup the old database file
    # by renaming it to format 'fileshare-yy-mm-dd.db'
    #if 'fileshare.db' in os.listdir(current_app.instance_path):
    #    instpath = current_app.instance_path
    #    cur_date = datetime.datetime.now().strftime('%Y-%m-%d')
    #    os.rename(os.path.join(instpath, 'fileshare.db'), os.path.join(instpath, 'fileshare'+cur_date+'.db'))

    db = get_db()

    with current_app.open_resource('schema.sql') as schema:
        db.executescript(schema.read().decode('utf8'))

    # create a new log file
    #log_file = open(current_app.config['LOG_FILE'], 'w')
    #log_file.close()

# regist 'init_db' as a command
@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo('The database is initialized.')

# regist close_db and init_db_command into the application instance.
# should be called in 'create_app'
def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
