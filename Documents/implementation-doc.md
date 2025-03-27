# OpenManus Implementation Guide

## Overview

OpenManus is an open-source framework for building general AI agents, enabling developers to create versatile AI assistants that can execute complex tasks through planning, tool usage, and multi-agent coordination. This document provides a comprehensive guide to understanding, setting up, and extending the OpenManus framework.

## Project Architecture

### Core Components

1. **Agents**
   - `BaseAgent`: Abstract base class for all agents
   - `ReActAgent`: Implements the ReAct pattern (Reasoning and Acting)
   - `ToolCallAgent`: Extends ReAct to handle structured tool calls
   - `CoTAgent`: Chain of Thought agent for reasoning-focused tasks
   - `PlanningAgent`: Agent with planning capabilities
   - `BrowserAgent`: Specialized for web browsing automation
   - `SWEAgent`: Software engineering agent for coding tasks
   - `MCPAgent`: Connects to Model Context Protocol servers
   - `Manus`: The main versatile agent that combines multiple capabilities

2. **Tools**
   - `BaseTool`: Abstract base class for all tools
   - `Bash`: Terminal command execution
   - `BrowserUseTool`: Web browser automation
   - `FileOperators`: File manipulation (reading/writing)
   - `PythonExecute`: Python code execution
   - `StrReplaceEditor`: Text editing operations
   - `PlanningTool`: Plan creation and management
   - `WebSearch`: Web search functionality
   - `Terminate`: Session termination
   - `ToolCollection`: Container for managing multiple tools

3. **Flow**
   - `BaseFlow`: Framework for multi-agent coordination
   - `PlanningFlow`: Implementation for planning-based workflows
   - `FlowFactory`: Factory for creating flow instances

4. **Support Systems**
   - `LLM`: Interface to language models
   - `Memory`: Conversation history management
   - `Sandbox`: Containerized execution environment
   - `Config`: Configuration management

### Interaction Flows

1. **Standard Agent Operation**
   ```
   User Input → Agent Processing → Tool Selection → Tool Execution → Result Interpretation → Response
   ```

2. **Multi-Agent Flow**
   ```
   User Input → Planning → Task Distribution → Agent Execution → Result Aggregation → Response
   ```

3. **MCP Operation**
   ```
   User Input → MCP Agent → Tool Discovery → Remote Tool Execution → Response
   ```

## Setup Guide

### Environment Setup

1. **Python Environment**

   OpenManus requires Python 3.11-3.13. We recommend using Python 3.12 for optimal compatibility.

   ```bash
   # Method 1: Using conda
   conda create -n open_manus python=3.12
   conda activate open_manus

   # Method 2: Using uv (recommended)
   curl -LsSf https://astral.sh/uv/install.sh | sh
   uv venv --python 3.12
   source .venv/bin/activate  # On Unix/macOS
   # OR
   # .venv\Scripts\activate  # On Windows
   ```

2. **Install Dependencies**

   ```bash
   # Using pip
   pip install -r requirements.txt
   
   # OR using uv (faster)
   uv pip install -r requirements.txt
   
   # Optional: Install browser automation tool
   playwright install
   ```

3. **Directory Structure**

   Ensure these directories exist:
   ```bash
   mkdir -p logs workspace
   ```

### Configuration

1. **LLM Configuration**

   Create a configuration file based on the example:
   ```bash
   cp config/config.example.toml config/config.toml
   ```

   Edit `config/config.toml` with your API details:
   ```toml
   [llm]
   model = "claude-3-7-sonnet-20250219"        # Change as needed
   base_url = "https://api.anthropic.com/v1/"  # Change based on provider
   api_key = "YOUR_API_KEY"                    # Replace with actual key
   max_tokens = 8192
   temperature = 0.0
   ```

2. **Optional Configurations**

   The following components can be configured in the same file:
   - Browser automation settings
   - Proxy settings
   - Search engine preferences
   - Sandbox execution environment

## Running OpenManus

OpenManus provides several execution modes:

1. **Standard Mode**
   ```bash
   python main.py
   ```
   This runs the core Manus agent, which can handle a wide range of tasks using all available tools.

2. **MCP Tool Version**
   ```bash
   python run_mcp.py
   ```
   This runs the Model Context Protocol agent, which can connect to MCP servers for extended functionality.

3. **Multi-Agent Flow**
   ```bash
   python run_flow.py
   ```
   This runs the planning-based multi-agent workflow, distributing tasks among specialized agents.

