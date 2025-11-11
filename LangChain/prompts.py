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

from langchain_core.prompts import PromptTemplate
from langchain_google_genai import GoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser

#llm = GoogleGenerativeAI(model="gemini-1.5-pro")

# First chain generates a story
story_prompt = PromptTemplate.from_template("Write a short story about {topic}")
story_chain = story_prompt | openai_llm | StrOutputParser()

# Second chain analyzes the story
analysis_prompt = PromptTemplate.from_template(
    "Analyze the following story's mood:\n{story}"
)
analysis_chain = analysis_prompt | openai_llm | StrOutputParser()

# Combine chains
story_with_analysis = story_chain | analysis_chain

# Run the combined chain
story_analysis = story_with_analysis.invoke({"topic": "a rainy day"})
print("\nAnalysis:", story_analysis)

# LLMs and prompts

from langchain_core.prompts import PromptTemplate
from langchain_google_genai import GoogleGenerativeAI

# Create a template with variables
template = """
Summarize this text in one sentence:

{text}
"""
llm = GoogleGenerativeAI(model="gemini-1.5-pro")

prompt = PromptTemplate.from_template(template)

# Format the prompt with actual values
formatted_prompt = prompt.format(text="Some long story about AI...")

# Use with any LLM, such as the one created in the LLM section
result = openai_llm.invoke(formatted_prompt)
print(result)

# Chat models and prompts

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

template = ChatPromptTemplate.from_messages([
    ("system", "You are an English to French translator."),
    ("user", "Translate this to French: {text}")
])

formatted_messages = template.format_messages(text="Hello, how are you?")
result = openai_llm.invoke(formatted_messages)
print(result.content)