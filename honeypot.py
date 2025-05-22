from flask import Flask, request, render_template_string, redirect, url_for
import datetime
import sqlite3

app = Flask(__name__)

# --- DB Setup ---
conn = sqlite3.connect('honeypot_logs.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                ip TEXT,
                user_agent TEXT,
                username TEXT,
                password TEXT,
                payload_detected TEXT
             )''')
conn.commit()

# --- Templates ---
login_page = '''
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>Admin Login</title>
    <style>
        body { background-color: #1e1e1e; color: #eee; font-family: sans-serif; display: flex; height: 100vh; align-items: center; justify-content: center; }
        .login-box { background: #2e2e2e; padding: 2em; border-radius: 12px; box-shadow: 0 0 12px #000; }
        input { display: block; width: 100%; padding: 0.5em; margin: 1em 0; background: #444; color: #fff; border: none; border-radius: 6px; }
        button { background: #007acc; color: white; border: none; padding: 0.7em 1.5em; border-radius: 6px; cursor: pointer; }
        button:hover { background: #005999; }
    </style>
</head>
<body>
<div class="login-box">
    <h2>Admin Login</h2>
    <form action="/login" method="post">
        <input type="text" name="username" placeholder="Username" required>
        <input type="password" name="password" placeholder="Password" required>
        <!-- Honeypot field -->
        <input type="text" name="invisible" style="display:none">
        <button type="submit">Login</button>
    </form>
</div>
</body>
</html>
'''

dashboard_page = '''
<!doctype html>
<html><head><title>Admin Dashboard</title></head>
<body style="background:#111;color:#fff;font-family:sans-serif;text-align:center;padding-top:50px;">
<h1>Welcome to the Admin Panel</h1>
<p>You have been logged... I mean, logged in 😉</p>
</body></html>
'''

# --- Helper ---
def detect_payloads(username, password):
    bad_keywords = ["<script", "--", "' OR", '" OR', "1=1", "admin' --"]
    combined = f"{username} {password}".lower()
    for kw in bad_keywords:
        if kw.lower() in combined:
            return kw
    return "None"

# --- Routes ---
@app.route('/')
def index():
    return render_template_string(login_page)

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    hidden_field = request.form.get('invisible')
    ip = request.remote_addr
    user_agent = request.headers.get('User-Agent')
    timestamp = datetime.datetime.now().isoformat()
    payload_flag = detect_payloads(username, password)

    if hidden_field:
        payload_flag = 'Bot detected (honeypot field filled)'

    c.execute('INSERT INTO logs (timestamp, ip, user_agent, username, password, payload_detected) VALUES (?, ?, ?, ?, ?, ?)',
              (timestamp, ip, user_agent, username, password, payload_flag))
    conn.commit()
    
    print(f"[+] Logged attempt: {username} / {password} from {ip}")


    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    return render_template_string(dashboard_page)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

@app.route('/view-logs')
def view_logs():
    conn = sqlite3.connect('honeypot_logs.db')
    c = conn.cursor()
    c.execute("SELECT timestamp, ip, username, password, payload_detected FROM logs ORDER BY id DESC")
    logs = c.fetchall()
    conn.close()

    html = """
    <h2>Captured Login Attempts</h2>
    <table border='1' cellpadding='5'>
        <tr><th>Time</th><th>IP</th><th>Username</th><th>Password</th><th>Payload?</th></tr>
        {}
    </table>
    """.format("".join([
        f"<tr><td>{ts}</td><td>{ip}</td><td>{u}</td><td>{p}</td><td>{payload}</td></tr>"
        for ts, ip, u, p, payload in logs
    ]))

    return html
