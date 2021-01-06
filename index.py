from flask import Flask, render_template, redirect, url_for, request, session
from werkzeug.utils import secure_filename
import os
import glob

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key-goes-here'
app.config['UPLOAD_FOLDER'] = './admin'


@app.before_request
def before_request():
    if (not 'logged_in' in session) and (request.endpoint != 'login'):
        return redirect(url_for('login'))
    else:
        pass


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'logged_in' in session:
        return redirect(url_for('upload_page'))
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            session['logged_in'] = True
            return redirect(url_for('upload_page'))
    return render_template('login.html', error=error)


@app.route('/logout', methods=['GET'])
def logout():
    if 'logged_in' in session:
        session.pop('logged_in', None)
        return redirect(url_for('login'))


@app.route('/upload')
def upload_page():
	photo_list = glob.glob(os.path.join(app.config['UPLOAD_FOLDER']+'/*'))
	return render_template('upload.html', photo_list=photo_list)


@ app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        filename = secure_filename(f.filename)
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect(url_for('upload_page'))


if __name__ == '__main__':
    app.run('0.0.0.0', debug=True, port=5000)
