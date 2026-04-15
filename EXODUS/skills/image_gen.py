import urllib.parse

class ImageGenSkill:
    """
    Skill for generating images via Pollinations.ai.
    """
    def __init__(self):
        self.base_url = "https://image.pollinations.ai/prompt/"

    def generate_image_url(self, prompt: str) -> str:
        """
        Creates a Pollinations.ai URL for the prompt.
        """
        encoded_prompt = urllib.parse.quote(prompt)
        # Adding some high-quality tags for better results
        full_prompt = f"{encoded_prompt}, high quality, cinematic, 8k"
        image_url = f"{self.base_url}{full_prompt}"
        
        return f"I have generated the image for you:\n\n[IMAGE_URL: {image_url}]\n\n*Note: Image generation is powered by Pollinations.ai*"
