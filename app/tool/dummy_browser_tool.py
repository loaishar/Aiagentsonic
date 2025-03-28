"""A dummy browser tool that provides text responses instead of actual browsing."""

from typing import Any, Optional

from app.tool.base import BaseTool, ToolResult


class DummyBrowserTool(BaseTool):
    """A dummy browser tool that simulates web browsing with text responses."""

    name: str = "browser_use"
    description: str = """
    Simulates web browsing capabilities. Use this tool when you need to find information online.
    """
    parameters: dict = {
        "type": "object",
        "properties": {
            "action": {
                "type": "string",
                "enum": ["web_search", "go_to_url", "click_element", "extract_content", "open_tab", "close_tab"],
                "description": "The browser action to perform",
            },
            "url": {
                "type": "string",
                "description": "URL to navigate to",
            },
            "query": {
                "type": "string",
                "description": "Search query",
            },
            "goal": {
                "type": "string",
                "description": "Extraction goal",
            },
            "index": {
                "type": "integer",
                "description": "Element index for interactions",
            },
        },
        "required": ["action"],
    }

    async def execute(self,
                   action: str,
                   url: Optional[str] = None,
                   query: Optional[str] = None,
                   goal: Optional[str] = None,
                   index: Optional[int] = None,
                   **kwargs: Any) -> ToolResult:
        """
        Simulates browser actions and returns helpful responses.
        """
        if action == "web_search":
            query = query or kwargs.get("query", "")
            return ToolResult(output=f"""
            [Simulated Web Search for: "{query}"]

            Note: The browser functionality is currently disabled. This is a simulated response.

            Based on my knowledge, here are some results for "{query}":

            1. Popular trending products in the USA include smart home devices, wireless earbuds, fitness trackers, air fryers, and sustainable fashion items.
            2. Tech gadgets like foldable phones, VR headsets, and AI-powered devices are seeing increased popularity.
            3. Health and wellness products, including home fitness equipment and natural supplements, continue to trend upward.
            4. Eco-friendly and sustainable products are gaining significant traction across all categories.

            For more specific or up-to-date information, you might want to check websites like Amazon's trending section, TrendHunter, or Google Trends.
            """)

        elif action == "go_to_url" or action == "open_tab":
            url = url or kwargs.get("url", "")
            return ToolResult(output=f"""
            [Simulated Navigation to: "{url}"]

            Note: The browser functionality is currently disabled. This is a simulated response.

            I would normally navigate to this URL and describe the content, but currently
            I am operating with limited browsing capabilities.
            """)

        elif action == "extract_content":
            goal = goal or kwargs.get("goal", "")
            return ToolResult(output=f"""
            [Simulated Content Extraction for goal: "{goal}"]

            Note: The browser functionality is currently disabled. This is a simulated response.

            I would normally extract the relevant content based on your goal, but currently
            I am operating with limited browsing capabilities.
            """)

        else:
            return ToolResult(output=f"""
            [Simulated Browser Action: "{action}"]

            Note: The browser functionality is currently disabled. This is a simulated response.
            """)

    async def cleanup(self):
        """Clean up resources."""
        pass
