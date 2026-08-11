from flask import Flask, render_template, request, redirect
import sqlite3
import csv
from io import StringIO
from flask import Response


app = Flask(__name__)


# =====================================================
# DATABASE
# =====================================================

def init_db():

    conn = sqlite3.connect("smartwaste.db")

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            area TEXT NOT NULL,
            quantity REAL NOT NULL,
            delay INTEGER NOT NULL,
            priority TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# =====================================================
# HOME PAGE
# =====================================================

@app.route("/")
def home():

    return render_template("index.html")


# =====================================================
# PREDICT PAGE
# =====================================================

@app.route("/predict", methods=["GET", "POST"])
def predict():

    if request.method == "POST":

        area = request.form.get("area")

        quantity = float(
            request.form.get("quantity", 0)
        )

        delay = int(
            request.form.get("delay", 0)
        )


        # ---------------------------------------------
        # PRIORITY CALCULATION
        # ---------------------------------------------

        score = quantity + (delay * 10)


        if score >= 80:

            priority = "High"

        elif score >= 50:

            priority = "Medium"

        else:

            priority = "Low"


        # ---------------------------------------------
        # SAVE TO DATABASE
        # ---------------------------------------------

        conn = sqlite3.connect("smartwaste.db")

        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO predictions
            (area, quantity, delay, priority)
            VALUES (?, ?, ?, ?)
        """, (
            area,
            quantity,
            delay,
            priority
        ))

        conn.commit()
        conn.close()


        # ---------------------------------------------
        # RESULT PAGE
        # ---------------------------------------------

        return render_template(
            "result.html",
            area=area,
            quantity=quantity,
            delay=delay,
            priority=priority
        )


    return render_template("predict.html")


# =====================================================
# ADMIN DASHBOARD
# =====================================================

@app.route("/dashboard")
def dashboard():

    conn = sqlite3.connect("smartwaste.db")

    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()


    # ALL RECORDS

    cursor.execute("""
        SELECT *
        FROM predictions
        ORDER BY id DESC
    """)

    predictions = cursor.fetchall()


    # TOTAL

    cursor.execute("""
        SELECT COUNT(*)
        FROM predictions
    """)

    total = cursor.fetchone()[0]


    # HIGH

    cursor.execute("""
        SELECT COUNT(*)
        FROM predictions
        WHERE priority = 'High'
    """)

    high = cursor.fetchone()[0]


    # MEDIUM

    cursor.execute("""
        SELECT COUNT(*)
        FROM predictions
        WHERE priority = 'Medium'
    """)

    medium = cursor.fetchone()[0]


    # LOW

    cursor.execute("""
        SELECT COUNT(*)
        FROM predictions
        WHERE priority = 'Low'
    """)

    low = cursor.fetchone()[0]


    conn.close()


    # CHART DATA

    chart_labels = [
        "High",
        "Medium",
        "Low"
    ]

    chart_values = [
        high,
        medium,
        low
    ]


    return render_template(
        "dashboard.html",
        predictions=predictions,
        total=total,
        high=high,
        medium=medium,
        low=low,
        chart_labels=chart_labels,
        chart_values=chart_values
    )


# =====================================================
# DELETE PREDICTION
# =====================================================

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


# =====================================================
# EXPORT CSV
# =====================================================

@app.route("/export")
def export():

    conn = sqlite3.connect("smartwaste.db")

    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            area,
            quantity,
            delay,
            priority
        FROM predictions
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()

    conn.close()


    output = StringIO()

    writer = csv.writer(output)

    writer.writerow([
        "ID",
        "Area",
        "Waste Quantity (kg)",
        "Collection Delay (days)",
        "Priority"
    ])


    for row in rows:

        writer.writerow(row)


    output.seek(0)


    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={
            "Content-Disposition":
            "attachment; filename=smartwaste_predictions.csv"
        }
    )


# =====================================================
# START APPLICATION
# =====================================================

if __name__ == "__main__":

    init_db()

    app.run(
        debug=True
    )