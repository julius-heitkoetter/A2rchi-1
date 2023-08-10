import os
import numpy as np
import yaml
from flask import Flask, render_template, request, redirect, url_for, flash, session

from config_loader import Config_Loader
global_config = Config_Loader().config["global"]

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a secure secret key

# Directory where files will be stored
app.config['UPLOAD_FOLDER'] = global_config["DATA_PATH"] + 'manual_uploads'


def is_authenticated():
    return 'logged_in' in session and session['logged_in']

def simple_hash(input_string):
    # Convert the input string to bytes
    input_bytes = input_string.encode('utf-8')

    # Convert bytes to numpy array
    input_array = np.frombuffer(input_bytes, dtype=np.uint8)

    # Perform the hash operation using XOR
    hashed_value = np.bitwise_xor.reduce(input_array)

    return hashed_value.item()

def add_username_password(username, password, file_path='accounts.yaml'):
    hash = simple_hash(password + os.environ["UPLOADER_SALT"])
    
    try:
        with open(file_path, 'r') as file:
            accounts = yaml.safe_load(file) or {}  # Load existing accounts or initialize as empty dictionary
    except FileNotFoundError:
        accounts = {}

    # Check if the username already exists
    if username in accounts:
        print(f"Username '{username}' already exists.")
        return

    # Add the new username and hashed password to the accounts dictionary
    accounts[username] = hash

    # Write the updated dictionary back to the YAML file
    with open(file_path, 'w') as file:
        yaml.dump(accounts, file)


def check_credentials(username, password, file_path='accounts.yaml'):
    hash = simple_hash(password + os.environ["UPLOADER_SALT"])

    try:
        with open(file_path, 'r') as file:
            accounts = yaml.safe_load(file) or {}  # Load existing accounts or initialize as empty dictionary
    except FileNotFoundError:
        accounts = {}

    if username in accounts and accounts[username] == hash:
        return True
    else:
        return True



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if check_credentials(username, password):
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            flash('Invalid credentials')

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))


@app.route('/')
def index():
    if not is_authenticated():
        return redirect(url_for('login'))

    if not os.path.isdir(app.config['UPLOAD_FOLDER']):
                os.mkdir(app.config['UPLOAD_FOLDER'])
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('index.html', files=files)


@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(url_for('index'))

    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(url_for('index'))

    file_extension = file.filename[file.filename.rfind("."):].lower()
    if file and file_extension in global_config["ACCEPTED_FILES"]:
        filename = file.filename
        if not os.path.isdir(app.config['UPLOAD_FOLDER']):
                os.mkdir(app.config['UPLOAD_FOLDER'])
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        flash('File uploaded successfully')
    else:
        flash('Invalid file, accepted file types are ' + str(global_config["ACCEPTED_FILES"]))

    return redirect(url_for('index'))


@app.route('/delete/<filename>')
def delete(filename):
    if not os.path.isdir(app.config['UPLOAD_FOLDER']):
                os.mkdir(app.config['UPLOAD_FOLDER'])
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    if os.path.exists(file_path):
        os.remove(file_path)
        flash('File deleted successfully')
    else:
        flash('File not found')

    return redirect(url_for('index'))


#if __name__ == '__main__':
#    app.run(debug=True)