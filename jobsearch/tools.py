"""Custom tool functions that can be registered with CAMEL agents."""

from __future__ import annotations

from linkup import LinkupClient
from typing import Any, Dict
from camel.toolkits import FunctionTool
from .config import LINKUP_API_KEY

client = LinkupClient(api_key=LINKUP_API_KEY)


def search_linkup(
    query: str
) -> Dict[str, Any]:
    """Search the web for job postings with Linkup.

    Args:
        query: The query

    Returns:
        Parsed JSON response from LinkUp.
    """

    return client.search(
        query=query,
        depth="deep",
        output_type="sourcedAnswer"
    )


search_linkup_tool = FunctionTool(search_linkup)
