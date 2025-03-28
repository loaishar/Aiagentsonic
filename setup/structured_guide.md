# OpenManus Fix Guide

This guide will help you resolve the issues with your OpenManus implementation.

## 1. Fix Token Limit Issue

The error `Token limit error (from RetryError): Request may exceed input token limit (Current: 0, Needed: 1966, Max: 0)` indicates your token limit configuration is incorrect.

### Fix:
1. Edit your `config/config.toml` file
2. Ensure the following settings:
   ```toml
   [llm]
   max_tokens = 4096
   max_input_tokens = 8192  # This was likely set to 0
   ```

## 2. Fix Browser Tool Initialization

The error `Browser action 'web_search' failed: 'Browser' object has no attribute 'start'` indicates an issue with the browser-use library.

### Method 1: Fix the Browser Tool Implementation
1. Locate `app/tool/browser_use_tool.py` in your project
2. Find the `_ensure_browser_initialized` method
3. Change:
   ```python
   self.browser = BrowserUseBrowser(BrowserConfig(**browser_config_kwargs))
   ```
   
   To:
   ```python
   self.browser = BrowserUseBrowser.create(BrowserConfig(**browser_config_kwargs))
   ```

### Method 2: Use a Dummy Browser Tool (Temporary Solution)
1. Create a new file at `app/tool/dummy_browser_tool.py` (use the provided script)
2. In `app/agent/manus.py`, import the dummy tool:
   ```python
   from app.tool.dummy_browser_tool import DummyBrowserTool
   ```
3. Replace the BrowserUseTool with DummyBrowserTool:
   ```python
   available_tools: ToolCollection = Field(
       default_factory=lambda: ToolCollection(
           PythonExecute(), DummyBrowserTool(), StrReplaceEditor(), Terminate()
       )
   )
   ```

## 3. Check Directory Structure

Ensure the following directory structure is intact:

```
/
├── app/
│   ├── agent/
│   │   └── manus.py
│   ├── tool/
│   │   ├── browser_use_tool.py
│   │   └── [other tool files]
│   ├── config.py
│   └── llm.py
├── config/
│   └── config.toml
└── main.py
```

## 4. Update browser-use Library

Your browser-use library may be outdated:

```bash
pip install browser-use==0.1.40 --upgrade
```

## 5. Running OpenManus

After applying these fixes, run OpenManus using:

```bash
python main.py
```

When prompted for input, start with a simple task like:
- "Tell me about the weather in New York today"
- "Generate a simple Python calculator"

## Troubleshooting Additional Issues

If you continue to experience issues:

1. **Check Logs**: Look at the logs directory for detailed error messages
2. **Verify Browser Installation**: Run `playwright install` again
3. **Check Python Version**: Consider downgrading to Python 3.12 if issues persist
4. **Re-run Verification**: Use `python verify_installation.py` after making changes

## Extended Fix for Browser Tool

If you want to dig deeper into fixing the browser-use tool:

1. Check the version of browser-use:
   ```bash
   pip show browser-use
   ```

2. Investigate the browser-use documentation:
   ```
   https://docs.browser-use.com/
   ```

3. Consider other alternatives:
   - Use PythonExecute tool instead
   - Add a simple web_search tool that uses requests to fetch information
