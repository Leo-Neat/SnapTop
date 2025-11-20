import vertexai
from vertexai.preview.vision_models import ImageGenerationModel
from backend.src.common.utils import get_project_name


def initialize_vertexai(project=None, location="us-central1"):
    """
    Initialize Vertex AI with the specified project and location.

    Args:
        project (str, optional): GCP project name. Defaults to get_project_name().
        location (str, optional): GCP region. Defaults to "us-central1".
    """
    if project is None:
        project = get_project_name()
    vertexai.init(project=project, location=location)


def get_imagen_fast(project=None):
    """
    Get the Imagen 3.0 Fast model for quick image generation.

    Args:
        project (str, optional): GCP project name. Defaults to get_project_name().

    Returns:
        ImageGenerationModel: Initialized Imagen model
    """
    initialize_vertexai(project=project)
    return ImageGenerationModel.from_pretrained("imagen-3.0-fast-generate-001")


def get_imagen_standard(project=None):
    """
    Get the standard Imagen 3.0 model for higher quality image generation.

    Args:
        project (str, optional): GCP project name. Defaults to get_project_name().

    Returns:
        ImageGenerationModel: Initialized Imagen model
    """
    initialize_vertexai(project=project)
    return ImageGenerationModel.from_pretrained("imagen-3.0-generate-001")
