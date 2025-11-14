from typing_extensions import TypedDict
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from io import BytesIO
from langgraph.graph import StateGraph, START, END, Graph

"""
Let's see how we can defined state fields that accumulate values. 
The first option is to use a default reducer that replaces the values in the state
"""
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

def analyze_job_description(state):
    print("...Analyzing a provided job description ...")
    result = {
        "is_suitable": len(state["job_description"]) < 100,
        "actions": ["action1"]}
    return result

def generate_application(state):
    print("...generating application...")
    return {"application": "some_fake_application", "actions": ["action2"]}



builder = StateGraph(JobApplicationState)
builder.add_node("analyze_job_description", analyze_job_description)
builder.add_node("generate_application", generate_application)
builder.add_edge(START, "analyze_job_description")
builder.add_conditional_edges("analyze_job_description", is_suitable_condition)
builder.add_edge("generate_application", END)

graph = builder.compile()

for chunk in graph.stream(
    input={"job_description":"fake_jd"},
    stream_mode="values"
):
    print(chunk)
    print("\n\n")

png_bytes = graph.get_graph().draw_mermaid_png()
img = mpimg.imread(BytesIO(png_bytes))
plt.imshow(img)
plt.axis('off')
plt.show()    

"""
Option 2 - use add method as a reducer:
"""

from typing import Annotated, Optional
from operator import add

class JobApplicationState(TypedDict):
    job_description: str
    is_suitable: bool
    application: str
    actions: Annotated[list[str], add]

def analyze_job_description(state):
    print("...Analyzing a provided job description ...")
    result = {
        "is_suitable": len(state["job_description"]) < 100,
        "actions": ["action1"]}
    return result

def generate_application(state):
    print("...generating application...")
    return {"application": "some_fake_application", "actions": ["action2"]}



builder = StateGraph(JobApplicationState)
builder.add_node("analyze_job_description", analyze_job_description)
builder.add_node("generate_application", generate_application)
builder.add_edge(START, "analyze_job_description")
builder.add_conditional_edges("analyze_job_description", is_suitable_condition)
builder.add_edge("generate_application", END)

graph = builder.compile()

for chunk in graph.stream(
    input={"job_description":"fake_jd"},
    stream_mode="values"
):
    print(chunk)
    print("\n\n")
    
"""
And the last option is to build your own custom reducer:
"""    

from typing import Annotated, Optional, Union
from operator import add

def my_reducer(left: list[str], right: Optional[Union[str, list[str]]]) -> list[str]:
  if right:
    return left + [right] if isinstance(right, str) else left + right
  return left


class JobApplicationState(TypedDict):
    job_description: str
    is_suitable: bool
    application: str
    actions: Annotated[list[str], my_reducer]

def analyze_job_description(state):
    print("...Analyzing a provided job description ...")
    result = {
        "is_suitable": len(state["job_description"]) < 100,
        "actions": "action1"}
    return result

def generate_application(state):
    print("...generating application...")
    return {"application": "some_fake_application", "actions": ["action2", "action3"]}



builder = StateGraph(JobApplicationState)
builder.add_node("analyze_job_description", analyze_job_description)
builder.add_node("generate_application", generate_application)
builder.add_edge(START, "analyze_job_description")
builder.add_conditional_edges("analyze_job_description", is_suitable_condition)
builder.add_edge("generate_application", END)

graph = builder.compile()
for chunk in graph.stream(
    input={"job_description":"fake_jd"},
    stream_mode="values"
):
    print(chunk)
    print("\n\n")
    
png_bytes = graph.get_graph().draw_mermaid_png()
img = mpimg.imread(BytesIO(png_bytes))
plt.imshow(img)
plt.axis('off')
plt.show()      