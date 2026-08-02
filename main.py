import os
from flask import Flask, render_template_string, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = 'copyguard_super_secret_key'

# 🔑 AAPKA NAYA PASSWORD SET HO GAYA HAI:
SITE_PASSWORD = "Rakesh222"

LOGIN_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CopyGuard - Access Restricted</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #0f172a; color: white; margin: 0; padding: 20px; display: flex; justify-content: center; align-items: center; min-height: 100vh; }
        .card { background: #1e293b; padding: 30px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.5); max-width: 400px; width: 100%; text-align: center; }
        h1 { color: #38bdf8; margin-bottom: 10px; font-size: 24px; }
        p { color: #94a3b8; font-size: 14px; }
        input[type="password"] { width: 80%; padding: 10px; border-radius: 6px; border: 1px solid #334155; background: #0f172a; color: white; margin-top: 15px; text-align: center; font-size: 16px; }
        .btn { background: #0284c7; color: white; border: none; padding: 10px 20px; border-radius: 6px; margin-top: 15px; font-weight: bold; cursor: pointer; width: 85%; }
        .btn:hover { background: #0369a1; }
        .error { color: #ef4444; font-size: 13px; margin-top: 10px; }
    </style>
</head>
<body>
    <div class="card">
        <h1>🔒 Private Access Only</h1>
        <p>Is website ko access karne ke liye password daalein.</p>
        
        <form action="/login" method="post">
            <input type="password" name="password" placeholder="Enter Password" required />
            <br>
            <button type="submit" class="btn">Unlock Access 🔑</button>
        </form>
        {% if error %}
            <div class="error">{{ error }}</div>
        {% endif %}
    </div>
</body>
</html>
"""

DASHBOARD_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CopyGuard Dashboard</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #0f172a; color: white; margin: 0; padding: 20px; display: flex; justify-content: center; align-items: center; min-height: 100vh; }
        .card { background: #1e293b; padding: 30px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.5); max-width: 500px; width: 100%; text-align: center; }
        h1 { color: #38bdf8; margin-bottom: 10px; }
        p { color: #94a3b8; font-size: 14px; }
        input[type="file"] { display: none; }
        .custom-file-upload { display: inline-block; background: #0284c7; color: white; padding: 12px 24px; border-radius: 8px; font-weight: bold; margin-top: 15px; cursor: pointer; }
        .submit-btn { background: #22c55e; color: white; border: none; padding: 10px 20px; border-radius: 6px; margin-top: 15px; font-weight: bold; cursor: pointer; display: none; }
        .logout-btn { display: inline-block; color: #ef4444; text-decoration: none; font-size: 12px; margin-top: 25px; }
    </style>
</head>
<body>
    <div class="card">
        <h1>CopyGuard Dashboard 🛡️</h1>
        <p>Video Watermark Remover & Audio Pitch Shifter</p>
        <hr style="border-color: #334155; margin: 20px 0;">
        
        <form action="/upload" method="post" enctype="multipart/form-data">
            <label for="video-upload" class="custom-file-upload">
                📂 Choose Video File
            </label>
            <input id="video-upload" name="file" type="file" accept="video/*" onchange="showSubmit()"/>
            <br><br>
            <span id="file-name" style="font-size: 13px; color: #38bdf8;"></span>
            <br>
            <button type="submit" id="sub-btn" class="submit-btn">Process Video 🚀</button>
        </form>
        <br>
        <a href="/logout" class="logout-btn">🔒 Lock / Logout</a>
    </div>

    <script>
        function showSubmit() {
            var input = document.getElementById('video-upload');
            var fileName = input.files[0].name;
            document.getElementById('file-name').textContent = "Selected: " + fileName;
            document.getElementById('sub-btn').style.display = "inline-block";
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    if not session.get('authenticated'):
        return render_template_string(LOGIN_TEMPLATE)
    return render_template_string(DASHBOARD_TEMPLATE)

@app.route('/login', methods=['POST'])
def login():
    entered_password = request.form.get('password')
    if entered_password == SITE_PASSWORD:
        session['authenticated'] = True
        return redirect(url_for('home'))
    return render_template_string(LOGIN_TEMPLATE, error="Wrong Password! Access Denied.")

@app.route('/logout')
def logout():
    session.pop('authenticated', None)
    return redirect(url_for('home'))

@app.route('/upload', methods=['POST'])
def upload():
    if not session.get('authenticated'):
        return "Unauthorized", 401
    if 'file' not in request.files:
        return "No file uploaded", 400
    file = request.files['file']
    return f"<h2 style='color:white; background:#0f172a; text-align:center; padding:50px;'>File '{file.filename}' uploaded successfully!</h2>"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
