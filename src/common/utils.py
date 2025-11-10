from google.cloud import secretmanager
import os


def get_gcp_secret(
    secret_id: str, version: str = "latest", project_id: str = None
) -> str:
    """
    Fetch a secret value from Google Cloud Secret Manager.
    Args:
        secret_id (str): Secret name
        version (str): Secret version (default: 'latest')
        project_id (str): GCP project ID (default: env GCP_PROJECT_ID or hardcoded)
    Returns:
        str: Secret value
    """
    if not project_id:
        project_id = os.getenv("GCP_PROJECT_ID") or "171070825881"
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version}"
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")


def get_project_name() -> str:
    """
    Returns the GCP project name from the PROJECT_NAME env var, or 'recipellm' if not set.
    """
    return os.getenv("PROJECT_NAME", "recipellm")


def get_bigquery_dataset_name() -> str:
    """
    Returns the BigQuery dataset name from the BIGQUERY_DATASET env var, or 'mealprep' if not set.
    """
    return os.getenv("BIGQUERY_DATASET", "mealprep")
