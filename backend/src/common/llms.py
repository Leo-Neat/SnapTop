import google.generativeai as genai
from langchain_google_vertexai import ChatVertexAI
from backend.src.common.utils import get_gcp_secret, get_project_name

genai.configure(api_key=get_gcp_secret("google-cloud-api-key", version="1"))


def get_gemini_flash(system_prompt=None, project=None):
    if project is None:
        project = get_project_name()
    return ChatVertexAI(
        model_name="gemini-2.5-flash", project=project, system_message=system_prompt
    )


def get_gemini_pro(system_prompt=None, project=None):
    if project is None:
        project = get_project_name()
    return ChatVertexAI(
        model_name="gemini-2.5-pro", project=project, system_message=system_prompt
    )


def get_gemini_flash_lite(system_prompt=None, project=None):
    if project is None:
        project = get_project_name()
    return ChatVertexAI(
        model_name="gemini-2.5-flash-lite",
        project=project,
        system_message=system_prompt,
    )
