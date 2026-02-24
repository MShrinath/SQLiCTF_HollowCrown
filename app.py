from flask import Flask, request, render_template
import sqlite3

app = Flask(__name__)
FLAG = "CTF{h0ll0w_cr0wn_3xf1ltr4t3d}"

def get_db():
    return sqlite3.connect("users.db")

def init_db():
    db = get_db()
    db.execute("DROP TABLE IF EXISTS users")
    db.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)")
    db.execute("INSERT INTO users VALUES (1,'user','user123')")
    db.execute("INSERT INTO users VALUES (2,'admin','admin123')")
    db.execute("INSERT INTO users VALUES (3,'CEO','C3O_t0p_s3cr3t!')")
    db.commit()
    db.close()

def vuln_login(username, password):
    db = get_db()
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    res = db.execute(query).fetchone()
    db.close()
    return res

@app.route("/")
def splash():
    return render_template("splash.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        u = request.form.get("username")
        p = request.form.get("password")
        user = vuln_login(u, p)
        if user:
            flag = FLAG if user[1] == "CEO" else None
            return render_template("dashboard.html", user=user, flag=flag)
        return render_template("login.html", error="Access denied. Invalid credentials.")
    return render_template("login.html")

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
