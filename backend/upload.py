import os
import time
import functools
from flask import (
        Blueprint, request, abort, jsonify, url_for, current_app
        )
from urllib.parse import unquote
from backend.db import get_db

bp = Blueprint('upload', __name__)

# Provide authorization through a unique keyfile for every user and MAC address
# Originally no MAC address is related to a keyfile, once the first request
# with it comes, the MAC address of in the request will be related with it, and
# the keyfile is bounded with this MAC address permanently.
# The route '/upload' only receive POST request for uploading files, any GET
# request will be rejected with a '403 Forbidden'.
@bp.route('/upload', methods=('GET', 'POST'))
def upload():
    if request.method == 'POST':
        print("receive POST request")
        db = get_db()
        keyfile = request.form['keyfile']
        macaddr = request.form['macaddr']
        checkinfo = db.execute(
                'SELECT id, keyfile, macaddr FROM users WHERE keyfile = ?',
                (keyfile,)).fetchone()
        # Check the SHA256 values of keyfile and MAC address sended from client.
        # Only allow requests with a keyfile restored in database.
        # If the keyfile is legal but the MAC address is NULL in database, set
        # the MAC address as the uploaded value.
        # If the MAC address is not NULL in database, compare it with the
        # uploaded infomation.
        if checkinfo is None:
            abort(403)
        elif checkinfo['macaddr'] is None:
            db.execute(
                    'UPDATE users SET macaddr = ? WHERE id = ?',
                    (macaddr, checkinfo['id']))
            db.commit()
        elif macaddr != checkinfo['macaddr']:
            abort(403)
        else:
            pass
        upload_file = request.files['upload-file']
        filename = upload_file.filename
        current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        print("filename is %s" % filename)
        if filename != '':
            filename = unquote(filename)
            if db.execute('SELECT id FROM files WHERE filename = ?', (filename,)).fetchone() is None:
                current_type = get_type(filename)
                db.execute(
                        'INSERT INTO files (uploaded, userid, filename, filetype) VALUES (?, ?, ?)',
                        (current_time, checkinfo['id'], filename, current_type))
            else:
                db.execute(
                        'UPDATE files SET uploaded = ? WHERE filename = ?',
                        (current_time, filename))
            db.commit()
            upload_file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            result = { 'status': 'success' }
        else:
            result = { 'status': 'failed', 'message': 'empty filename'}
        return jsonify(result)
    else:
        abort(403)

# Get the type of uploaded file by its suffix
def get_type(filename):
    if '.' in filename:
        res = filename.rsplit('.', 1)[1].lower()
        if res in ['doc', 'docx']:
            res = 'word'
        elif res == 'pdf':
            res = 'pdf'
        elif res in ['xls', 'xlsx']:
            res = 'excel'
        elif res in ['jpg', 'jpeg', 'png', 'bmp']:
            res = 'picture'
        else:
            res = 'others'
    else:
        res = 'others'
    return res