## Extension Guide

### Adding a New Tool

1. Create a new tool class that inherits from `BaseTool`:
   ```python
   from app.tool.base import BaseTool, ToolResult

   class MyNewTool(BaseTool):
       name: str = "my_new_tool"
       description: str = "Description of what your tool does"
       parameters: dict = {
           "type": "object",
           "properties": {
               "param1": {
                   "type": "string",
                   "description": "Description of parameter 1",
               },
               # Add more parameters as needed
           },
           "required": ["param1"],
       }

       async def execute(self, param1: str, **kwargs) -> ToolResult:
           # Implement your tool logic here
           result = # ... your implementation
           return ToolResult(output=result)
   ```

2. Register your tool with an agent:
   ```python
   from app.agent.toolcall import ToolCallAgent
   from app.tool import ToolCollection
   from my_module import MyNewTool

   # Create agent with the new tool
   my_agent = ToolCallAgent(
       available_tools=ToolCollection(MyNewTool(), Terminate())
   )
   ```

### Creating a Custom Agent

1. Create a new agent class that inherits from an appropriate base:
   ```python
   from app.agent.toolcall import ToolCallAgent
   from app.prompt.custom import SYSTEM_PROMPT, NEXT_STEP_PROMPT

   class MyCustomAgent(ToolCallAgent):
       name: str = "my_custom_agent"
       description: str = "Description of your agent's capabilities"

       system_prompt: str = SYSTEM_PROMPT
       next_step_prompt: str = NEXT_STEP_PROMPT

       # Override methods as needed
       async def think(self) -> bool:
           # Custom thinking logic
           return await super().think()
   ```

2. Run your custom agent:
   ```python
   agent = MyCustomAgent()
   await agent.run("Your task prompt here")
   ```

## Best Practices

1. **Tool Design**
   - Keep tools focused on a single responsibility
   - Provide clear descriptions and parameter documentation
   - Handle errors gracefully and return informative messages
   - Consider whether to use sandbox execution for potentially risky operations

2. **Agent Design**
   - Define clear prompts that guide the model's behavior
   - Implement proper error handling and recovery mechanisms
   - Consider memory management for long conversations
   - Use appropriate base classes based on your needs

3. **Performance Optimization**
   - Use asynchronous execution for I/O-bound operations
   - Implement proper resource cleanup
   - Consider token usage when making multiple LLM calls
   - Use streaming responses for real-time feedback

## Testing

1. **Unit Testing**
   - Test individual tools and agents in isolation
   - Mock external dependencies (LLM calls, browser operations)
   - Verify correct behavior under various inputs

2. **Integration Testing**
   - Test complete workflows combining multiple components
   - Verify correct interaction between agents and tools
   - Test error handling and recovery

3. **System Testing**
   - Test the system as a whole with real LLM backends
   - Verify end-to-end task completion
   - Measure performance and resource usage

## Troubleshooting

### Common Issues

1. **LLM Configuration Problems**
   - Verify API keys are correct
   - Check model names match provider's offerings
   - Ensure base URLs are correctly formatted

2. **Browser Automation Issues**
   - Run `playwright install` to ensure browsers are available
   - Check browser configuration settings
   - Consider disabling headless mode for debugging

3. **Sandbox Execution Errors**
   - Verify Docker is installed and running
   - Check sandbox configuration settings
   - Ensure working directory has appropriate permissions

4. **Tool Execution Failures**
   - Review tool error messages in logs
   - Check parameter formatting and types
   - Verify external dependencies are available

## Security Considerations

1. **API Key Management**
   - Store API keys securely, never commit them to version control
   - Consider using environment variables or a secure vault

2. **Sandbox Isolation**
   - Enable sandbox for untrusted code execution
   - Configure appropriate resource limits

3. **Browser Security**
   - Be cautious when navigating to unknown websites
   - Consider using isolated browser profiles

4. **Input Validation**
   - Validate and sanitize user inputs
   - Be cautious with dynamic code execution

## Conclusion

OpenManus provides a flexible framework for building AI agents with diverse capabilities. By understanding its architecture and following the implementation guidelines in this document, you can effectively leverage and extend the framework to build powerful AI assistants tailored to your specific needs.

## References

- [GitHub Repository](https://github.com/mannaandpoem/OpenManus)
- [API Documentation](https://github.com/mannaandpoem/OpenManus/docs) (if available)
- [Model Context Protocol](https://github.com/mcp-dev/mcp)