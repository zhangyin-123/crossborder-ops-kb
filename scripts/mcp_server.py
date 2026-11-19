"""Serve current Markdown cards over MCP stdio without a network listener."""
from typing import Literal

from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

from kb_core import read_card, search

server = FastMCP("crossborder-ops-kb")
readonly = ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=False)
Status = Literal["approved", "draft"]


@server.tool(annotations=readonly)
def search_knowledge(query: str, status: Status = "approved", limit: int = 10) -> list[dict]:
    """Search by title, tags, market or text. For review only, explicitly set status=draft."""
    return search(query, status=status, limit=limit)


@server.tool(annotations=readonly)
def read_knowledge(id: str, status: Status = "approved") -> dict:
    """Read one card by its exact ID, with its source, scope, dates and review status."""
    return read_card(id, status=status)


if __name__ == "__main__":
    server.run(transport="stdio")
