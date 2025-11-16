# Stand library imports.
from argparse import ArgumentParser
from dotenv import load_dotenv
from time import perf_counter
from typing import Dict, List

# Third party imports.
from langchain.agents import create_agent
from langchain.tools import tool
from ray import get, init, remote, shutdown
from whois import whois
from yaml import safe_load

whois = tool("whois")(whois)

def get_agent_profiles(yaml_file_name: str) -> List:
    with open(yaml_file_name, mode="r", encoding="UTF-8") as yaml_file:
        return safe_load(yaml_file)

def check_agent_profile(agent_profile: Dict):
    # Check agent "name" key.
    if "name" not in agent_profile:
        raise ValueError('"name" key not found in agent profile')
    
    # Check agent "name" value.
    if agent_profile.get("name") is None:
        raise ValueError('"name" key in agent profile is null')
    
    # Check "model" key.
    if "model" not in agent_profile:
        raise ValueError('"model" key not found in agent profile')
    
    # Check "model" provider value.
    if agent_profile.get("model").get("provider") is None:
        raise ValueError('"provider" key in "model" key is null')
    
    # Check "model" name value.
    if agent_profile.get("model").get("name") is None:
        raise ValueError('"name" key in "model" key is null')
    
    # Check model "system_prompt" value.
    if agent_profile.get("model").get("system_prompt") is None:
        raise ValueError('"system_prompt" key in "model" key is null')

    # Check "harness" key.
    if "harness" not in agent_profile:
        raise ValueError('"harness" key not found in agent profile')

    # Check harness "tools" value.
    if len(agent_profile.get("harness").get("tools")) < 1:
        raise ValueError('"tools" key in "harness" key is null')

def load_tools(agent_profile: Dict):
    tools = []
    for t in agent_profile["harness"]["tools"]:
        match t:
            case "whois":
                tools.append(whois)
            case _:
                raise RuntimeError(f"unknown tool: {t}")
    agent_profile["harness"]["tools"] = tools

def check_agent_profiles(agent_profiles: List[Dict]):
    for agent_profile in agent_profiles:
        check_agent_profile(agent_profile) # what does this check, profile quality?
        load_tools(agent_profile)

@remote
def run_agent(model_name: str, system_prompt: str, tools: List[tool] | None, task: str):
    return create_agent(
        model=model_name,
        tools=tools,
        system_prompt=system_prompt,
    ).invoke({
        "messages": [
            {"role": "user", "content": task}
        ]
    })

def main(file_name: str, task: str):
    """
    The main entrypoint to coach.
    """
    # Load environment variables (e.g., API keys) from a file.
    load_dotenv()

    # Load agent configurations from a file.
    agent_profiles = get_agent_profiles(yaml_file_name=file_name)
    check_agent_profiles(agent_profiles)

    # Init a Ray cluster.
    init()

    # Run each agent in parallel on the Ray cluster. 
    object_references = []
    for agent_profile in agent_profiles:
        object_reference = run_agent.remote(
            agent_profile["model"]["name"],
            agent_profile["model"]["system_prompt"],
            agent_profile["harness"]["tools"],
            task)
        object_references.append(object_reference)

    # Get the output of each agent.
    objects = get(object_references)
    for object in objects:
        print(object)

    # Shutdown the Ray cluster.
    shutdown()

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--file", type=str, default="agent-profiles.yaml")
    parser.add_argument("--task", type=str, required=True)
    args = parser.parse_args()
    start = perf_counter()
    main(file_name=args.file, task=args.task)
    end = perf_counter()
    print(f"Time: {end - start:.6f} seconds")
