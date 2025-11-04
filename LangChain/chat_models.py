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

response = openai_llm.invoke("Tell me a joke about light bulbs!")
print(response)

# For testing, there's the FakeListLLM

# Create a fake LLM that always returns the same responses
fake_llm = FakeListLLM(responses=["Hello"])

result = fake_llm.invoke("Any input will return Hello")
print(result)  # Output: Hello

# The default interface to work with LLMs is the Chat interface.

# specifying a model:
chat = ChatOpenAI(model="gpt-4.1", api_key=api_key,base_url = base_url)
# or:
# chat = ChatOpenAI(model='gpt-4')

# messages:
messages = [
    SystemMessage(content="You're a helpful programming assistant"),
    HumanMessage(content="Write a Python function to calculate factorial")
]
response = chat.invoke(messages)

print(response.content)