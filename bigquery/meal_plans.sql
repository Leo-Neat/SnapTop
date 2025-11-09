CREATE TABLE meal_plans (
  meal_plan_id STRING NOT NULL,
  user_id STRING NOT NULL,
  week_start DATE,
  meals ARRAY<STRUCT<meal_type STRING, recipe_id STRING, servings INT64>>,
  created_at TIMESTAMP
);
