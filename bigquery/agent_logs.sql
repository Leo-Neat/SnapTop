
CREATE TABLE agent_logs (
  log_id STRING NOT NULL,
  meal_plan_id STRING,
  agent_name STRING,
  timestamp TIMESTAMP,
  action STRING,
  input STRUCT<key STRING, value STRING>,
  output STRUCT<key STRING, value STRING>,
  feedback STRING
);
