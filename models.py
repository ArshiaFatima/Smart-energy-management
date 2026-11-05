from datetime import datetime, timezone
from database import db

class EnergyReading(db.Model):
    __tablename__ = "energy_readings"
    id = db.Column(db.Integer, primary_key=True)
    meter_id = db.Column(db.String(50), nullable=False, index=True)
    device_type = db.Column(db.String(80), nullable=False)
    power_kw = db.Column(db.Float, nullable=False)
    energy_kwh = db.Column(db.Float, nullable=False)
    active = db.Column(db.Boolean, nullable=False, default=True)
    recorded_at = db.Column(db.DateTime, nullable=False,
        default=lambda: datetime.now(timezone.utc).replace(tzinfo=None))

    def to_dict(self):
        return {
            "id": self.id, "meter_id": self.meter_id,
            "device_type": self.device_type, "power_kw": self.power_kw,
            "energy_kwh": self.energy_kwh, "active": self.active,
            "recorded_at": self.recorded_at.isoformat()
        }
