from flask import Flask, request, render_template, redirect, url_for, send_from_directory
import datetime, os, json

app = Flask(__name__)
LOG_FILE = "ip_logs.txt"

def log_ip(path):
    ip = request.headers.get('X-Forwarded-For',
          request.headers.get('X-Real-IP', request.remote_addr))
    with open(LOG_FILE, "a") as f:
        f.write(f"{datetime.datetime.now()} - {ip} - {path}\n")

@app.before_request
def before():
    log_ip(request.path)

@app.route('/')
def home():
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == 'admin' and password == 'admin123':
            return redirect('/dashboard')
        return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/admin-portal-45sd2/check')
def admin_portal():
    if request.args.get("key") == "letmein":
        return render_template("admin.html")
    return render_template("fake_admin.html")

@app.route('/log_fingerprint', methods=['POST'])
def log_fingerprint():
    data = request.get_json()
    with open("fingerprints.json", "a") as f:
        f.write(json.dumps(data) + "\n")
    return {"status": "logged"}

@app.route('/robots.txt')
def robots():
    return "User-agent: *\nDisallow: /hidden-dir/", 200, {'Content-Type': 'text/plain'}

@app.route('/hidden-dir/clue.html')
def clue_page():
    return send_from_directory("hidden-dir", "clue.html")