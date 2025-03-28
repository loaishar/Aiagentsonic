# Setting Up OpenManus

This guide will walk you through setting up OpenManus with all its features working correctly.

## Prerequisites

Make sure you have the following installed:
- [Python 3.11-3.13](https://www.python.org/downloads/) (Required as per the project requirements)
- [Visual Studio Code](https://code.visualstudio.com/download)
- [Git](https://git-scm.com/downloads)
- [Docker](https://www.docker.com/products/docker-desktop/) (Optional, for sandbox functionality)

## Step 1: Configure Python Environment

First, let's set up a Python virtual environment:

```bash
# Create a virtual environment
python -m venv .venv

# Activate the virtual environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

Alternatively, you can use `uv` as recommended in the README:

```bash
# Install uv if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create a virtual environment
uv venv --python 3.12

# Activate the virtual environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

# Install dependencies
uv pip install -r requirements.txt
```

## Step 2: Install Browser Automation Tool (Optional)

If you need browser automation capabilities:

```bash
pip install playwright
playwright install
```

## Step 3: Configure API Keys

The config.toml file is already set up in the config directory. If you need to modify it, you can edit it directly:

```bash
# Open the config file in VS Code
code config/config.toml
```

Make sure your API keys are correctly configured. Here's a minimal configuration:

```toml
# Global LLM configuration
[llm]
model = "gpt-4o"  # Or another model you have access to
base_url = "https://api.openai.com/v1"
api_key = "your-openai-api-key-here"
max_tokens = 4096
temperature = 0.0
```

You can use any of the supported models:
- OpenAI (default)
- Azure OpenAI
- Anthropic Claude
- Ollama (local models)
- Amazon Bedrock

## Step 4: Configure VS Code

### Install Recommended Extensions

VS Code should prompt you to install recommended extensions when you open the workspace. If not, you can manually install them:

- Even Better TOML
- Python Black Formatter
- isort

You can install these by clicking on the Extensions icon in the sidebar and searching for each one.

### VS Code Settings and Launch Configurations

The VS Code settings and launch configurations have been set up for you. You can use the following launch configurations:

- **OpenManus Main**: Runs the standard OpenManus agent interface
- **OpenManus Flow**: Runs OpenManus with the planning flow (multi-agent)
- **OpenManus MCP**: Runs OpenManus with the Model Context Protocol interface
- **OpenManus MCP Server**: Runs the MCP server
- **Verify Installation**: Runs the installation verification script

To use these configurations, press F5 in VS Code and select the desired configuration from the dropdown menu.

## Step 5: Verify Your Installation

Run the verification script to check if your installation is correctly set up:

```bash
python verify_installation.py
```

This script will check:
- Python version compatibility
- Required dependencies
- Configuration file
- Workspace directory
- Browser automation tools
- VS Code settings
- Basic component imports

## Step 6: Run the Application

Now you're ready to run OpenManus. There are several ways to run it:

### Basic Mode

```bash
python main.py
```

This will start the standard OpenManus agent interface where you can enter prompts via the terminal.

### Multi-Agent Flow Mode

```bash
python run_flow.py
```

This runs OpenManus with the planning flow, which uses multiple agents to break down and solve complex tasks.

### MCP (Model Context Protocol) Mode

```bash
python run_mcp.py
```

This uses the MCP interface for enhancing tool integration capabilities.

## Testing Your Installation

Enter a simple test prompt to ensure everything is working correctly:

```
Help me find information about the weather in New York City today
```

The agent should use its web browsing capabilities to search for the information.

## Troubleshooting

### Common Issues:

1. **API Key Issues**: Ensure your API key in `config/config.toml` is valid and has sufficient credits/quota.

2. **Import Errors**: Make sure the virtual environment is activated when running the application.

3. **Browser Tool Errors**: If you're having issues with the browser tool, make sure Playwright is installed correctly with `playwright install`.

4. **Permission Issues**: If you're getting permission errors when running scripts, you may need to adjust permissions with `chmod +x *.py` on Linux/macOS.

5. **Dependency Conflicts**: If you encounter dependency conflicts, try using `uv` instead of `pip` for installation.

## Project Structure

Understanding the project structure can help you navigate and make changes:

- `app/` - Core application code
  - `agent/` - Different agent implementations
  - `tool/` - Tools that agents can use
  - `prompt/` - Prompt templates
  - `flow/` - Multi-agent workflows
  - `sandbox/` - Docker sandbox functionality
- `config/` - Configuration files
- `tests/` - Test cases

## Next Steps

Now that your environment is set up, consider exploring:

1. The different agent types in `app/agent/`
2. Adding new tools to `app/tool/`
3. Customizing prompts in `app/prompt/`
4. Running tests to validate functionality: `pytest tests/`

Happy coding with OpenManus!
