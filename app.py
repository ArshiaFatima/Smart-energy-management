from flask import Flask, render_template_string, request, send_file
from subsystem4.models import DatabaseManager, AICoachService, ReportGenerator
import os

app = Flask(__name__)

# Initialize our OOP services
db_manager = DatabaseManager()
ai_coach = AICoachService()

@app.route("/")
def index():
    return """
    <h1>Smart Energy Management - Subsystem 4</h1>
    <p>Welcome to the AI Sustainability Coach & Reports System!</p>
    <ul>
        <li><a href="/log">Log Energy Usage</a></li>
        <li><a href="/report">Generate PDF Report</a></li>
    </ul>
    """

@app.route("/log", methods=["GET", "POST"])
def log_energy():
    message = ""
    if request.method == "POST":
        kwh = float(request.form.get("kwh", 0))
        cost = kwh * 0.15  # Example cost calculation ($0.15 per kWh)
        
        # Use DatabaseManager to insert log
        with db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO energy_logs (timestamp, kwh_used, cost) VALUES (datetime('now'), ?, ?)", (kwh, cost))
            conn.commit()
            
        tip = ai_coach.generate_coach_tips(kwh)
        message = f"Logged {kwh} kWh successfully! AI Tip: {tip}"

    return f"""
    <h2>Log Energy Consumption</h2>
    <form method="POST">
        <label>Enter kWh Used:</label><br>
        <input type="text" name="kwh" required><br><br>
        <button type="submit">Submit Log</button>
    </form>
    <p style="color: green;"><b>{message}</b></p>
    <br><a href="/">Back to Home</a>
    """

@app.route("/report")
def download_report():
    # Generate a report using our ReportGenerator class
    report_gen = ReportGenerator("sustainability_report.pdf")
    tip = ai_coach.generate_coach_tips(20.0)  # Sample default consumption
    report_gen.create_pdf_report("Average daily consumption: 20 kWh", tip)
    
    return send_file("sustainability_report.pdf", as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)