import http.server
import socketserver
import sqlite3
import json
import urllib.parse
import os

PORT = 8000
DB_FILE = "messages.db"

# Customizable credentials for single-user authentication
AUTH_PIN = "4884"
AUTH_TOKEN = "shamil_secure_session_token"

# ==========================================
# 1. Database Setup & Initialization
# ==========================================
def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            subject TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()
    print(f"[*] SQLite Database '{DB_FILE}' initialized and ready.")

# ==========================================
# 2. Authentication Helper Functions
# ==========================================
def check_auth(headers):
    cookie_header = headers.get("Cookie", "")
    cookies = {}
    for item in cookie_header.split(";"):
        if "=" in item:
            k, v = item.strip().split("=", 1)
            cookies[k] = v
    return cookies.get("auth_token") == AUTH_TOKEN

# ==========================================
# 3. HTML Login Page Template Generator
# ==========================================
def generate_login_html(error_msg=None):
    error_banner = ""
    if error_msg:
        error_banner = f"""
        <div class="error-banner">
            <i class="fas fa-exclamation-circle"></i> {error_msg}
        </div>
        """
        
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard Access | Muhammed Shamil P</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root {{
            --bg-primary: #05070c;
            --bg-secondary: #0b111e;
            --text-primary: #f8fafc;
            --text-secondary: #94a3b8;
            --border-color: rgba(255, 255, 255, 0.06);
            --glass-bg: rgba(11, 17, 30, 0.75);
            --glass-border: rgba(255, 255, 255, 0.08);
            --accent-gradient: linear-gradient(135deg, #6366f1, #a855f7);
            --accent-solid: #6366f1;
            --red-status: #f87171;
        }}
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Plus Jakarta Sans', sans-serif;
        }}
        body {{
            background-color: var(--bg-primary);
            color: var(--text-primary);
            min-height: 100vh;
            line-height: 1.6;
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        .glow-blob {{
            position: fixed;
            width: 400px;
            height: 400px;
            border-radius: 50%;
            background: radial-gradient(circle, #6366f1, #7c3aed);
            filter: blur(140px);
            opacity: 0.12;
            z-index: -1;
        }}
        #blob-1 {{ top: 10%; left: 10%; }}
        #blob-2 {{ bottom: 10%; right: 10%; }}
        
        .login-card {{
            width: 100%;
            max-width: 400px;
            padding: 40px 32px;
            background: var(--glass-bg);
            backdrop-filter: blur(12px);
            border: 1px solid var(--glass-border);
            border-radius: 20px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.4);
            text-align: center;
        }}
        .lock-icon {{
            font-size: 40px;
            background: var(--accent-gradient);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 20px;
            display: inline-block;
        }}
        h2 {{
            font-family: 'Outfit', sans-serif;
            font-size: 28px;
            font-weight: 800;
            margin-bottom: 6px;
        }}
        p {{
            font-size: 14px;
            color: var(--text-secondary);
            margin-bottom: 30px;
        }}
        .form-group {{
            margin-bottom: 24px;
            text-align: left;
        }}
        .form-group label {{
            font-size: 13px;
            font-weight: 700;
            color: var(--text-secondary);
            margin-bottom: 8px;
            display: block;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        .form-group input {{
            width: 100%;
            padding: 14px;
            border-radius: 10px;
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid var(--border-color);
            color: var(--text-primary);
            font-size: 20px;
            outline: none;
            text-align: center;
            letter-spacing: 4px;
            font-weight: 700;
            transition: all 0.3s ease;
        }}
        .form-group input:focus {{
            border-color: var(--accent-solid);
            background: rgba(255, 255, 255, 0.08);
            box-shadow: 0 0 12px rgba(99, 102, 241, 0.15);
        }}
        .btn-submit {{
            width: 100%;
            padding: 14px;
            border-radius: 10px;
            border: none;
            background: var(--accent-gradient);
            color: #ffffff;
            font-size: 16px;
            font-weight: 700;
            cursor: pointer;
            box-shadow: 0 4px 15px rgba(99, 102, 241, 0.2);
            transition: all 0.3s ease;
        }}
        .btn-submit:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(99, 102, 241, 0.35);
        }}
        .error-banner {{
            background: rgba(248, 113, 113, 0.1);
            border: 1px solid rgba(248, 113, 113, 0.2);
            color: var(--red-status);
            padding: 12px;
            border-radius: 8px;
            font-size: 13px;
            font-weight: 600;
            margin-bottom: 20px;
            text-align: center;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
        }}
    </style>
</head>
<body>
    <div class="glow-blob" id="blob-1"></div>
    <div class="glow-blob" id="blob-2"></div>

    <div class="login-card">
        <span class="lock-icon"><i class="fas fa-lock"></i></span>
        <h2>Secure Dashboard</h2>
        <p>Enter your secret passcode to view inbox messages</p>
        
        {error_banner}

        <form action="/login" method="POST">
            <div class="form-group">
                <label for="passcode">Secret Passcode</label>
                <input type="password" id="passcode" name="passcode" placeholder="••••" required autofocus autocomplete="off">
            </div>
            <button type="submit" class="btn-submit">Authenticate <i class="fas fa-arrow-right"></i></button>
        </form>
    </div>
</body>
</html>
"""

# ==========================================
# 4. HTML Dashboard Template Generator
# ==========================================
def generate_dashboard_html(messages):
    message_cards = ""
    
    if not messages:
        message_cards = """
        <div class="empty-state">
            <i class="fas fa-inbox"></i>
            <h3>No messages yet</h3>
            <p>Your inbox is empty. Message submissions will appear here in real-time.</p>
        </div>
        """
    else:
        for msg in messages:
            msg_id, name, email, subject, text, created_at = msg
            message_cards += f"""
            <div class="message-card glass-card">
                <div class="card-header">
                    <div class="user-meta">
                        <span class="user-avatar"><i class="fas fa-user"></i></span>
                        <div>
                            <h4>{name}</h4>
                            <a href="mailto:{email}" class="user-email">{email}</a>
                        </div>
                    </div>
                    <span class="timestamp"><i class="far fa-clock"></i> {created_at}</span>
                </div>
                <div class="card-body">
                    <div class="subject-badge">Subject: {subject}</div>
                    <p class="message-text">{text}</p>
                </div>
                <div class="card-footer">
                    <a href="/delete-message?id={msg_id}" class="delete-btn" onclick="return confirm('Are you sure you want to delete this message?');">
                        <i class="fas fa-trash-alt"></i> Delete Message
                    </a>
                </div>
            </div>
            """

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Inbox Dashboard | Muhammed Shamil P</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root {{
            --bg-primary: #05070c;
            --bg-secondary: #0b111e;
            --text-primary: #f8fafc;
            --text-secondary: #94a3b8;
            --border-color: rgba(255, 255, 255, 0.06);
            --glass-bg: rgba(11, 17, 30, 0.75);
            --glass-border: rgba(255, 255, 255, 0.08);
            --accent-gradient: linear-gradient(135deg, #6366f1, #a855f7);
            --accent-solid: #6366f1;
            --red-status: #f87171;
            --green-status: #34d399;
        }}
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Plus Jakarta Sans', sans-serif;
        }}
        body {{
            background-color: var(--bg-primary);
            color: var(--text-primary);
            min-height: 100vh;
            line-height: 1.6;
            padding-bottom: 60px;
        }}
        .glow-blob {{
            position: fixed;
            width: 400px;
            height: 400px;
            border-radius: 50%;
            background: radial-gradient(circle, #6366f1, #7c3aed);
            filter: blur(140px);
            opacity: 0.15;
            z-index: -1;
        }}
        #blob-1 {{ top: -10%; left: -10%; }}
        #blob-2 {{ bottom: -10%; right: -10%; }}
        
        .container {{
            max-width: 1000px;
            margin: 0 auto;
            padding: 40px 24px;
        }}
        header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 24px;
            margin-bottom: 40px;
            flex-wrap: wrap;
            gap: 20px;
        }}
        h1 {{
            font-family: 'Outfit', sans-serif;
            font-size: 32px;
            font-weight: 800;
            background: var(--accent-gradient);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        .header-actions {{
            display: flex;
            align-items: center;
            gap: 16px;
        }}
        .stats-badge {{
            background: rgba(99, 102, 241, 0.15);
            border: 1px solid rgba(99, 102, 241, 0.3);
            color: var(--accent-solid);
            padding: 6px 16px;
            border-radius: 50px;
            font-size: 14px;
            font-weight: 700;
        }}
        .logout-btn {{
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid var(--border-color);
            color: var(--text-secondary);
            padding: 6px 16px;
            border-radius: 50px;
            font-size: 13px;
            font-weight: 700;
            text-decoration: none;
            transition: all 0.2s ease;
            display: flex;
            align-items: center;
            gap: 6px;
        }}
        .logout-btn:hover {{
            background: rgba(248, 113, 113, 0.1);
            color: var(--red-status);
            border-color: rgba(248, 113, 113, 0.2);
        }}
        
        .messages-list {{
            display: grid;
            grid-template-columns: 1fr;
            gap: 24px;
        }}
        .glass-card {{
            background: var(--glass-bg);
            backdrop-filter: blur(12px);
            border: 1px solid var(--glass-border);
            border-radius: 16px;
            padding: 24px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
            transition: transform 0.2s ease, border-color 0.2s ease;
        }}
        .glass-card:hover {{
            transform: translateY(-2px);
            border-color: rgba(99, 102, 241, 0.4);
        }}
        .card-header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            flex-wrap: wrap;
            gap: 16px;
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 16px;
            margin-bottom: 16px;
        }}
        .user-meta {{
            display: flex;
            align-items: center;
            gap: 16px;
        }}
        .user-avatar {{
            width: 44px;
            height: 44px;
            border-radius: 50%;
            background: var(--accent-gradient);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 18px;
            color: #fff;
        }}
        .user-meta h4 {{
            font-family: 'Outfit', sans-serif;
            font-size: 18px;
            font-weight: 600;
        }}
        .user-email {{
            font-size: 13px;
            color: var(--text-secondary);
            text-decoration: none;
            transition: color 0.2s ease;
        }}
        .user-email:hover {{
            color: var(--accent-solid);
            text-decoration: underline;
        }}
        .timestamp {{
            font-size: 13px;
            color: var(--text-secondary);
            font-weight: 600;
        }}
        .subject-badge {{
            display: inline-block;
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid var(--border-color);
            padding: 4px 12px;
            border-radius: 6px;
            font-size: 13px;
            font-weight: 700;
            color: var(--text-primary);
            margin-bottom: 12px;
        }}
        .message-text {{
            font-size: 15px;
            color: var(--text-secondary);
            white-space: pre-wrap;
        }}
        .card-footer {{
            display: flex;
            justify-content: flex-end;
            margin-top: 16px;
            border-top: 1px solid var(--border-color);
            padding-top: 16px;
        }}
        .delete-btn {{
            background: transparent;
            border: 1px solid rgba(248, 113, 113, 0.2);
            color: var(--red-status);
            padding: 8px 16px;
            border-radius: 8px;
            font-size: 13px;
            font-weight: 700;
            text-decoration: none;
            cursor: pointer;
            transition: all 0.2s ease;
            display: inline-flex;
            align-items: center;
            gap: 8px;
        }}
        .delete-btn:hover {{
            background: var(--red-status);
            color: #fff;
            border-color: var(--red-status);
            box-shadow: 0 4px 12px rgba(248, 113, 113, 0.2);
        }}
        
        .empty-state {{
            text-align: center;
            padding: 60px 40px;
            background: var(--glass-bg);
            border: 1px dashed var(--glass-border);
            border-radius: 16px;
        }}
        .empty-state i {{
            font-size: 50px;
            color: var(--text-secondary);
            margin-bottom: 16px;
            opacity: 0.5;
        }}
        .empty-state h3 {{
            font-family: 'Outfit', sans-serif;
            font-size: 22px;
            margin-bottom: 8px;
        }}
        .empty-state p {{
            font-size: 14px;
            color: var(--text-secondary);
            max-width: 400px;
            margin: 0 auto;
        }}
    </style>
</head>
<body>
    <div class="glow-blob" id="blob-1"></div>
    <div class="glow-blob" id="blob-2"></div>

    <div class="container">
        <header>
            <div>
                <h1>Inbox Dashboard</h1>
                <p style="font-size: 14px; color: var(--text-secondary); margin-top: 4px;">Muhammed Shamil P | Contact Submissions</p>
            </div>
            <div class="header-actions">
                <div class="stats-badge">
                    <i class="fas fa-envelope"></i> Total Messages: {len(messages)}
                </div>
                <a href="/logout" class="logout-btn"><i class="fas fa-sign-out-alt"></i> Logout</a>
            </div>
        </header>

        <main class="messages-list">
            {message_cards}
        </main>
    </div>
</body>
</html>
"""

# ==========================================
# 5. HTTP Request Routing Handlers
# ==========================================
class MessageHandler(http.server.BaseHTTPRequestHandler):

    def _set_cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS, DELETE")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def do_OPTIONS(self):
        self.send_response(204)
        self._set_cors_headers()
        self.end_headers()

    def do_GET(self):
        parsed_url = urllib.parse.urlparse(self.path)
        
        # Route: GET /logout
        if parsed_url.path == "/logout":
            self.send_response(303)
            self.send_header("Set-Cookie", "auth_token=; Path=/; Max-Age=0; HttpOnly")
            self.send_header("Location", "/dashboard")
            self.end_headers()
            return

        # Route: GET /dashboard or GET /
        elif parsed_url.path == "/dashboard" or parsed_url.path == "/":
            # Check Authentication
            if not check_auth(self.headers):
                html_content = generate_login_html()
                self.send_response(200)
                self.send_header("Content-Type", "text/html")
                self.end_headers()
                self.wfile.write(html_content.encode("utf-8"))
                return

            # Fetch Messages
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, email, subject, message, datetime(created_at, 'localtime') FROM messages ORDER BY id DESC")
            messages = cursor.fetchall()
            conn.close()

            html_content = generate_dashboard_html(messages)
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(html_content.encode("utf-8"))
            return

        # Route: GET /delete-message?id=<id>
        elif parsed_url.path == "/delete-message":
            # Check Authentication
            if not check_auth(self.headers):
                self.send_response(303)
                self.send_header("Location", "/dashboard")
                self.end_headers()
                return

            query_params = urllib.parse.parse_qs(parsed_url.query)
            msg_id = query_params.get("id", [None])[0]
            
            if msg_id:
                conn = sqlite3.connect(DB_FILE)
                cursor = conn.cursor()
                cursor.execute("DELETE FROM messages WHERE id = ?", (msg_id,))
                conn.commit()
                conn.close()
                print(f"[x] Deleted message ID: {msg_id}")

            # Redirect back to dashboard
            self.send_response(303)
            self.send_header("Location", "/dashboard")
            self.end_headers()
            return

        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not Found")

    def do_POST(self):
        parsed_url = urllib.parse.urlparse(self.path)

        # Route: POST /login (form submission passcode validation)
        if parsed_url.path == "/login":
            content_length = int(self.headers.get("Content-Length", 0))
            post_data = self.rfile.read(content_length).decode("utf-8")
            form_params = urllib.parse.parse_qs(post_data)
            
            passcode = form_params.get("passcode", [None])[0]
            
            if passcode == AUTH_PIN:
                # Auth success -> set cookie and redirect to dashboard
                self.send_response(303)
                self.send_header("Set-Cookie", f"auth_token={AUTH_TOKEN}; Path=/; HttpOnly")
                self.send_header("Location", "/dashboard")
                self.end_headers()
                return
            else:
                # Auth failed -> re-render login with error
                html_content = generate_login_html("Incorrect passcode. Access denied.")
                self.send_response(200)
                self.send_header("Content-Type", "text/html")
                self.end_headers()
                self.wfile.write(html_content.encode("utf-8"))
                return

        # Route: POST /api/messages (public API for contact form)
        elif parsed_url.path == "/api/messages":
            content_length = int(self.headers.get("Content-Length", 0))
            post_data = self.rfile.read(content_length)
            
            try:
                data = json.loads(post_data.decode("utf-8"))
                name = data.get("name")
                email = data.get("email")
                subject = data.get("subject")
                message = data.get("message")

                if not name or not email or not subject or not message:
                    self.send_response(400)
                    self._set_cors_headers()
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps({"success": False, "error": "Missing fields"}).encode("utf-8"))
                    return

                # Write to Database
                conn = sqlite3.connect(DB_FILE)
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO messages (name, email, subject, message) VALUES (?, ?, ?, ?)",
                    (name, email, subject, message)
                )
                conn.commit()
                conn.close()
                print(f"[+] Saved message from {name} ({email}) Subject: {subject}")

                # Success Response
                self.send_response(201)
                self._set_cors_headers()
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"success": True, "message": "Saved successfully!"}).encode("utf-8"))
                return

            except Exception as e:
                self.send_response(500)
                self._set_cors_headers()
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"success": False, "error": str(e)}).encode("utf-8"))
                return
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not Found")

# ==========================================
# 6. Spawns Server Instance
# ==========================================
if __name__ == "__main__":
    init_db()
    
    # Configure socket server allowing address reuse
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), MessageHandler) as httpd:
        print(f"[+] Python secure server running at http://localhost:{PORT}/")
        print(f"[+] Inbox dashboard accessible at http://localhost:{PORT}/dashboard")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n[-] Shutting down local server.")
