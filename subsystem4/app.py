import os
from flask import Flask, render_template, request, redirect, url_for, send_file
from subsystem4.models import DatabaseManager, AICoachService, ReportGenerator, Subsystem4ErrorHandler, Subsystem4Exception

app = Flask(__name__)

# Initialize Subsystem 4 components
db_manager = DatabaseManager("subsystem4/energy_data.db")
ai_coach = AICoachService()
report_generator = ReportGenerator("subsystem4/sustainability_report.pdf")

@app.route("/")
def index():
    """Subsystem 4 Home Route."""
    try:
        with db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT timestamp, kwh_used, cost FROM energy_logs ORDER BY id DESC LIMIT 5;")
            logs = cursor.fetchall()
    except Exception as e:
        Subsystem4ErrorHandler.handle_database_error(e)
        logs = []
    
    return render_template("index.html", logs=logs)

@app.route("/log", methods=["GET", "POST"])
def log_energy():
    """Log new energy consumption and generate AI coach feedback."""
    tip = None
    if request.method == "POST":
        try:
            timestamp = request.form.get("timestamp")
            kwh_used = float(request.form.get("kwh_used", 0))
            cost = float(request.form.get("cost", 0))

            with db_manager.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO energy_logs (timestamp, kwh_used, cost) VALUES (?, ?, ?)",
                               (timestamp, kwh_used, cost))
                conn.commit()

            # Generate AI Coach tip
            tip = ai_coach.generate_coach_tips(kwh_used)
            # Generate Report
            report_generator.create_pdf_report(f"Logged {kwh_used} kWh on {timestamp}", tip)

            return render_template("log.html", success=True, tip=tip)
        except Exception as e:
            Subsystem4ErrorHandler.handle_database_error(e)
            return render_template("log.html", error=str(e))

    return render_template("log.html", success=False, tip=tip)

@app.route("/report")
def download_report():
    """Download the generated Subsystem 4 PDF report."""
    report_path = "subsystem4/sustainability_report.pdf"
    if os.path.exists(report_path):
        return send_file(report_path, as_attachment=True)
    return "Report not found. Please log energy data first.", 404

if __name__ == "__main__":
    app.run(debug=True, port=5000)