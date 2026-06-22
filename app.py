import os
import joblib
import pandas as pd
import datetime
import uuid
import json
import sqlite3
import contextlib
from functools import wraps
from flask import Flask, render_template, request, jsonify, redirect, url_for, session, g, flash
from werkzeug.security import generate_password_hash, check_password_hash

# MongoDB and BSON
import pymongo
from bson import ObjectId

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'premium_estimator_secret_key_129847')

MODEL_PATH = 'insurance_model.joblib'
DATA_PATH = 'insurance.csv'
SQLITE_DB_PATH = os.path.join(os.path.dirname(__file__), 'database.db')
MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017/")


# ==============================================================================
# Unified Database Manager: MongoDB with SQLite local fallback
# ==============================================================================
class DBManager:
    def __init__(self, sqlite_path, mongo_uri="mongodb://localhost:27017/"):
        self.sqlite_path = sqlite_path
        self.mongo_uri = mongo_uri
        self.mongo_client = None
        self.mongo_db = None
        self.mongo_online = False
        
        self.init_sqlite()
        self.check_mongo_connection()
        
    @contextlib.contextmanager
    def sqlite_conn(self):
        conn = sqlite3.connect(self.sqlite_path, timeout=30.0)
        try:
            conn.execute("PRAGMA journal_mode=WAL;")
            yield conn
        finally:
            conn.close()

    def init_sqlite(self):
        with self.sqlite_conn() as conn:
            c = conn.cursor()
            c.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id TEXT PRIMARY KEY,
                    username TEXT UNIQUE NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    is_admin INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            # Backwards compatibility migration for existing database.db files
            try:
                c.execute("ALTER TABLE users ADD COLUMN is_admin INTEGER DEFAULT 0")
                conn.commit()
            except sqlite3.OperationalError:
                pass
            c.execute('''
                CREATE TABLE IF NOT EXISTS profiles (
                    user_id TEXT PRIMARY KEY,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    age INTEGER,
                    sex TEXT,
                    bmi REAL,
                    children INTEGER,
                    smoker TEXT,
                    region TEXT
                )
            ''')
            c.execute('''
                CREATE TABLE IF NOT EXISTS quotes (
                    id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    age INTEGER,
                    sex TEXT,
                    bmi REAL,
                    children INTEGER,
                    smoker TEXT,
                    region TEXT,
                    charges REAL,
                    timestamp TEXT
                )
            ''')
            conn.commit()

    def check_mongo_connection(self):
        try:
            self.mongo_client = pymongo.MongoClient(self.mongo_uri, serverSelectionTimeoutMS=2000)
            self.mongo_client.server_info()  # Forces check
            self.mongo_db = self.mongo_client["insurance_db"]
            self.mongo_online = True
            print("Successfully connected to MongoDB!")
        except Exception as e:
            self.mongo_online = False
            self.mongo_client = None
            self.mongo_db = None
            print(f"MongoDB connection failed: {e}. Falling back to SQLite.")

    def create_user(self, username, email, password_hash, is_admin=0):
        user_id = str(uuid.uuid4())
        if self.mongo_online and self.mongo_db is not None:
            try:
                self.mongo_db.users.insert_one({
                    "_id": user_id,
                    "username": username,
                    "email": email,
                    "password_hash": password_hash,
                    "is_admin": bool(is_admin),
                    "created_at": datetime.datetime.utcnow().isoformat()
                })
                return user_id
            except pymongo.errors.DuplicateKeyError:
                return None
            except Exception:
                pass
        
        # SQLite Fallback
        try:
            with self.sqlite_conn() as conn:
                c = conn.cursor()
                c.execute(
                    "INSERT INTO users (id, username, email, password_hash, is_admin) VALUES (?, ?, ?, ?, ?)",
                    (user_id, username, email, password_hash, is_admin)
                )
                conn.commit()
                return user_id
        except sqlite3.IntegrityError:
            return None

    def get_user_by_email_or_username(self, login_input):
        if self.mongo_online and self.mongo_db is not None:
            try:
                user = self.mongo_db.users.find_one({
                    "$or": [
                        {"username": login_input},
                        {"email": login_input}
                    ]
                })
                if user:
                    user['id'] = user['_id']
                    return user
            except Exception:
                pass
                
        # SQLite Fallback
        with self.sqlite_conn() as conn:
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            user = c.execute(
                "SELECT * FROM users WHERE username = ? OR email = ?",
                (login_input, login_input)
            ).fetchone()
            if user:
                return dict(user)
        return None

    def get_profile(self, user_id):
        if self.mongo_online and self.mongo_db is not None:
            try:
                prof = self.mongo_db.profiles.find_one({"_id": user_id})
                if prof:
                    prof['user_id'] = prof['_id']
                    return prof
            except Exception:
                pass
                
        # SQLite Fallback
        with self.sqlite_conn() as conn:
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            prof = c.execute("SELECT * FROM profiles WHERE user_id = ?", (user_id,)).fetchone()
            if prof:
                return dict(prof)
        return None

    def save_profile(self, user_id, profile_data):
        if self.mongo_online and self.mongo_db is not None:
            try:
                self.mongo_db.profiles.update_one(
                    {"_id": user_id},
                    {"$set": {
                        "first_name": profile_data["first_name"],
                        "last_name": profile_data["last_name"],
                        "age": int(profile_data["age"]),
                        "sex": profile_data["sex"],
                        "bmi": float(profile_data["bmi"]),
                        "children": int(profile_data["children"]),
                        "smoker": profile_data["smoker"],
                        "region": profile_data["region"]
                    }},
                    upsert=True
                )
                return True
            except Exception:
                pass
                
        # SQLite Fallback
        with self.sqlite_conn() as conn:
            c = conn.cursor()
            c.execute("""
                INSERT OR REPLACE INTO profiles (user_id, first_name, last_name, age, sex, bmi, children, smoker, region)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (user_id, profile_data["first_name"], profile_data["last_name"], int(profile_data["age"]), 
                  profile_data["sex"], float(profile_data["bmi"]), int(profile_data["children"]), 
                  profile_data["smoker"], profile_data["region"]))
            conn.commit()
        return True

    def save_quote(self, user_id, quote_data):
        quote_id = str(uuid.uuid4())
        doc = {
            "user_id": user_id,
            "age": int(quote_data['age']),
            "sex": str(quote_data['sex']),
            "bmi": float(quote_data['bmi']),
            "children": int(quote_data['children']),
            "smoker": str(quote_data['smoker']),
            "region": str(quote_data['region']),
            "charges": float(quote_data['charges']),
            "timestamp": datetime.datetime.utcnow().isoformat()
        }
        
        if self.mongo_online and self.mongo_db is not None:
            try:
                doc_to_save = doc.copy()
                doc_to_save["_id"] = quote_id
                self.mongo_db.quotes.insert_one(doc_to_save)
                doc["id"] = quote_id
                return doc
            except Exception:
                pass
                
        # SQLite Fallback
        with self.sqlite_conn() as conn:
            c = conn.cursor()
            c.execute("""
                INSERT INTO quotes (id, user_id, age, sex, bmi, children, smoker, region, charges, timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (quote_id, user_id, doc["age"], doc["sex"], doc["bmi"], doc["children"], 
                  doc["smoker"], doc["region"], doc["charges"], doc["timestamp"]))
            conn.commit()
        doc["id"] = quote_id
        return doc

    def get_quotes_history(self, user_id, smoker_filter=None, region_filter=None):
        if self.mongo_online and self.mongo_db is not None:
            try:
                query = {"user_id": user_id}
                if smoker_filter:
                    query["smoker"] = smoker_filter
                if region_filter:
                    query["region"] = region_filter
                    
                results = list(self.mongo_db.quotes.find(query).sort("timestamp", -1))
                for doc in results:
                    doc["id"] = str(doc["_id"])
                    del doc["_id"]
                return results
            except Exception:
                pass
                
        # SQLite Fallback
        with self.sqlite_conn() as conn:
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            q = "SELECT * FROM quotes WHERE user_id = ?"
            params = [user_id]
            if smoker_filter:
                q += " AND smoker = ?"
                params.append(smoker_filter)
            if region_filter:
                q += " AND region = ?"
                params.append(region_filter)
            q += " ORDER BY timestamp DESC"
            
            rows = c.execute(q, params).fetchall()
            return [dict(r) for r in rows]

    def delete_quote(self, user_id, quote_id):
        if self.mongo_online and self.mongo_db is not None:
            try:
                res = self.mongo_db.quotes.delete_one({"_id": quote_id, "user_id": user_id})
                return res.deleted_count > 0
            except Exception:
                pass
                
        # SQLite Fallback
        with self.sqlite_conn() as conn:
            c = conn.cursor()
            c.execute("DELETE FROM quotes WHERE id = ? AND user_id = ?", (quote_id, user_id))
            count = c.rowcount
            conn.commit()
        return count > 0

    def get_all_users(self):
        if self.mongo_online and self.mongo_db is not None:
            try:
                users = list(self.mongo_db.users.find())
                for u in users:
                    u['id'] = u['_id']
                return users
            except Exception:
                pass
        # SQLite Fallback
        with self.sqlite_conn() as conn:
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            users = c.execute("SELECT * FROM users").fetchall()
            return [dict(u) for u in users]

    def get_all_profiles(self):
        if self.mongo_online and self.mongo_db is not None:
            try:
                profiles = list(self.mongo_db.profiles.find())
                for p in profiles:
                    p['user_id'] = p['_id']
                return profiles
            except Exception:
                pass
        # SQLite Fallback
        with self.sqlite_conn() as conn:
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            profiles = c.execute("SELECT * FROM profiles").fetchall()
            return [dict(p) for p in profiles]

    def get_all_quotes(self):
        if self.mongo_online and self.mongo_db is not None:
            try:
                quotes = list(self.mongo_db.quotes.find())
                for q in quotes:
                    q['id'] = str(q['_id'])
                return quotes
            except Exception:
                pass
        # SQLite Fallback
        with self.sqlite_conn() as conn:
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            quotes = c.execute("SELECT * FROM quotes").fetchall()
            return [dict(q) for q in quotes]


# Instantiate DB Manager
db_manager = DBManager(sqlite_path=SQLITE_DB_PATH, mongo_uri=MONGO_URI)

def seed_admin_user():
    admin = db_manager.get_user_by_email_or_username("admin")
    if not admin:
        print("Seeding default admin user...")
        hashed_pw = generate_password_hash("admin123")
        db_manager.create_user("admin", "admin@insure.com", hashed_pw, is_admin=1)
        print("Admin user seeded successfully. Username: admin, Password: admin123")
    else:
        # Check if is_admin is 1, otherwise update it
        try:
            with db_manager.sqlite_conn() as conn:
                c = conn.cursor()
                c.execute("UPDATE users SET is_admin = 1 WHERE username = 'admin'")
                conn.commit()
        except Exception:
            pass
        if db_manager.mongo_online and db_manager.mongo_db is not None:
            try:
                db_manager.mongo_db.users.update_one({"username": "admin"}, {"$set": {"is_admin": True}})
            except Exception:
                pass

# Run admin seeding on startup
seed_admin_user()


# ==============================================================================
# Model Initialization & Training
# ==============================================================================
def init_and_load_model():
    """Checks for the model artifact. Trains it if missing."""
    if not os.path.exists(MODEL_PATH):
        if not os.path.exists(DATA_PATH):
            print(f"Error: '{DATA_PATH}' not found. Cannot train model.")
            return None

        print("First-time setup: Training model...")
        df = pd.read_csv(DATA_PATH)

        X = df.drop(columns=['charges'])
        y = df['charges']

        from sklearn.compose import ColumnTransformer
        from sklearn.preprocessing import OneHotEncoder
        from sklearn.pipeline import Pipeline
        from sklearn.ensemble import RandomForestRegressor

        preprocessor = ColumnTransformer(
            transformers=[
                (
                    'cat',
                    OneHotEncoder(
                        drop='first',
                        handle_unknown='ignore'
                    ),
                    ['sex', 'smoker', 'region']
                )
            ],
            remainder='passthrough'
        )

        pipeline = Pipeline(
            steps=[
                ('preprocessor', preprocessor),
                ('regressor', RandomForestRegressor(
                    n_estimators=100,
                    random_state=42
                ))
            ]
        )

        pipeline.fit(X, y)

        joblib.dump(pipeline, MODEL_PATH)
        print("Model trained and saved successfully.")

    try:
        return joblib.load(MODEL_PATH)
    except Exception as e:
        print(f"Error loading model: {e}")
        return None

# Load model pipeline on startup
model_pipeline = init_and_load_model()


# ==============================================================================
# Auth Security & Session Decorator
# ==============================================================================
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or not session.get('is_admin'):
            flash("Admin privileges required to access this page.", "error")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


# ==============================================================================
# Page Routes
# ==============================================================================
@app.route('/')
@login_required
def index():
    profile = db_manager.get_profile(session['user_id'])
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
            # Check if user exists
            existing_user = db_manager.get_user_by_email_or_username(username)
            if not existing_user:
                existing_user = db_manager.get_user_by_email_or_username(email)
                
            if existing_user:
                error = 'Username or email already exists.'
            else:
                try:
                    hashed_pw = generate_password_hash(password)
                    user_id = db_manager.create_user(username, email, hashed_pw)
                    if user_id:
                        session['user_id'] = user_id
                        session['username'] = username
                        return redirect(url_for('create_profile'))
                    else:
                        error = 'An error occurred during account creation.'
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
            user = db_manager.get_user_by_email_or_username(login_input)
            if user and check_password_hash(user['password_hash'], password):
                session['user_id'] = user['id']
                session['username'] = user['username']
                session['is_admin'] = bool(user.get('is_admin', False)) or (user['username'] == 'admin')
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
    profile = db_manager.get_profile(session['user_id'])
    error = None
    
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
                profile_data = {
                    "first_name": first_name,
                    "last_name": last_name,
                    "age": age,
                    "sex": sex,
                    "bmi": bmi,
                    "children": children,
                    "smoker": smoker,
                    "region": region
                }
                db_manager.save_profile(session['user_id'], profile_data)
                return redirect(url_for('index'))
        except ValueError:
            error = 'Please enter valid numerical values for age, BMI, and children.'
        except Exception as e:
            error = f'Error saving profile: {str(e)}'
            
    return render_template('create_profile.html', profile=profile, error=error, username=session['username'])


# ==============================================================================
# Admin Routes
# ==============================================================================
@app.route('/admin')
@admin_required
def admin_dashboard():
    users = db_manager.get_all_users()
    profiles = db_manager.get_all_profiles()
    quotes = db_manager.get_all_quotes()

    profile_map = {p['user_id']: p for p in profiles}
    
    quotes_by_user = {}
    total_charges = 0.0
    for q in quotes:
        uid = q['user_id']
        if uid not in quotes_by_user:
            quotes_by_user[uid] = []
        quotes_by_user[uid].append(q)
        total_charges += q['charges']

    avg_charge = total_charges / len(quotes) if quotes else 0.0

    combined_users = []
    for u in users:
        uid = u['id']
        prof = profile_map.get(uid, {})
        u_quotes = quotes_by_user.get(uid, [])
        
        combined_users.append({
            'id': uid,
            'username': u['username'],
            'email': u['email'],
            'password_hash': u['password_hash'],
            'is_admin': bool(u.get('is_admin', False)) or (u['username'] == 'admin'),
            'created_at': u.get('created_at', ''),
            'first_name': prof.get('first_name', '-'),
            'last_name': prof.get('last_name', '-'),
            'age': prof.get('age', '-'),
            'sex': prof.get('sex', '-'),
            'bmi': prof.get('bmi', '-'),
            'children': prof.get('children', '-'),
            'smoker': prof.get('smoker', '-'),
            'region': prof.get('region', '-'),
            'quotes_count': len(u_quotes)
        })

    sex_counts = {'male': 0, 'female': 0, 'unknown': 0}
    smoker_counts = {'yes': 0, 'no': 0, 'unknown': 0}
    region_charges = {'northeast': [], 'northwest': [], 'southeast': [], 'southwest': []}
    bmi_categories = {'Underweight': 0, 'Healthy': 0, 'Overweight': 0, 'Obese': 0, 'Unknown': 0}

    for p in profiles:
        sex = p.get('sex', '').lower()
        if sex in sex_counts:
            sex_counts[sex] += 1
        else:
            sex_counts['unknown'] += 1

        smoker = p.get('smoker', '').lower()
        if smoker in smoker_counts:
            smoker_counts[smoker] += 1
        else:
            smoker_counts['unknown'] += 1

        bmi = p.get('bmi')
        if bmi is not None:
            try:
                bmi_val = float(bmi)
                if bmi_val < 18.5:
                    bmi_categories['Underweight'] += 1
                elif bmi_val < 25:
                    bmi_categories['Healthy'] += 1
                elif bmi_val < 30:
                    bmi_categories['Overweight'] += 1
                else:
                    bmi_categories['Obese'] += 1
            except ValueError:
                bmi_categories['Unknown'] += 1
        else:
            bmi_categories['Unknown'] += 1

    for q in quotes:
        reg = q.get('region', '').lower()
        if reg in region_charges:
            region_charges[reg].append(q['charges'])

    region_avg_charges = {}
    for reg, charges_list in region_charges.items():
        region_avg_charges[reg] = sum(charges_list) / len(charges_list) if charges_list else 0.0

    analytics = {
        'sex_counts': sex_counts,
        'smoker_counts': smoker_counts,
        'region_avg_charges': region_avg_charges,
        'bmi_categories': bmi_categories,
        'totals': {
            'users': len(users),
            'profiles': len(profiles),
            'quotes': len(quotes),
            'avg_charge': round(avg_charge, 2)
        }
    }

    admin_profile = db_manager.get_profile(session['user_id'])
    if not admin_profile:
        admin_profile = {'first_name': 'System', 'last_name': 'Admin'}

    return render_template('admin_dashboard.html', users=combined_users, analytics=analytics, profile=admin_profile)

@app.route('/admin/export/csv')
@admin_required
def admin_export_csv():
    users = db_manager.get_all_users()
    profiles = db_manager.get_all_profiles()
    quotes = db_manager.get_all_quotes()

    profile_map = {p['user_id']: p for p in profiles}
    
    quotes_by_user = {}
    for q in quotes:
        uid = q['user_id']
        if uid not in quotes_by_user:
            quotes_by_user[uid] = []
        quotes_by_user[uid].append(q)

    export_data = []
    for u in users:
        uid = u['id']
        prof = profile_map.get(uid, {})
        u_quotes = quotes_by_user.get(uid, [])
        avg_charge = sum(q['charges'] for q in u_quotes) / len(u_quotes) if u_quotes else 0.0
        
        export_data.append({
            'User ID': uid,
            'Username': u['username'],
            'Email': u['email'],
            'Password Hash': u['password_hash'],
            'Is Admin': 'Yes' if (bool(u.get('is_admin', False)) or u['username'] == 'admin') else 'No',
            'Created At': u.get('created_at', ''),
            'First Name': prof.get('first_name', ''),
            'Last Name': prof.get('last_name', ''),
            'Age': prof.get('age', ''),
            'Sex': prof.get('sex', ''),
            'BMI': prof.get('bmi', ''),
            'Children': prof.get('children', ''),
            'Smoker': prof.get('smoker', ''),
            'Region': prof.get('region', ''),
            'Quotes Saved Count': len(u_quotes),
            'Avg Quote Charges': round(avg_charge, 2)
        })

    df = pd.DataFrame(export_data)
    csv_data = df.to_csv(index=False)
    
    from flask import Response
    return Response(
        csv_data,
        mimetype="text/csv",
        headers={"Content-disposition": "attachment; filename=insure_users_dataset.csv"}
    )


# ==============================================================================
# Quote Estimation and DB Actions API (MongoDB with local SQLite backup)
# ==============================================================================

@app.route('/predict', methods=['POST'])
@login_required
def predict():
    if model_pipeline is None:
        return jsonify({'success': False, 'error': 'Model could not be loaded.'})

    try:
        data = request.get_json()
        age = int(data.get('age', 0))
        sex = data.get('sex', '')
        bmi = float(data.get('bmi', 0.0))
        children = int(data.get('children', 0))
        smoker = data.get('smoker', '')
        region = data.get('region', '')

        input_data = {
            'age': age,
            'sex': sex,
            'bmi': bmi,
            'children': children,
            'smoker': smoker,
            'region': region
        }
        
        input_df = pd.DataFrame([input_data])
        prediction = model_pipeline.predict(input_df)[0]
        
        return jsonify({'success': True, 'prediction': float(prediction)})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@app.route('/api/quotes', methods=['POST'])
@login_required
def save_quote():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"status": "error", "message": "No input payload received."}), 400

        saved_doc = db_manager.save_quote(session['user_id'], data)
        return jsonify({
            "status": "success",
            "message": "Quote saved successfully",
            "quote": saved_doc,
            "local_mode": not db_manager.mongo_online
        }), 201
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400


