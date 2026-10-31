from flask import Flask, render_template, redirect, url_for, request, session, flash
import sqlite3

app = Flask(__name__)
app.secret_key = "supersecretkey"

# ---------------- DATABASE ----------------

def init_db():
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS resources(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        name TEXT,
        type TEXT,
        region TEXT,
        cost REAL,
        status TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()

# ---------------- AUTH ----------------

@app.route('/')
def home():
    if "user_id" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        conn = sqlite3.connect("database.db")
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO users(username,password) VALUES(?,?)",
                        (request.form['username'], request.form['password']))
            conn.commit()
            flash("Registration successful!","success")
            return redirect(url_for("login"))
        except:
            flash("Username already exists!","danger")
        conn.close()
    return render_template("register.html")

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        conn = sqlite3.connect("database.db")
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username=? AND password=?",
                    (request.form['username'], request.form['password']))
        user = cur.fetchone()
        conn.close()

        if user:
            session["user_id"] = user[0]
            session["username"] = user[1]
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid credentials","danger")

    return render_template("login.html")

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("login"))

# ---------------- DASHBOARD ----------------

@app.route('/dashboard')
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM resources WHERE user_id=?",
                (session["user_id"],))
    rows = cur.fetchall()
    conn.close()

    approved_regions = ["ap-south-1", "us-east-1"]

    resources = []
    suspicious_count = 0
    total_cost = 0

    for r in rows:
        cost = r[5]
        region = r[4]
        status = r[6]

        total_cost += cost

        # Suspicious Logic
        is_suspicious = False
        risk_score = 0

        if cost > 150:
            is_suspicious = True
            risk_score += 40

        if region not in approved_regions:
            is_suspicious = True
            risk_score += 30

        if cost > 150 and status == "Running":
            risk_score += 30

        if is_suspicious:
            suspicious_count += 1

        resources.append((*r, is_suspicious, risk_score))

    total = len(resources)

    # Threat Level
    if suspicious_count >= 3:
        threat = "HIGH"
    elif suspicious_count >= 1:
        threat = "MEDIUM"
    else:
        threat = "LOW"

    return render_template("dashboard.html",
                           total=total,
                           suspicious=suspicious_count,
                           total_cost=round(total_cost,2),
                           threat=threat,
                           resources=resources)

# ---------------- CRUD ----------------

@app.route('/add_resource', methods=['POST'])
def add_resource():
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("""
    INSERT INTO resources(user_id,name,type,region,cost,status)
    VALUES(?,?,?,?,?,?)
    """,(session["user_id"],
         request.form['name'],
         request.form['type'],
         request.form['region'],
         float(request.form['cost']),
         request.form['status']))
    conn.commit()
    conn.close()
    return redirect(url_for("dashboard"))

@app.route('/edit_resource/<int:id>', methods=['GET','POST'])
def edit_resource(id):
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    if request.method == 'POST':
        cur.execute("""
        UPDATE resources
        SET name=?, type=?, region=?, cost=?, status=?
        WHERE id=?
        """,(request.form['name'],
             request.form['type'],
             request.form['region'],
             float(request.form['cost']),
             request.form['status'],
             id))
        conn.commit()
        conn.close()
        return redirect(url_for("dashboard"))

    cur.execute("SELECT * FROM resources WHERE id=?",(id,))
    resource = cur.fetchone()
    conn.close()
    return render_template("edit_resource.html", resource=resource)

@app.route('/delete_resource/<int:id>')
def delete_resource(id):
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM resources WHERE id=?",(id,))
    conn.commit()
    conn.close()
    return redirect(url_for("dashboard"))

if __name__ == "__main__":
    app.run(debug=True)