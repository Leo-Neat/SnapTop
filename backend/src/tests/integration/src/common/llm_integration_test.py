import pytest
from backend.src.common.llms import get_gemini_flash, get_gemini_pro, get_gemini_flash_lite


@pytest.mark.parametrize(
    "llm_func, model_name",
    [
        (get_gemini_flash, "gemini-2.5-flash"),
        (get_gemini_pro, "gemini-2.5-pro"),
        (get_gemini_flash_lite, "gemini-2.5-flash-lite"),
    ],
)
def test_llm_hello_world(llm_func, model_name):
    llm = llm_func()
    response = llm.invoke([{"role": "user", "content": "hello world"}])
    assert response, f"No response from {model_name}"
    print(f"{model_name} response: {response}")
