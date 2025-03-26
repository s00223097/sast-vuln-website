from flask import Flask, render_template, request, redirect, url_for, session, send_file
import mysql.connector
from mysql.connector import Error
import os
import subprocess
import json

app = Flask(__name__)
app.secret_key = 'super_secret_key_123'  # Hardcoded secret key
app.config['UPLOAD_FOLDER'] = 'uploads'  # No validation of file types

# Create uploads directory if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Vulnerable database connection
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='password',
            database='vuln_db'
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    # SQL Injection
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute(query)
        user = cursor.fetchone()
        
        if user:
            session['user_id'] = user[0]
            return redirect(url_for('dashboard'))
        else:
            return "Invalid credentials", 401

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    
    # SQL Injection
    user_id = session['user_id']
    query = f"SELECT * FROM users WHERE id={user_id}"
    
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute(query)
        user = cursor.fetchone()
        
        # No input validation
        cursor.execute(f"SELECT * FROM comments WHERE user_id={user_id} ORDER BY created_at DESC LIMIT 10")
        comments = cursor.fetchall()
        
        return render_template('dashboard.html', user=user, comments=comments)

@app.route('/search')
def search():
    #SQL Injection
    query = request.args.get('q', '')
    sql_query = f"SELECT * FROM products WHERE name LIKE '%{query}%'"
    
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute(sql_query)
        products = cursor.fetchall()
        return render_template('search.html', products=products)

@app.route('/comment', methods=['POST'])
def add_comment():
    # XSS
    comment = request.form['comment']
    user_id = session.get('user_id')
    
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute(f"INSERT INTO comments (user_id, comment) VALUES ({user_id}, '{comment}')")
        conn.commit()
        return redirect(url_for('dashboard'))

@app.route('/upload', methods=['POST'])
def upload_file():
    # file upload
    if 'file' not in request.files:
        return 'No file part', 400
    
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400
    
    # No file type validation
    filename = file.filename
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return 'File uploaded successfully'

@app.route('/download/<filename>')
def download_file(filename):
    # path traversal
    return send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename))

@app.route('/ping', methods=['POST'])
def ping():
    #command injection
    host = request.form.get('host', '')
    result = subprocess.check_output(f'ping -c 1 {host}', shell=True)
    return result

@app.route('/api/user/<user_id>')
def get_user(user_id):
    #information disclosure
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM users WHERE id={user_id}")
        user = cursor.fetchone()
        return json.dumps({
            'id': user[0],
            'username': user[1],
            'password': user[2]  # Exposing password in API
        })

@app.route('/admin')
def admin():
    #broken access control
    if 'user_id' not in session:
        return redirect(url_for('index'))
    
    user_id = session['user_id']
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM users WHERE id={user_id}")
        user = cursor.fetchone()
        
        # No proper admin check
        if user[1] == 'admin':
            cursor.execute("SELECT * FROM users")
            all_users = cursor.fetchall()
            return render_template('admin.html', users=all_users)
        else:
            return "Access denied", 403

if __name__ == '__main__':
    app.run(debug=True) 