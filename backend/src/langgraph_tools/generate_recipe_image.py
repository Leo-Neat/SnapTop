import base64
from langchain.tools import tool
from backend.src.common.img_generation_models import get_imagen_fast


@tool
def generate_recipe_image(recipe_description: str) -> str:
    """
    Generate an image for a recipe using Google's Imagen model.

    Args:
        recipe_description (str): A description of the recipe to generate an image for.
                                  Should be descriptive and include key visual elements.

    Returns:
        str: Base64-encoded image data (PNG format) that can be embedded in responses.

    Example:
        generate_recipe_image("A colorful pasta dish with grilled chicken, fresh spinach,
                              and cherry tomatoes on a white plate")
    """
    try:
        # Get the Imagen model
        model = get_imagen_fast()

        # Enhance the prompt for better food photography
        enhanced_prompt = f"Professional food photography of {recipe_description}, appetizing, well-lit, high quality, detailed"

        # Generate the image
        response = model.generate_images(
            prompt=enhanced_prompt,
            number_of_images=1,
            aspect_ratio="1:1",
            safety_filter_level="block_some",
            person_generation="dont_allow"
        )

        # Get the first (and only) generated image
        image = response.images[0]

        # Convert image to base64
        # The image object has a _image_bytes attribute with the raw image data
        image_bytes = image._image_bytes
        base64_image = base64.b64encode(image_bytes).decode('utf-8')

        return base64_image

    except Exception as e:
        error_msg = f"Error generating recipe image: {str(e)}"
        print(error_msg)
        raise Exception(error_msg)


if __name__ == "__main__":
    # Test the tool
    description = "Healthy chicken and spinach pasta with whole wheat penne, fresh vegetables, and a light garlic sauce"
    try:
        print(f"Generating image for: {description}")
        result = generate_recipe_image.invoke({"recipe_description": description})
        print(f"Generated image (base64 length: {len(result)} characters)")

        # Save the image to a file for testing
        output_file = "test_recipe_image.png"
        with open(output_file, "wb") as f:
            f.write(base64.b64decode(result))
        print(f"Image saved to: {output_file}")

    except Exception as e:
        print(f"Error: {e}")
