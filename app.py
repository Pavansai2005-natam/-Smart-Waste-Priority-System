from flask import Flask, render_template, request, redirect, Response, session
import sqlite3

app = Flask(__name__)
app.secret_key = "smartwaste123"


# ---------------- DATABASE ----------------

def init_db():
    conn = sqlite3.connect("smartwaste.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS predictions(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        area TEXT,
        quantity INTEGER,
        delay INTEGER,
        priority TEXT
    )
    """)

    conn.commit()
    conn.close()


init_db()


# ---------------- LOGIN ----------------

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        if username == "admin" and password == "admin123":
            session["admin"] = True
            return redirect("/dashboard")

        else:
            return render_template(
                "login.html",
                error="Invalid Username or Password"
            )

    return render_template("login.html")



# ---------------- HOME ----------------

@app.route("/")
def home():
    return render_template("index.html")



# ---------------- PREDICT ----------------

@app.route("/predict", methods=["GET", "POST"])
def predict():

    # When user clicks "Predict Waste Priority"
    if request.method == "GET":
        return render_template("predict.html")


    # When prediction form is submitted
    area = request.form["area"]
    quantity = int(request.form["quantity"])
    delay = int(request.form["delay"])

    score = quantity + (delay * 10)

    if score >= 80:
        priority = "High"

    elif score >= 50:
        priority = "Medium"

    else:
        priority = "Low"


    # Save prediction to database
    conn = sqlite3.connect("smartwaste.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO predictions(area, quantity, delay, priority)
        VALUES (?, ?, ?, ?)
    """, (area, quantity, delay, priority))

    conn.commit()
    conn.close()


    return render_template(
        "result.html",
        area=area,
        quantity=quantity,
        delay=delay,
        priority=priority
    )

# ================= DASHBOARD =================

@app.route("/dashboard")
def dashboard():

    search = request.args.get("search", "")

    conn = sqlite3.connect("smartwaste.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM predictions
        WHERE area LIKE ?
        ORDER BY id DESC
    """, ("%" + search + "%",))

    rows = cursor.fetchall()

    cursor.execute("SELECT COUNT(*) FROM predictions")
    total = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM predictions
        WHERE priority = 'High'
    """)
    high = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM predictions
        WHERE priority = 'Medium'
    """)
    medium = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM predictions
        WHERE priority = 'Low'
    """)
    low = cursor.fetchone()[0]

    conn.close()

    return render_template(
        "dashboard.html",
        rows=rows,
        total=total,
        high=high,
        medium=medium,
        low=low,
        chart_labels=["High", "Medium", "Low"],
        chart_values=[high, medium, low]
    )


# ================= DELETE =================

@app.route("/delete/<int:id>")
def delete(id):

    conn = sqlite3.connect("smartwaste.db")
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM predictions WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect("/dashboard")



# ---------------- EXPORT CSV ----------------

@app.route("/export")
def export_csv():

    conn = sqlite3.connect("smartwaste.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM predictions")
    rows = cursor.fetchall()

    conn.close()


    def generate():

        yield "ID,Area,Quantity,Delay,Priority\n"

        for row in rows:
            yield f"{row[0]},{row[1]},{row[2]},{row[3]},{row[4]}\n"


    return Response(
        generate(),
        mimetype="text/csv",
        headers={
            "Content-Disposition":
            "attachment; filename=predictions.csv"
        }
    )



# ---------------- LOGOUT ----------------

@app.route("/logout")
def logout():

    session.pop("admin",None)

    return redirect("/login")



# ---------------- RUN ----------------

if __name__ == "__main__":
    app.run(debug=True)