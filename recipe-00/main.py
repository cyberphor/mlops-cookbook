# Stand library imports.
from dotenv import load_dotenv
from whois import whois
from typing import List

# Third party imports.
from langchain.agents import create_agent
from langchain.tools import tool
import ray

@tool
def whois_tool(url: str):
    """Resolves IP addresses to domain names and vice versa."""
    return whois(url=url)

load_dotenv()

ray.init()

@ray.remote
def run_agent(model: str, tools: List[tool] | None, system_prompt: str, content: str):
    agent = create_agent(
        model=model,
        tools=tools,
        system_prompt=system_prompt,
    )

    return agent.invoke({
        "messages": [
            {"role": "user", "content": content}
        ]
    })

models = [
    {
        "name": "gpt-4o",
        "system_prompt": "You are a helpful assistant",
        "tools": [whois_tool]
    },
    {
        "name": "gpt-4.1",
        "system_prompt": "You are a helpful assistant",
        "tools": []
    },
    {
        "name": "gpt-5",
        "system_prompt": "You are a helpful assistant",
        "tools": []
    },
]

content = "Who owns 149.132.208.123?"
def main(content: str):
    object_references = []
    for model in models:
        object_reference = run_agent.remote(model["name"], model["tools"], model["system_prompt"], content)
        object_references.append(object_reference)

    objects = ray.get(object_references)
    for object in objects:
        print(object)

def test(content: str):
    agent = create_agent(
        model=models[0]["name"],
        tools=models[0]["tools"],
        system_prompt=models[0]["system_prompt"],
    )

    print(agent.invoke({
        "messages": [
            {"role": "user", "content": content}
        ]
    }))

main(content)