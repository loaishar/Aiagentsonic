# Browser Tool Fix

import os

def fix_browser_tool():
    """Fixes the browser_use_tool.py file."""
    print("Choose an option:")
    print("1. Fix existing browser_use_tool.py file")
    print("2. Create a temporary dummy browser tool")
    choice = input("Enter your choice (1 or 2): ")

    if choice == "1":
        fix_existing_tool()
    elif choice == "2":
        create_dummy_tool()
    else:
        print("Invalid choice.")

def fix_existing_tool():
    """Fixes the existing browser_use_tool.py file."""
    try:
        with open("app/tool/browser_use_tool.py", "r") as f:
            content = f.readlines()

        # Identify the lines to modify
        browser_use_import_line = None
        for i, line in enumerate(content):
            if "from browser_use import Browser as BrowserUseBrowser" in line:
                browser_use_import_line = i
                break

        if browser_use_import_line is None:
            print("BrowserUse import not found in browser_use_tool.py")
            return

        # Insert the new code
        content.insert(browser_use_import_line + 1, "from playwright.sync_api import sync_playwright")

        # Find the BrowserUseTool class
        browser_use_tool_class_start = None
        for i, line in enumerate(content):
            if "class BrowserUseTool(BaseTool):" in line:
                browser_use_tool_class_start = i
                break

        if browser_use_tool_class_start is None:
            print("BrowserUseTool class not found in browser_use_tool.py")
            return

        # Find the execute method
        execute_method_start = None
        for i, line in enumerate(content[browser_use_tool_class_start:]):
            if "async def _execute(self, action: str, **kwargs: Any) -> ToolResult:" in line:
                execute_method_start = browser_use_tool_class_start + i
                break

        if execute_method_start is None:
            print("execute method not found in BrowserUseTool class")
            return

        # Modify the execute method
        content.insert(execute_method_start + 1, "        with sync_playwright() as p:")
        content.insert(execute_method_start + 2, "            browser = p.chromium.launch()")
        content.insert(execute_method_start + 3, "            context = browser.new_context()")
        content.insert(execute_method_start + 4, "            page = context.new_page()")

        # Write the modified content back to the file
        with open("app/tool/browser_use_tool.py", "w") as f:
            f.writelines(content)

        print("Successfully fixed browser_use_tool.py")

    except FileNotFoundError:
        print("Error: browser_use_tool.py not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

def create_dummy_tool():
    """Creates a temporary dummy browser tool."""
    try:
        with open("app/tool/dummy_browser_tool.py", "w") as f:
            f.write('''
from app.tool.base import BaseTool, ToolResult

class DummyBrowserTool(BaseTool):
    name = "dummy_browser"
    description = "A temporary dummy browser tool that provides helpful responses without failing."

    async def _execute(self, action: str, **kwargs: Any) -> ToolResult:
        if action == "web_search":
            query = kwargs.get("query")
            return ToolResult(output=f"I am a dummy browser. I cannot search the web for '{query}'. Please try a different tool.")
        elif action == "go_to_url":
            url = kwargs.get("url")
            return ToolResult(output=f"I am a dummy browser. I cannot navigate to '{url}'. Please try a different tool.")
        else:
            return ToolResult(output="I am a dummy browser. I cannot perform this action. Please try a different tool.")
''')
        print("Successfully created dummy_browser_tool.py")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    fix_browser_tool()
