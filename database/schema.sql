CREATE DATABASE IF NOT EXISTS smart_energy_assignment3
  CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE smart_energy_assignment3;

CREATE TABLE IF NOT EXISTS energy_readings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    meter_id VARCHAR(50) NOT NULL ,  -- NOTE: Add UNIQUE after NOT NULL if you want to ensure each meter_id is unique
    device_type VARCHAR(80) NOT NULL,
    power_kw FLOAT NOT NULL,
    energy_kwh FLOAT NOT NULL,
    active BOOLEAN NOT NULL DEFAULT TRUE,
    recorded_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_meter_id (meter_id)
);

INSERT INTO energy_readings (meter_id, device_type, power_kw, energy_kwh, active)
VALUES
 ('HVAC-001', 'HVAC', 6.2, 1.4, TRUE),
 ('SOLAR-002', 'Solar Inverter', 3.5, 2.1, TRUE),
 ('BATTERY-003', 'Battery Storage', 4.0, 1.8, TRUE);
