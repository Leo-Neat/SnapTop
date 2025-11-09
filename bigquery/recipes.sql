CREATE TABLE recipes (
  recipe_id STRING NOT NULL,
  title STRING,
  description STRING,
  ingredients ARRAY<STRUCT<name STRING, quantity FLOAT64, unit STRING, notes STRING>>,
  instructions ARRAY<STRUCT<section_name STRING, steps ARRAY<STRING>>>,
  prep_time_minutes INT64,
  cook_time_minutes INT64,
  nutrition STRUCT<calories INT64, protein_grams FLOAT64, carbs_grams FLOAT64, fat_grams FLOAT64, fiber_grams FLOAT64, sugar_grams FLOAT64, sodium_mg FLOAT64>,
  servings INT64,
  serving_size STRING,
  citations ARRAY<STRING>,
  version INT64,
  created_at TIMESTAMP
);
