from flask import Flask, jsonify, render_template
from config import Config
from database import db
from routes import energy_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    app.register_blueprint(energy_bp)

    @app.get("/")
    def home():
        return render_template("index.html")

    @app.get("/health")
    def health():
        return jsonify({"status": "ok", "application": "Smart Energy Management API"})

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
