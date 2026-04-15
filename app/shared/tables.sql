CREATE TABLE locations (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    parent_id TEXT NULL REFERENCES locations(id) ON DELETE SET NULL
);

CREATE TABLE assets (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    location_id TEXT NULL REFERENCES locations(id) ON DELETE SET NULL,
    parent_id TEXT NULL REFERENCES assets(id) ON DELETE SET NULL
);

CREATE TABLE components (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    parent_id TEXT NULL,
    sensor_type TEXT NOT NULL,
    status TEXT NOT NULL
);

ALTER TABLE components
ADD CONSTRAINT components_sensor_type_check
CHECK (sensor_type IN ('vibration', 'energy'));

ALTER TABLE components
ADD CONSTRAINT components_status_check
CHECK (status IN ('operating', 'alert'));

CREATE TABLE readings (
    id UUID PRIMARY KEY,
    component_id TEXT NOT NULL REFERENCES components(id) ON DELETE CASCADE,
    recorded_at TIMESTAMP NOT NULL,
    value DOUBLE PRECISION NOT NULL
);

CREATE TABLE alerts (
    id UUID PRIMARY KEY,
    component_id TEXT NOT NULL REFERENCES components(id),
    reading_id UUID NOT NULL REFERENCES readings(id),
    anomaly_type TEXT NOT NULL,
    severity TEXT NOT NULL,
    occurrence_count INTEGER NOT NULL DEFAULT 1,
    message TEXT NOT NULL,
    status TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

ALTER TABLE alerts
ADD CONSTRAINT alerts_status_check
CHECK (status IN ('open', 'acknowledged', 'resolved'));

CREATE TABLE anomaly_states (
    component_id TEXT NOT NULL REFERENCES components(id),
    anomaly_type TEXT NOT NULL,
    occurrence_count INTEGER NOT NULL DEFAULT 0,
    last_reading_id UUID NOT NULL REFERENCES readings(id),
    alert_id UUID NULL REFERENCES alerts(id),
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    PRIMARY KEY (component_id, anomaly_type)
);

CREATE TABLE work_orders (
    id UUID PRIMARY KEY,
    alert_id UUID NOT NULL UNIQUE REFERENCES alerts(id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    status TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

ALTER TABLE work_orders
ADD CONSTRAINT work_orders_status_check
CHECK (status IN ('open', 'in_progress', 'done', 'canceled'));