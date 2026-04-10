CREATE TABLE IF NOT EXISTS devices (
  id SERIAL PRIMARY KEY,
  uid VARCHAR(128) UNIQUE NOT NULL,
  ip_address VARCHAR(64) NOT NULL,
  hostname VARCHAR(255),
  manufacturer VARCHAR(255),
  model VARCHAR(255),
  confidence DOUBLE PRECISION NOT NULL DEFAULT 0,
  metadata_json JSONB NOT NULL DEFAULT '{}'::jsonb,
  created_at TIMESTAMP NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS discovery_jobs (
  id SERIAL PRIMARY KEY,
  scope_cidr VARCHAR(64) NOT NULL,
  mode VARCHAR(32) NOT NULL DEFAULT 'safe',
  status VARCHAR(32) NOT NULL DEFAULT 'pending',
  findings_count INT NOT NULL DEFAULT 0,
  created_at TIMESTAMP NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS recommendations (
  id SERIAL PRIMARY KEY,
  device_uid VARCHAR(128) NOT NULL,
  recommendation_type VARCHAR(64) NOT NULL,
  payload JSONB NOT NULL DEFAULT '{}'::jsonb,
  confidence DOUBLE PRECISION NOT NULL DEFAULT 0,
  validator_status VARCHAR(32) NOT NULL DEFAULT 'pending',
  created_at TIMESTAMP NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS approvals (
  id SERIAL PRIMARY KEY,
  target_type VARCHAR(64) NOT NULL,
  target_id VARCHAR(128) NOT NULL,
  approved_by VARCHAR(128),
  status VARCHAR(32) NOT NULL DEFAULT 'pending',
  reason TEXT,
  created_at TIMESTAMP NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS execution_plans (
  id SERIAL PRIMARY KEY,
  plan_name VARCHAR(255) NOT NULL,
  dry_run BOOLEAN NOT NULL DEFAULT TRUE,
  status VARCHAR(32) NOT NULL DEFAULT 'pending',
  steps_json JSONB NOT NULL DEFAULT '[]'::jsonb,
  created_at TIMESTAMP NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS rollback_snapshots (
  id SERIAL PRIMARY KEY,
  plan_id INT NOT NULL REFERENCES execution_plans(id),
  snapshot_json JSONB NOT NULL DEFAULT '{}'::jsonb,
  created_at TIMESTAMP NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS audit_logs (
  id SERIAL PRIMARY KEY,
  timestamp TIMESTAMP NOT NULL DEFAULT NOW(),
  actor VARCHAR(128) NOT NULL DEFAULT 'system',
  action VARCHAR(128) NOT NULL,
  target VARCHAR(255) NOT NULL,
  details JSONB NOT NULL DEFAULT '{}'::jsonb
);
