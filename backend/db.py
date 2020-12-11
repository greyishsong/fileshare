import os
import sqlite3
import click
from flask import current_app, g
from flask.cli import with_appcontext
from hashlib import sha256
from base64 import b64encode


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
    # delete all files uploaded
    # the only folder is the KEY_FOLDER and it should be remained
    flist = os.listdir(current_app.config['UPLOAD_FOLDER'])
    for fname in flist:
        if not os.path.isdir(os.path.join(current_app.config['UPLOAD_FOLDER'], fname)):
            os.remove(os.path.join(current_app.config['UPLOAD_FOLDER'], fname))

    db = get_db()

    with current_app.open_resource('schema.sql') as schema:
        db.executescript(schema.read().decode('utf8'))

    flist = os.listdir(current_app.config['KEY_FOLDER'])
    for fname in flist:
        with open(os.path.join(current_app.config['KEY_FOLDER'], fname)) as f:
            content = f.read()
            tmp = sha256(content.encode('utf-8')).digest()
            value = b64encode(tmp).decode('ascii')
            if db.execute('SELECT id FROM users WHERE keyfile = value').fetchone() is None:
                db.execute(
                        'INSERT INTO users (keyfile, macaddr) VALUES (?, ?)', (value, None)
                        )
    db.commit()

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
