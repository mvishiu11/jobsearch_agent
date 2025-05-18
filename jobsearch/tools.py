"""Custom tool functions that can be registered with CAMEL agents."""

from __future__ import annotations

from linkup import LinkupClient
from camel.toolkits import FunctionTool, SearchToolkit
from .config import LINKUP_API_KEY

client = LinkupClient(api_key=LINKUP_API_KEY)

_LINKUP_SCHEMA = {
    "type": "function",
    "function": {
        "name": "search_linkup",
        "description": "Look through web for query-relevant information.",
        "strict": True,
        "parameters": {
            "type": "object",
            "properties": {
                "query":  {"type": "string", "description": "Boolean search string"},
            },
            "required": ["query"],
            "additionalProperties": False
        }
    }
}


def _linkup(*, query: str):
    return client.search(
        query=query, depth="standard", output_type="sourcedAnswer",
    ).model_dump()


search_linkup_tool = FunctionTool(_linkup, openai_tool_schema=_LINKUP_SCHEMA)
web_search_tool = FunctionTool(SearchToolkit().search_brave)
