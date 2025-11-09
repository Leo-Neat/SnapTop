CREATE TABLE users (
  user_id STRING NOT NULL,
  dietary_profile STRUCT<
    profiles ARRAY<STRING>,
    allergens ARRAY<STRING>
  >,
  dietary_preferences STRING,
  dietary_dislikes STRING,
  kitchen_tools ARRAY<STRING>,
  pantry ARRAY<STRUCT<name STRING, quantity FLOAT64, unit STRING, notes STRING>>,
  grocery_stores ARRAY<STRING>,
  meal_params STRUCT<
    meal_requests ARRAY<STRUCT<type STRING, recipes_per_week INT64, servings_per_recipe INT64>>,
    daily_calorie_target INT64,
    macro_targets STRUCT<carbs_percent FLOAT64, fat_percent FLOAT64, protein_percent FLOAT64>
  >
);
