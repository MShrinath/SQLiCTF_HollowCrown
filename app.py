from flask import Flask, request, render_template
import sqlite3

app = Flask(__name__)

def get_db():
    return sqlite3.connect("users.db")

def init_db():
    db = get_db()
    db.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)")
    db.execute("INSERT OR IGNORE INTO users VALUES (1,'admin','admin123')")
    db.execute("INSERT OR IGNORE INTO users VALUES (2,'user','user123')")
    db.commit()
    db.close()

def vuln_login(username, password):
    db = get_db()
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    res = db.execute(query).fetchone()
    db.close()
    return res

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        u = request.form.get("username")
        p = request.form.get("password")
        user = vuln_login(u, p)
        if user:
            return render_template("dashboard.html", user=user)
        return "Login failed"
    return render_template("login.html")

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
