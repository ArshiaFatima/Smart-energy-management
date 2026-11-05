import sqlite3
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

class DatabaseManager:
    """Manages SQLite database connections and initialization for energy logs."""
    def __init__(self, db_path="energy_data.db"):
        self.__db_path = db_path
        self.initialize_database()

    # Getter for database path (Encapsulation)
    @property
    def db_path(self):
        return self.__db_path

    def get_connection(self):
        """Creates and returns a sqlite3 connection."""
        return sqlite3.connect(self.__db_path)

    def initialize_database(self):
        """Creates the energy usage table if it doesn't already exist."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS energy_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    kwh_used REAL NOT NULL,
                    cost REAL NOT NULL
                )
            """)
            conn.commit()


class AICoachService:
    """Provides sustainability tips and AI energy-saving recommendations."""
    def __init__(self, api_key=None):
        self.__api_key = api_key or os.getenv("OPENAI_API_KEY")

    # Getter and Setter for API key (Encapsulation)
    @property
    def api_key(self):
        return self.__api_key

    @api_key.setter
    def api_key(self, new_key):
        self.__api_key = new_key

    def generate_coach_tips(self, current_kwh):
        """Generates tailored feedback based on consumption levels (with fallback logic)."""
        if current_kwh > 25.0:
            return "High energy alert: Consider shifting heavy appliance usage to off-peak hours and checking thermostat settings."
        elif current_kwh > 15.0:
            return "Moderate usage detected. Turning off standby electronics could help optimize your daily efficiency."
        else:
            return "Great job! Your energy consumption is well-optimized today. Keep up the sustainable habits!"


class ReportGenerator:
    """Generates PDF reports for energy consumption and AI coaching summaries."""
    def __init__(self, filename="sustainability_report.pdf"):
        self.__filename = filename

    # Getter for filename (Encapsulation)
    @property
    def filename(self):
        return self.__filename

    def create_pdf_report(self, data_summary, coach_tip):
        """Uses ReportLab to generate a clean PDF summary report."""
        c = canvas.Canvas(self.__filename, pagesize=letter)
        width, height = letter

        # Title
        c.setFont("Helvetica-Bold", 18)
        c.drawString(50, height - 50, "AI Sustainability Coach & Energy Report")

        # Data Section
        c.setFont("Helvetica", 12)
        c.drawString(50, height - 90, f"Energy Summary: {data_summary}")

        # AI Coach Section
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, height - 130, "AI Coach Recommendation:")
        c.setFont("Helvetica", 11)
        c.drawString(50, height - 150, coach_tip)

        c.save()
        return self.__filename
        class Subsystem4Exception(Exception):
    """Custom base exception for Subsystem 4 errors."""
    pass


class Subsystem4ErrorHandler:
    """Centralized error-handling class for Subsystem 4 components."""
    
    @staticmethod
    def handle_database_error(error):
        """Logs or formats database-related exceptions."""
        error_msg = f"[Database Error]: {str(error)}"
        print(error_msg)
        return error_msg

    @staticmethod
    def handle_ai_error(error):
        """Logs or formats AI coach service exceptions."""
        error_msg = f"[AI Coach Error]: {str(error)}"
        print(error_msg)
        return error_msg

    @staticmethod
    def handle_report_error(error):
        """Logs or formats report generation exceptions."""
        error_msg = f"[Report Generation Error]: {str(error)}"
        print(error_msg)
        return error_msg