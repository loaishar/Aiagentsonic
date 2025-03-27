# Getting Started with OpenManus: A Comprehensive Guide

OpenManus is an open-source framework for building general AI agents. This guide will help you set up and run the project effectively.

## Table of Contents
1. [Project Overview](#project-overview)
2. [Installation Guide](#installation-guide)
3. [Configuration Setup](#configuration-setup)
4. [Running OpenManus](#running-openManus)
5. [Available Features & Tools](#available-features--tools)
6. [Common Use Cases](#common-use-cases)
7. [Troubleshooting](#troubleshooting)

## Project Overview

OpenManus is a versatile agent framework designed to execute a wide range of tasks without requiring an invitation code. The framework includes several agent types and tools to handle tasks like:

- Web browsing and interaction
- Code execution and file manipulation
- Task planning and execution
- Multi-agent workflows

The project was developed by contributors from MetaGPT, with core authors Xinbin Liang and Jinyu Xiang.

## Installation Guide

OpenManus provides two installation methods. The second method (using `uv`) is recommended for faster installation and better dependency management.

### Method 1: Using conda

```bash
# Create a new conda environment
conda create -n open_manus python=3.12
conda activate open_manus

# Clone the repository
git clone https://github.com/mannaandpoem/OpenManus.git
cd OpenManus

# Install dependencies
pip install -r requirements.txt
```

### Method 2: Using uv (Recommended)

```bash
# Install uv (A fast Python package installer and resolver)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone the repository
git clone https://github.com/mannaandpoem/OpenManus.git
cd OpenManus

# Create a new virtual environment and activate it
uv venv --python 3.12
source .venv/bin/activate  # On Unix/macOS
# Or on Windows:
# .venv\Scripts\activate

# Install dependencies
uv pip install -r requirements.txt
```

### Browser Automation Tool (Optional)
If you need web browsing capabilities:

```bash
playwright install
```

## Configuration Setup

OpenManus requires configuration for the LLM APIs it uses:

1. Create a `config.toml` file in the `config` directory:

```bash
cp config/config.example.toml config/config.toml
```

2. Edit `config/config.toml` to add your API keys and customize settings:

```toml
# Global LLM configuration
[llm]
model = "gpt-4o"               # You can use any supported model here
base_url = "https://api.openai.com/v1"
api_key = "sk-..."             # Replace with your actual API key
max_tokens = 4096
temperature = 0.0

# Optional configuration for specific LLM models
[llm.vision]
model = "gpt-4o"
base_url = "https://api.openai.com/v1"
api_key = "sk-..."             # Replace with your actual API key
```

### Supported API Models

OpenManus supports various LLM providers:

#### OpenAI
```toml
[llm]
model = "gpt-4o"
base_url = "https://api.openai.com/v1"
api_key = "YOUR_API_KEY"
max_tokens = 8192
temperature = 0.0
```

#### Anthropic Claude
```toml
[llm]
model = "claude-3-7-sonnet-20250219"
base_url = "https://api.anthropic.com/v1/"
api_key = "YOUR_API_KEY"
max_tokens = 8192
temperature = 0.0
```

#### Azure OpenAI
```toml
[llm]
api_type = "azure"
model = "YOUR_MODEL_NAME"  # e.g., "gpt-4o-mini"
base_url = "{YOUR_AZURE_ENDPOINT.rstrip('/')}/openai/deployments/{AZURE_DEPOLYMENT_ID}"
api_key = "AZURE_API_KEY"
max_tokens = 8096
temperature = 0.0
api_version = "2024-08-01-preview"
```

#### Ollama (Local Running Models)
```toml
[llm]
api_type = "ollama"
model = "llama3.2"
base_url = "http://localhost:11434/v1"
api_key = "ollama"
max_tokens = 4096
temperature = 0.0
```

## Running OpenManus

OpenManus provides several modes to run the agent:

### Standard Mode

The simplest way to run OpenManus:

```bash
python main.py
```

Then input your query via the terminal. This runs the agent in its standard configuration.

### MCP Tool Version

For the Model Context Protocol (MCP) tool version:

```bash
python run_mcp.py
```

You can also run it with various options:

```bash
# Interactive mode
python run_mcp.py --interactive

# Single prompt execution
python run_mcp.py --prompt "Your request here"

# With server connection options
python run_mcp.py --connection sse --server-url http://127.0.0.1:8000/sse
```

### Multi-Agent Flow (Experimental)

For the unstable multi-agent version, try:

```bash
python run_flow.py
```

This runs the planning flow with multiple agents collaborating to solve complex tasks.

## Available Features & Tools

OpenManus provides a rich set of tools and capabilities:

### Main Agent Types
- **Manus**: General-purpose agent with all tools
- **CoTAgent**: Chain of Thought agent for reasoning
- **BrowserAgent**: Web browsing specialist
- **PlanningAgent**: Task planning and execution 
- **SWEAgent**: Software engineering tasks
- **MCPAgent**: Model Context Protocol agent

### Available Tools
- **browser_use**: Web browsing and interaction
- **bash**: Execute bash commands
- **python_execute**: Run Python code
- **str_replace_editor**: File manipulation
- **planning**: Create and manage task plans
- **web_search**: Perform web searches through various engines
- **terminate**: End the agent's execution

### Browser Automation Features

The `browser_use` tool provides extensive browser automation:

- Navigate to websites with `go_to_url`
- Click elements with `click_element` 
- Input text with `input_text`
- Extract content with `extract_content`
- Scroll pages with `scroll_down`, `scroll_up`, `scroll_to_text`
- Manage tabs with `switch_tab`, `open_tab`, `close_tab`

### File Manipulation

The `str_replace_editor` tool allows:

- View files/directories with `view`
- Create files with `create`
- Edit files with `str_replace`
- Insert content with `insert`
- Undo edits with `undo_edit`

## Common Use Cases

OpenManus can handle a wide variety of tasks:

1. **Research and Information Gathering**
   - Web searches for specific information
   - Extract content from multiple websites
   - Summarize findings in a structured format

2. **Software Development**
   - Write and execute Python code
   - Create and edit files
   - Test code and fix bugs

3. **Web Automation**
   - Navigate websites
   - Fill forms and interact with elements
   - Extract structured data

4. **Multi-Step Task Planning**
   - Break down complex tasks
   - Execute steps in sequence
   - Monitor progress and adjust plans

5. **Data Analysis**
   - Process data files
   - Generate visualizations
   - Draw insights from various data sources

## Troubleshooting

### Common Issues

1. **API Configuration Problems**
   - Ensure your API key is correctly entered in `config.toml`
   - Check that you're using the correct base URL for your chosen provider

2. **Dependency Issues**
   - If encountering package conflicts, try using `uv` instead of `pip`
   - Make sure you're using Python 3.11-3.13

3. **Browser Automation Failures**
   - Run `playwright install` to ensure browser dependencies are installed
   - Check browser configuration settings in `config.toml`

4. **Agent Gets Stuck**
   - Use Ctrl+C to interrupt and restart if an agent gets stuck
   - Try breaking complex tasks into smaller steps

### Environment Checks

If you're experiencing issues, verify your environment with:

```bash
# Check Python version (should be 3.11-3.13)
python --version

# Verify installed packages
pip list

# Test browser installation
python -c "from playwright.sync_api import sync_playwright; print('Playwright is working' if sync_playwright else 'Issue with Playwright')"
```

### Getting Help

If you encounter persistent issues:
- Create an issue on the [GitHub repository](https://github.com/mannaandpoem/OpenManus)
- Join the community on [Discord](https://discord.gg/DYn29wFk9z)
- Contact the developers at mannaandpoem@gmail.com

---

With this guide, you should be ready to start using OpenManus for a wide range of AI agent tasks. Enjoy exploring the capabilities of this powerful open-source framework!
