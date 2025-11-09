import os
from google.cloud import bigquery

# Set your GCP project ID and dataset
PROJECT_ID = os.getenv("GCP_PROJECT_ID", "recipellm")
DATASET_ID = os.getenv("BIGQUERY_DATASET", "mealprep")

SQL_FILES = {
    "users": "users.sql",
    "recipes": "recipes.sql",
    "meal_plans": "meal_plans.sql",
    "agent_logs": "agent_logs.sql",
}

SQL_DIR = os.path.dirname(os.path.abspath(__file__))


def read_sql_file(filename):
    with open(os.path.join(SQL_DIR, filename), "r") as f:
        sql = f.read().strip()
        # Extract table name from first line
        first_line = sql.splitlines()[0]
        if first_line.startswith("CREATE TABLE"):
            parts = first_line.split()
            table_name = parts[2].strip("(")
            # Replace first line with CREATE TABLE IF NOT EXISTS project.dataset.table
            new_first_line = (
                f"CREATE TABLE IF NOT EXISTS `{PROJECT_ID}.{DATASET_ID}.{table_name}` ("
            )
            sql = sql.replace(first_line, new_first_line, 1)
        return sql


def create_table_if_not_exists(client, table_name, ddl):
    print(f"Creating table {table_name} if not exists...")
    client.query(ddl).result()
    print(f"Table {table_name} checked/created.")


if __name__ == "__main__":
    client = bigquery.Client(project=PROJECT_ID)
    for name, filename in SQL_FILES.items():
        ddl = read_sql_file(filename)
        create_table_if_not_exists(client, name, ddl)
    print("All tables checked/created.")
