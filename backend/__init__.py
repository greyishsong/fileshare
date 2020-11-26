import os
from flask import Flask


def create_app(test_config=None):
    app = Flask(__name__)
    
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)
    app.config['DATABASE'] = os.path.join(app.instance_path, 'fileshare.db')

    try:
        os.makedirs(app.instance_path)
    except:
        pass

    from . import db
    db.init_app(app)

    from . import upload
    app.register_blueprint(upload.bp)

    from . import download
    app.register_blueprint(download.bp)

    return app
