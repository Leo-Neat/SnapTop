def parse_yield_string(yield_str):
    if pd.isna(yield_str):
        return None
    s = str(yield_str).lower().strip()
    # Handle ranges like '6 to 8 - servings'
    range_match = re.match(r"(\d+)\s*(to|-)\s*(\d+)", s)
    if range_match:
        low = int(range_match.group(1))
        high = int(range_match.group(3))
        return (low + high) // 2
    # Handle '1 dozen', '2 dozen', etc.
    dozen_match = re.match(r"(\d+)\s*dozen", s)
    if dozen_match:
        return int(dozen_match.group(1)) * 12
    if "dozen" in s:
        return 12
    # Handle 'X cups', 'X pints', 'X quarts', 'X gallons', 'X pieces', 'X muffins', etc.
    num_match = re.match(r"(\d+)", s)
    if num_match:
        return int(num_match.group(1))
    # Handle 'X 9-inch pies', 'X 8-inch cakes', etc.
    multi_match = re.match(r"(\d+)\s*[a-z0-9\- ]*pie|cake|muffin|loaf|dish|pan|turnover|rose|jar|hand pie|serving|apple|crisp|bundt", s)
    if multi_match:
        return int(multi_match.group(1))
    return None

import kagglehub
import pandas as pd
import os
import re

# Download latest version
path = kagglehub.dataset_download("thedevastator/better-recipes-for-a-better-life")

print("Path to dataset files:", path)

def parse_nutrition_string(nutrition_str):
    # Regex patterns for each nutrient
    patterns = {
        "fat": r"Total Fat (\d+)g",
        "fiber": r"Dietary Fiber (\d+)g",
        "carbs": r"Total Carbohydrate (\d+)g",
        "sugars": r"Total Sugars (\d+)g",
        "protein": r"Protein (\d+)g",
        "sodium": r"Sodium (\d+)mg",
    }
    result = {}
    for key, pat in patterns.items():
        match = re.search(pat, nutrition_str)
        result[key] = int(match.group(1)) if match else None
    return result

with open(os.path.join(path, "recipes.csv"), "r") as f:
    data = pd.read_csv(f)
    important_cols = ["ingredients", "nutrition", "yield"]
    print(data[important_cols].head())
    print(data.iloc[0]['nutrition'])

    # Parse nutrition strings and add columns
    nutrition_parsed = data["nutrition"].apply(parse_nutrition_string)
    data["carbs_g"] = nutrition_parsed.apply(lambda x: x["carbs"])
    data["fat_g"] = nutrition_parsed.apply(lambda x: x["fat"])
    data["fiber_g"] = nutrition_parsed.apply(lambda x: x["fiber"])
    data["sugars_g"] = nutrition_parsed.apply(lambda x: x["sugars"])
    data["protein_g"] = nutrition_parsed.apply(lambda x: x["protein"])
    data["sodium_mg"] = nutrition_parsed.apply(lambda x: x["sodium"])

    # Calculate total calories from fat, carbs, protein
    def calc_total_calories(row):
        fat = row["fat_g"] if row["fat_g"] is not None else 0
        carbs = row["carbs_g"] if row["carbs_g"] is not None else 0
        protein = row["protein_g"] if row["protein_g"] is not None else 0
        return 9 * fat + 4 * carbs + 4 * protein

    data["calories_calc"] = data.apply(calc_total_calories, axis=1)

    print(data['yield'].unique()[:30])

    # Parse yield strings and add as int column
    data["yield_int"] = data["yield"].apply(parse_yield_string)
    label_cols = ["carbs_g", "fat_g", "fiber_g", "sugars_g", "protein_g", "sodium_mg", "calories_calc"]
    
    feature_cols = ["ingredients", "yield_int"]

    print("Filtering valid training data...")
    print("Total Training Samples:", len(data))

    valid_training_data = data.dropna(subset=label_cols + feature_cols)
    print("Total Training Samples:", len(valid_training_data))

    # Save processed recipes to the same path
    output_path = os.path.join(os.path.dirname(__file__), "../ml/recipes_processed.csv")
    output_path = os.path.abspath(output_path)
    data.to_csv(output_path, index=False)
    print(f"Processed recipes saved to: {output_path}")