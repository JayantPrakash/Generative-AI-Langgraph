from typing_extensions import TypedDict
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from io import BytesIO
"""
LangGraph fundamentals
Let's start with creating an agent that analyzes a provided job description 
and if it fits my profile, it generated an application. 
We'll fake the application logic itself, and work only on the flow for now:
"""
    

class JobApplicationState(TypedDict):
    job_description: str
    is_suitable: bool
    application: str

from langgraph.graph import StateGraph, START, END, Graph

def analyze_job_description(state):
    print("...Analyzing a provided job description ...")
    return {"is_suitable": len(state["job_description"]) > 100}

def generate_application(state):
    print("...generating application...")
    return {"application": "some_fake_application"}

builder = StateGraph(JobApplicationState)
builder.add_node("analyze_job_description", analyze_job_description)
builder.add_node("generate_application", generate_application)

builder.add_edge(START, "analyze_job_description")
builder.add_edge("analyze_job_description", "generate_application")
builder.add_edge("generate_application", END)

graph = builder.compile()

res = graph.invoke({"job_description":"fake_jd"})
print(res)

from IPython.display import Image, display
display(Image(graph.get_graph().draw_mermaid_png()))

png_bytes = graph.get_graph().draw_mermaid_png()
img = mpimg.imread(BytesIO(png_bytes))
plt.imshow(img)
plt.axis('off')
plt.show()

from langchain_core.runnables import Runnable
print(isinstance(graph, Runnable))

"""
Now, let's make our logic a little
bit more complex and make an edge conditional - in other words, 
our flow would depend on the previous outcomes (of an LLM):
"""

from typing import Literal

builder = StateGraph(JobApplicationState)
builder.add_node("analyze_job_description", analyze_job_description)
builder.add_node("generate_application", generate_application)

def is_suitable_condition(state: JobApplicationState) -> Literal["generate_application", END]:
    if state.get("is_suitable"):
        return "generate_application"
    return END

builder.add_edge(START, "analyze_job_description")
builder.add_conditional_edges("analyze_job_description", is_suitable_condition)
builder.add_edge("generate_application", END)

graph = builder.compile()
res = graph.invoke({"job_description":"fake_jd"})
print(res)

png_bytes = graph.get_graph().draw_mermaid_png()
img = mpimg.imread(BytesIO(png_bytes))
plt.imshow(img)
plt.axis('off')
plt.show()

"""
How we can add configuration to our graph:
"""
from langchain_core.runnables.config import RunnableConfig

class JobApplicationState(TypedDict):
    job_description: str
    is_suitable: bool
    application: str
    actions: list[str]

from typing import Literal

def is_suitable_condition(state: JobApplicationState) -> Literal["generate_application", END]:
    if state.get("is_suitable"):
        return "generate_application"
    return END

def generate_application(state: JobApplicationState, config: RunnableConfig):
    model_provider = config["configurable"].get("model_provider", "Google")
    model_name = config["configurable"].get("model_name", "gemini-2.0-flash")
    print(f"...generating application with {model_provider} and {model_name} ...")
    return {"application": "some_fake_application", "actions": ["action2", "action3"]}



builder = StateGraph(JobApplicationState)
builder.add_node("analyze_job_description", analyze_job_description)
builder.add_node("generate_application", generate_application)
builder.add_edge(START, "analyze_job_description")
builder.add_conditional_edges("analyze_job_description", is_suitable_condition)
builder.add_edge("generate_application", END)

graph = builder.compile()
res = graph.invoke({"job_description":"fake_jd"})
print(res)