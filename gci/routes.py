import base64
import os
import cv2
import shutil
from flask import Blueprint, flash, redirect, render_template, request, send_from_directory, current_app
from .db import get_db

bp = Blueprint('routes', __name__)

@bp.route('/')
def home():
    media = get_db().execute('SELECT * FROM media').fetchall()
    return render_template('home.html', media=media)

@bp.route('/camera', methods=['GET', 'POST'])
def camera():
    if request.method == 'GET':
        return render_template('camera.html')
    
    name = request.form.get('name')
    video_data = request.form['video_data']

    try:
        if 'base64,' in video_data:
            video_data = video_data.split('base64,')[1]
        video_binary = base64.b64decode(video_data)

        x = 0
        while True:
            dirname = f"face_{name}_{x}"
            dir_path = os.path.join(current_app.config['UPLOAD_FOLDER'], dirname)
            if not os.path.exists(dir_path): break
            x += 1
            
        # Create directory and save video file
        os.makedirs(dir_path)
        video_file = os.path.join(dir_path, "video.mp4")
        with open(video_file, 'wb') as f:
            f.write(video_binary)

        db = get_db()
        db.execute('INSERT INTO media (name, filename) VALUES (?, ?)',
                   (name, dirname))
        db.commit()
        
        flash('Video saved successfully!')
        return redirect('/')

    except db.IntegrityError:
        flash(f'Directory {dirname} already exists.')
    except Exception as e:
        flash(f'Error processing video: {str(e)}')
    
    return redirect('/')

@bp.route('/media/<filename>')
def media(filename):
    # Return the video file directly
    video_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename, 'video.mp4')
    return send_from_directory(os.path.dirname(video_path), os.path.basename(video_path))

@bp.route('/delete/<filename>', methods=['POST'])
def delete(filename):
    try:
        # Delete directory
        dir_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        if os.path.exists(dir_path):
            shutil.rmtree(dir_path)
        
        # Delete database entry
        db = get_db()
        db.execute('DELETE FROM media WHERE filename = ?', (filename,))
        db.commit()
        
        flash('Video deleted successfully!')
    except Exception as e:
        flash(f'Error deleting video: {str(e)}')
    
    return redirect('/')