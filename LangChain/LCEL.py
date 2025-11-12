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

# LangChain Common Expression Language (LCEL)

from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Create components
prompt = PromptTemplate.from_template("Tell me a joke about {topic}")
output_parser = StrOutputParser()

# Chain them together using LCEL
chain = prompt | openai_llm | output_parser

# Use the chain
result = chain.invoke({"topic": "programming"})
print(result)

# More complex expressions
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

# First chain generates a story
story_prompt = PromptTemplate.from_template("Write a short story about {topic}")
story_chain = story_prompt | openai_llm | StrOutputParser()

# Second chain analyzes the story
analysis_prompt = PromptTemplate.from_template("Analyze the following story's mood:\n{story}")
analysis_chain = analysis_prompt | openai_llm | StrOutputParser()

output_prompt = PromptTemplate.from_template(
    "Here's the story: \n{story}\n\nHere's the mood: \n{mood}"
)
# Combine chains
story_with_analysis = story_chain | analysis_chain

# Run the combined chain
result = story_with_analysis.invoke({"topic": "a rainy day"})
print(result)
