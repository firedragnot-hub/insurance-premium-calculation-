from flask import Flask, render_template, request, jsonify, redirect, url_for, session, g, flash
from werkzeug.security import generate_password_hash, check_password_hash
import joblib
import pandas as pd
import os
import sqlite3
from functools import wraps

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'premium_estimator_secret_key_129847')

DATABASE = os.path.join(os.path.dirname(__file__), 'database.db')

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        # Create users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        # Create profiles table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS profiles (
                user_id INTEGER PRIMARY KEY,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                age INTEGER,
                sex TEXT,
                bmi REAL,
                children INTEGER,
                smoker TEXT,
                region TEXT,
                FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        ''')
        db.commit()

# Initialize database
init_db()

# Load estimator model if it exists
MODEL_PATH = 'insurance_model.joblib'
try:
    model = joblib.load(MODEL_PATH)
except FileNotFoundError:
    model = None
    print(f"Warning: {MODEL_PATH} not found. Predictions will be mocked.")

# Decorator to secure routes
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
@login_required
def index():
    db = get_db()
    profile = db.execute('SELECT * FROM profiles WHERE user_id = ?', (session['user_id'],)).fetchone()
    if not profile:
        return redirect(url_for('create_profile'))
    return render_template('index.html', profile=profile, username=session['username'])

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if 'user_id' in session:
        return redirect(url_for('index'))
        
    error = None
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        if not username or not email or not password:
            error = 'All fields are required.'
        elif password != confirm_password:
            error = 'Passwords do not match.'
        else:
            db = get_db()
            # Check if user exists
            existing_user = db.execute(
                'SELECT id FROM users WHERE username = ? OR email = ?',
                (username, email)
            ).fetchone()
            
            if existing_user:
                error = 'Username or email already exists.'
            else:
                try:
                    hashed_pw = generate_password_hash(password)
                    cursor = db.cursor()
                    cursor.execute(
                        'INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)',
                        (username, email, hashed_pw)
                    )
                    db.commit()
                    user_id = cursor.lastrowid
                    
                    # Store session details
                    session['user_id'] = user_id
                    session['username'] = username
                    
                    return redirect(url_for('create_profile'))
                except Exception as e:
                    error = f'Database error: {str(e)}'
                    
    return render_template('signup.html', error=error)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('index'))
        
    error = None
    if request.method == 'POST':
        login_input = request.form.get('login_input', '').strip()
        password = request.form.get('password', '')
        
        if not login_input or not password:
            error = 'Please enter username/email and password.'
        else:
            db = get_db()
            user = db.execute(
                'SELECT * FROM users WHERE username = ? OR email = ?',
                (login_input, login_input)
            ).fetchone()
            
            if user and check_password_hash(user['password_hash'], password):
                session['user_id'] = user['id']
                session['username'] = user['username']
                return redirect(url_for('index'))
            else:
                error = 'Invalid username/email or password.'
                
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/create-profile', methods=['GET', 'POST'])
@login_required
def create_profile():
    db = get_db()
    error = None
    
    # Check if a profile already exists
    profile = db.execute('SELECT * FROM profiles WHERE user_id = ?', (session['user_id'],)).fetchone()
    
    if request.method == 'POST':
        first_name = request.form.get('first_name', '').strip()
        last_name = request.form.get('last_name', '').strip()
        
        try:
            age = int(request.form.get('age', 0))
            sex = request.form.get('sex', '')
            bmi = float(request.form.get('bmi', 0.0))
            children = int(request.form.get('children', 0))
            smoker = request.form.get('smoker', '')
            region = request.form.get('region', '')
            
            if not first_name or not last_name or not sex or not smoker or not region:
                error = 'Please fill out all fields.'
            else:
                cursor = db.cursor()
                if profile:
                    cursor.execute('''
                        UPDATE profiles 
                        SET first_name = ?, last_name = ?, age = ?, sex = ?, bmi = ?, children = ?, smoker = ?, region = ?
                        WHERE user_id = ?
                    ''', (first_name, last_name, age, sex, bmi, children, smoker, region, session['user_id']))
                else:
                    cursor.execute('''
                        INSERT INTO profiles (user_id, first_name, last_name, age, sex, bmi, children, smoker, region)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (session['user_id'], first_name, last_name, age, sex, bmi, children, smoker, region))
                db.commit()
                return redirect(url_for('index'))
        except ValueError:
            error = 'Please enter valid numerical values for age, BMI, and children.'
        except Exception as e:
            error = f'Error saving profile: {str(e)}'
            
    return render_template('create_profile.html', profile=profile, error=error, username=session['username'])

@app.route('/predict', methods=['POST'])
@login_required
def predict():
    try:
        data = request.json
        age = int(data.get('age', 0))
        sex = data.get('sex', '')
        bmi = float(data.get('bmi', 0.0))
        children = int(data.get('children', 0))
        smoker = data.get('smoker', '')
        region = data.get('region', '')

        if model:
            input_data = {
                'age': age,
                'sex': sex,
                'bmi': bmi,
                'children': children,
                'smoker': smoker,
                'region': region
            }
            input_df = pd.DataFrame([input_data])
            prediction = model.predict(input_df)[0]
        else:
            base = 1000
            if smoker == 'yes':
                base += 15000
            base += age * 50
            base += bmi * 100
            prediction = base

        return jsonify({'success': True, 'prediction': float(prediction)})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