@app.route('/api/quotes', methods=['GET'])
@login_required
def get_quotes():
    smoker_filter = request.args.get('smoker')
    region_filter = request.args.get('region')

    try:
        history = db_manager.get_quotes_history(session['user_id'], smoker_filter, region_filter)
        return jsonify(history), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/api/quotes/<quote_id>', methods=['DELETE'])
@login_required
def delete_quote(quote_id):
    try:
        success = db_manager.delete_quote(session['user_id'], quote_id)
        if success:
            return jsonify({"status": "success", "message": "Quote deleted successfully."}), 200
        return jsonify({"status": "error", "message": "Quote not found or unauthorized."}), 404
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/api/db-status', methods=['GET'])
@login_required
def get_db_status():
    # Quick connectivity refresh check
    if db_manager.mongo_online:
        try:
            db_manager.mongo_client.server_info()
        except Exception:
            db_manager.mongo_online = False
    else:
        db_manager.check_mongo_connection()

    count = 0
    try:
        history = db_manager.get_quotes_history(session['user_id'])
        count = len(history)
    except Exception:
        pass

    return jsonify({
        "status": "online" if db_manager.mongo_online else "offline",
        "database": "insurance_db" if db_manager.mongo_online else "database.db (SQLite)",
        "records_count": count
    }), 200


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )
