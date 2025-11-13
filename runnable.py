from langchain.schema.runnable import Runnable

"""Runnable: Base Class
The Runnable class serves as the foundational building block. All other specialized Runnables inherit from this class.
"""
class MyRunnable(Runnable):
    def invoke(self, input):
        return input.upper()

# Create an instance of MyRunnable
runnable = MyRunnable()

# Test with a sample input
result = runnable.invoke("hello world")
print(result)  # Output: HELLO WORLD

# Try another example
result = runnable.invoke("LangChain is awesome")
print(result)  # Output: LANGCHAIN IS AWESOME

"""
RunnableMap
Executes multiple Runnables in parallel and aggregates their results
"""
from langchain.schema.runnable import RunnableMap

runnable_map = RunnableMap({
    "uppercase": lambda x: x.upper(),
    "reverse": lambda x: x[::-1],
})

result = runnable_map.invoke("langchain")
print(result)  # Output: {'uppercase': 'LANGCHAIN', 'reverse': 'niahcnagL'}

""" 
RunnableSequence
Chains Runnables sequentially, passing the output of one as input to the next.
"""
from langchain_core.runnables import RunnableLambda

# Method 1: Using RunnableLambda and pipe operator
step1 = RunnableLambda(lambda x: x.lower())
step2 = RunnableLambda(lambda x: x[::-1])

runnable_sequence = step1 | step2

result = runnable_sequence.invoke("LangChain")
print(result)   
# Output: 'niahcgnal'

# Method 2: Direct chaining with pipe operator
runnable_sequence2 = (
    RunnableLambda(lambda x: x.lower()) 
    | RunnableLambda(lambda x: x[::-1])
    | RunnableLambda(lambda x: f"Result: {x}")
)

result2 = runnable_sequence2.invoke("LangChain")
print(result2)
# Output: 'Result: niahcgnal'

from langchain_core.runnables import RunnableLambda, RunnableSequence

def add_one(x: int) -> int:
    return x + 1

def mul_two(x: int) -> int:
    return x * 2

runnable_1 = RunnableLambda(add_one)
runnable_2 = RunnableLambda(mul_two)
#sequence = runnable_1 | runnable_2
# Or equivalently:
sequence = RunnableSequence(first=runnable_1, last=runnable_2)
result = sequence.invoke(1)
print(result)

sequence = RunnableSequence(first=step1, last=step2)
result = sequence.invoke("LangChain")
print(result)

from langchain.schema.runnable import RunnableSequence

runnable_sequence = RunnableSequence(
    RunnableLambda(lambda x: x.lower()), 
    RunnableLambda(lambda x: x[::-1])
)

result = runnable_sequence.invoke("LangChain")
# Output: 'niahcnag'
print(result)

from langchain.schema.runnable import RunnableSequence

runnable_sequence = RunnableSequence(
    lambda x: x.lower(),
    lambda x: x[::-1],
)

result = runnable_sequence.invoke("LangChain")
print(result)
# Output: 'niahcnag'

"""RunnableLambda
Wraps a simple Python function in a Runnable.
"""
from langchain.schema.runnable import RunnableLambda

uppercase_runnable = RunnableLambda(lambda x: x.upper())
result = uppercase_runnable.invoke("langchain")
# Output: 'LANGCHAIN'
print(result)

"""
Example: End-to-End Workflow
Problem Statement:
Process customer feedback, classify its sentiment, and summarize it.

Solution with Runnables:
"""
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

from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from langchain.schema.runnable import Runnable, RunnableSequence, RunnableMap,RunnableLambda

# Define individual Runnables
sentiment_analysis_runnable = RunnableLambda(lambda text: "Positive" if "good" in text.lower() else "Negative")

summarization_runnable = RunnableSequence(
    PromptTemplate(input_variables=["text"], template="Summarize this: {text}"),
    openai_llm
)

# Combine Runnables into a pipeline
pipeline = RunnableMap({
    "sentiment": sentiment_analysis_runnable,
    "summary": summarization_runnable
})

# Invoke the pipeline
feedback = "The product quality is really good and exceeded expectations."
result = pipeline.invoke(feedback)

print(result)
# Output:
# {
#   "sentiment": "Positive",
#   "summary": "The product quality is excellent."
# }


"""
RunnableParallel
Runs multiple Runnables in parallel and combines the results.

Use Case:
Optimize performance by executing tasks concurrently.
"""

from langchain.schema.runnable import RunnableParallel

parallel_tasks = RunnableParallel({
    "uppercase": lambda x: x.upper(),
    "reverse": lambda x: x[::-1],
})

result = parallel_tasks.invoke("langchain")
print(result)  # Output: {'uppercase': 'LANGCHAIN', 'reverse': 'niahcnagL'}

"""RunnableSerializable
Allows Runnables to be serialized (e.g., to save and reload them).

Use Case:
Serialize Runnables for sharing or storage.
"""
from langchain.schema.runnable import RunnableSerializable

class SerializableRunnable(RunnableSerializable):
    def invoke(self, input):
        return input.upper()

serializable = SerializableRunnable()
result = serializable.invoke("langchain")
print(result)  # Output: 'LANGCHAIN'