import os
import time
import functools
from flask import (
        Blueprint, current_app, send_from_directory, jsonify, render_template, redirect, url_for
        )
from urllib.parse import unquote
from backend.db import get_db

bp = Blueprint('download', __name__)

@bp.route('/download')
def download_page():
    return render_template('index.html')

@bp.route('/')
def main_page_redirect():
    return redirect(url_for('download.download_page'))

@bp.route('/download/<filename>')
def download(filename):
    filename = unquote(str(filename))
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)

@bp.route('/filelist')
def filelist():
    flist = list()
    db = get_db()
    files = db.execute('SELECT filename, filetype FROM files').fetchall()
    for f in files:
        fitem = dict()
        fitem['filename'] = f[0]
        fitem['type'] = f[1]
        flist.append(fitem)

    return jsonify(flist)
