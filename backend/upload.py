import os
import time
import functools
from flask import (
        Blueprint, flash, request, render_template, abort, jsonify, url_for, current_app
        )
from urllib.parse import unquote
from backend.db import get_db

bp = Blueprint('upload', __name__)

@bp.route('/upload', methods=('GET', 'POST'))
def upload():
    if request.method == 'POST':
        print("receive POST request")
        upload_file = request.files['upload-file']
        filename = upload_file.filename
        print("filename is %s" % filename)
        if filename != '':
            db = get_db()
            filename = unquote(filename)
            current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            if db.execute('SELECT id FROM files WHERE filename = ?', (filename,)).fetchone() is None:
                if '.' in filename:
                    current_type = filename.rsplit('.', 1)[1].lower()
                    if current_type in ['doc', 'docx']:
                        current_type = 'word'
                    elif current_type == 'pdf':
                        current_type = 'pdf'
                    elif current_type in ['xls', 'xlsx']:
                        current_type = 'excel'
                    elif current_type in ['jpg', 'jpeg', 'png', 'bmp']:
                        current_type = 'picture'
                    else:
                        current_type = 'others'
                db.execute(
                        'INSERT INTO files (uploaded, filename, filetype) VALUES (?, ?, ?)',
                        (current_time, filename, current_type))
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
