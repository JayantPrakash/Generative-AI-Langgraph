import os
import sys
import importlib.util
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_community.llms import FakeListLLM

# Absolute path to config.py (adjust as needed)
config_path = "/Users/jn6878/Documents/config.py"

spec = importlib.util.spec_from_file_location("config", config_path)
config = importlib.util.module_from_spec(spec)
spec.loader.exec_module(config)

# Now you can use config.set_environment()
config.set_environment()

base_url = os.environ.get("OPEN_AI_LITE_LLM_BASE_URL")
api_key = os.environ.get("OPENAI_API_KEY")
openai_llm = ChatOpenAI(model="gpt-4.1", api_key=api_key,base_url = base_url)

"""
from langchain_community.utilities.dalle_image_generator import DallEAPIWrapper

dalle = DallEAPIWrapper(
   model="dall-e-3",  # Options: "dall-e-2" (default) or "dall-e-3"
   size="1024x1024",       # Image dimensions
    quality="standard",     # "standard" or "hd" for DALL-E 3
    n=1,
    api_key=api_key,
    base_url = base_url# Number of images to generate (only for DALL-E 2)
)
image_url = dalle.run("A detailed technical diagram of a quantum computer")
print(image_url)
"""
# Image understanding
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI

def analyze_image(image_url: str, question: str) -> str:
    # Use the configured OpenAI client with your base_url
    chat = ChatOpenAI(
        model="gpt-4o-mini", 
        max_tokens=256,
        api_key=api_key,
        base_url=base_url
    )

    message = HumanMessage(
        content=[
            {
                "type": "text",
                "text": question
            },
            {
                "type": "image_url",
                "image_url": {
                    "url": image_url,
                    "detail": "auto"
                }
            }
        ]
    )

    try:
        response = chat.invoke([message])
        # Handle both string and object responses
        if isinstance(response, str):
            return response
        elif hasattr(response, 'content'):
            return response.content
        else:
            return str(response)
    except Exception as e:
        return f"Error: {str(e)}"

# Example usage
image_url = "https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=640"
questions = [
    "What objects do you see in this image?",
    "What is the overall mood or atmosphere?",
    "Are there any people in the image?"
]

for question in questions:
    print(f"\nQ: {question}")
    print(f"A: {analyze_image(image_url, question)}")
    
"""    
# Gemini
import base64
with open("stable-diffusion.png", 'rb') as image_file:
 image_bytes = image_file.read()
 base64_bytes = base64.b64encode(image_bytes).decode("utf-8")


prompt = [
   {"type": "text", "text": "Describe the image: "},
   {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_bytes}"}},
]


llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",
    temperature=0,
)
response = llm.invoke([HumanMessage(content=prompt)])
print(response.content)    

# Using Google Cloud Storage

prompt = [
   {"type": "text", "text": "Describe the video in a few sentences."},
   {"type": "media", "file_uri": video_uri, "mime_type": "video/mp4"},
]


response = llm.invoke([HumanMessage(content=prompt)])
print(response.content)


# Image generation
from langchain_community.utilities.dalle_image_generator import DallEAPIWrapper

dalle = DallEAPIWrapper(
   model="dall-e-3",  # Options: "dall-e-2" (default) or "dall-e-3"
   size="1024x1024",       # Image dimensions
    quality="standard",     # "standard" or "hd" for DALL-E 3
    n=1                     # Number of images to generate (only for DALL-E 2)
)
image_url = dalle.run("A detailed technical diagram of a quantum computer")
print(image_url)

from langchain_community.llms import Replicate

# Initialize the text-to-image model:
text2image = Replicate(
    model="stability-ai/stable-diffusion-3.5-large",
    model_kwargs={
        "prompt_strength": 0.85,
        "cfg": 4.5,
        "steps": 40,
        "aspect_ratio": "1:1",
        "output_format": "webp",
        "output_quality": 90
    }
)


# Generate an image
image_url = text2image.invoke(
    "A detailed technical diagram of an AI agent"
)

print(image_url)

"""