# Standard library imports.
from dataclasses import dataclass, field
from typing import Any, Callable, List

# Third party imports.
from langchain.tools import tool
from pydantic import BaseModel
from whois import whois

whois = tool("whois")(whois)


class Harness(BaseModel):
    tool_names: List[str] = field(default_factory=list)
    tools: List[Callable[..., Any]] = field(default_factory=list, init=False)

    def __post_init__(self) -> None:
        if not isinstance(self.tool_names, list):
            raise ValueError('"tools" key is not a list')
        elif len(self.tool_names) < 1:
            raise ValueError('"tools" key cannot be empty')

        tools = []
        for tool_name in self.tool_names:
            match tool_name:
                case "whois":
                    tools.append(whois)
                case _:
                    raise RuntimeError(f"unknown tool: {tool_name}")
        self.tools = tools
