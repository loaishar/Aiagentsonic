# Aiagentsonic Advanced Features Integration Plan

This implementation plan focuses on integrating advanced OpenManus features into the Aiagentsonic project while following the integration guidelines in the sonicagent-guide.mdc file.

## Objectives

1. Integrate all four advanced features:
   - Multi-Agent Workflow
   - Planning and Execution Framework
   - Streaming Responses in WebSocket Interface
   - Tool Orchestration Workflow

2. Create a unified interface that maintains existing functionality
3. Ensure proper state management and error handling
4. Follow the "EXTEND, don't replace" philosophy from the integration guide

## Phase 1: Refactor Core Components (2 days)

### Task 1.1: Create a Unified Agent Controller Layer
```python
# app/controller/agent_controller.py

from typing import Dict, List, Optional, Union, Any, Callable

from app.agent.base import BaseAgent
from app.agent.manus import Manus
from app.agent.planning import PlanningAgent
from app.flow.flow_factory import FlowFactory, FlowType
from app.tool import ToolCollection
from app.logger import logger


class AgentController:
    """Centralizes agent creation and management for different modes."""
    
    MODES = {
        "standard": "Standard Manus Agent",
        "multi_agent": "Multi-Agent Workflow",
        "planning": "Planning and Execution Agent",
        "orchestration": "Tool Orchestration Workflow"
    }
    
    def __init__(self):
        self.configs = {}
        for mode in self.MODES:
            self.configs[mode] = self._load_default_config(mode)
    
    async def create_agent(self, mode: str, config: Optional[Dict[str, Any]] = None) -> Union[BaseAgent, Any]:
        """Create an agent based on the specified mode and configuration."""
        if config:
            # Merge with defaults
            merged_config = self.configs[mode].copy()
            merged_config.update(config)
            config = merged_config
        else:
            config = self.configs[mode]
            
        if mode == "standard":
            return self._create_standard_agent(config)
        elif mode == "multi_agent":
            return await self._create_multi_agent_flow(config)
        elif mode == "planning":
            return self._create_planning_agent(config)
        elif mode == "orchestration":
            return self._create_orchestration_agent(config)
        else:
            logger.warning(f"Unknown agent mode: {mode}, defaulting to standard")
            return self._create_standard_agent(self.configs["standard"])
    
    def _create_standard_agent(self, config: Dict[str, Any]) -> Manus:
        """Create a standard Manus agent."""
        return Manus(
            name=config.get("name", "Manus"),
            description=config.get("description", "A versatile agent for solving various tasks"),
            system_prompt=config.get("system_prompt", None),
            max_steps=config.get("max_steps", 20)
        )
    
    async def _create_multi_agent_flow(self, config: Dict[str, Any]) -> Any:
        """Create a multi-agent workflow."""
        # Import here to avoid circular imports
        from app.agent.cot import CoTAgent
        from app.agent.browser import BrowserAgent
        
        # Create agents based on roles
        agents = {}
        agent_roles = config.get("agent_roles", {
            "coordinator": "coordinator",
            "researcher": "researcher",
            "executor": "executor", 
            "critic": "critic"
        })
        
        for agent_name, role in agent_roles.items():
            if role == "coordinator" or role == "critic":
                agents[agent_name] = CoTAgent(
                    name=agent_name,
                    description=f"{role.capitalize()} agent"
                )
            elif role == "researcher":
                agents[agent_name] = BrowserAgent(
                    name=agent_name,
                    description=f"{role.capitalize()} agent"
                )
            else:
                agents[agent_name] = Manus(
                    name=agent_name,
                    description=f"{role.capitalize()} agent"
                )
        
        # Create and return the flow
        return FlowFactory.create_flow(
            flow_type=FlowType.MULTI_AGENT,
            agents=agents,
            agent_roles=agent_roles,
            execution_order=config.get("execution_order", list(agent_roles.keys())),
            max_iterations=config.get("max_iterations", 3)
        )
    
    def _create_planning_agent(self, config: Dict[str, Any]) -> PlanningAgent:
        """Create a planning agent with tools."""
        from app.tool import Bash, BrowserUseTool, PlanningTool
        from app.tool import PythonExecute, StrReplaceEditor, Terminate
        
        # Create tool collection based on config
        tools = ToolCollection()
        
        if config.get("use_planning_tool", True):
            tools.add_tool(PlanningTool())
        if config.get("use_bash", True):
            tools.add_tool(Bash())
        if config.get("use_browser", True):
            tools.add_tool(BrowserUseTool())
        if config.get("use_python", True):
            tools.add_tool(PythonExecute())
        if config.get("use_editor", True):
            tools.add_tool(StrReplaceEditor())
        
        tools.add_tool(Terminate())  # Always include terminate tool
        
        # Create and return planning agent
        return PlanningAgent(
            name=config.get("name", "Planning Agent"),
            description=config.get("description", "An agent that plans and executes complex tasks"),
            available_tools=tools
        )
    
    def _create_orchestration_agent(self, config: Dict[str, Any]) -> Manus:
        """Create an agent with tool orchestration capabilities."""
        from app.tool import Bash, BrowserUseTool, PythonExecute, StrReplaceEditor, Terminate
        from app.tool.orchestration import ToolOrchestration
        
        # Create tool collection
        tools = ToolCollection()
        
        if config.get("use_bash", True):
            tools.add_tool(Bash())
        if config.get("use_browser", True):
            tools.add_tool(BrowserUseTool())
        if config.get("use_python", True):
            tools.add_tool(PythonExecute())
        if config.get("use_editor", True):
            tools.add_tool(StrReplaceEditor())
        
        tools.add_tool(Terminate())  # Always include terminate tool
        
        # Create orchestration tool and add it to collection
        orchestration_tool = ToolOrchestration()
        orchestration_tool.available_tools = tools.tool_map
        tools.add_tool(orchestration_tool)
        
        # Create and return Manus agent with orchestration tools
        return Manus(
            name=config.get("name", "Orchestration Agent"),
            description=config.get("description", "An agent that can orchestrate complex workflows"),
            available_tools=tools
        )
    
    def _load_default_config(self, mode: str) -> Dict[str, Any]:
        """Load the default configuration for a mode."""
        import os
        import json
        from pathlib import Path
        
        config_dir = Path("configs") / mode
        if not config_dir.exists():
            config_dir.mkdir(parents=True, exist_ok=True)
            
        # Look for example.json in the mode directory
        example_path = config_dir / "example.json"
        if example_path.exists():
            try:
                with open(example_path, "r") as f:
                    config = json.load(f)
                    return config.get("params", {})
            except:
                pass
                
        # Return default configs if file not found or invalid
        if mode == "standard":
            return {
                "name": "Manus",
                "description": "A versatile agent for solving various tasks",
                "max_steps": 20
            }
        elif mode == "multi_agent":
            return {
                "agent_roles": {
                    "coordinator": "coordinator",
                    "researcher": "researcher",
                    "executor": "executor",
                    "critic": "critic"
                },
                "execution_order": ["coordinator", "researcher", "executor", "critic"],
                "max_iterations": 3
            }
        elif mode == "planning":
            return {
                "name": "Planning Agent",
                "description": "An agent that plans and executes complex tasks",
                "use_planning_tool": True,
                "use_bash": True,
                "use_browser": True,
                "use_python": True,
                "use_editor": True
            }
        elif mode == "orchestration":
            return {
                "name": "Orchestration Agent",
                "description": "An agent that can orchestrate complex workflows",
                "use_bash": True,
                "use_browser": True,
                "use_python": True,
                "use_editor": True
            }
        else:
            return {}
    
    def get_available_modes(self) -> List[Dict[str, str]]:
        """Get a list of available agent modes."""
        return [
            {"id": mode, "name": name}
            for mode, name in self.MODES.items()
        ]
    
    async def save_config(self, mode: str, config_id: str, config: Dict[str, Any]) -> bool:
        """Save a configuration to file."""
        import json
        from pathlib import Path
        
        try:
            config_dir = Path("configs") / mode
            config_dir.mkdir(parents=True, exist_ok=True)
            
            config_path = config_dir / f"{config_id}.json"
            with open(config_path, "w") as f:
                json.dump(config, f, indent=2)
            return True
        except Exception as e:
            logger.error(f"Error saving configuration: {e}")
            return False
    
    async def load_config(self, mode: str, config_id: str) -> Optional[Dict[str, Any]]:
        """Load a configuration from file."""
        import json
        from pathlib import Path
        
        try:
            config_path = Path("configs") / mode / f"{config_id}.json"
            if not config_path.exists():
                return None
                
            with open(config_path, "r") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading configuration: {e}")
            return None
```

### Task 1.2: Enhance Streaming Support in Base Agent

```python
# Update to app/agent/base.py

async def run_with_streaming(self, request: Optional[str] = None, stream_handler: Optional[Callable[[str], Any]] = None) -> str:
    """Execute the agent's main loop asynchronously with streaming.

    Args:
        request: Optional initial user request to process.
        stream_handler: Async function to handle streaming chunks.

    Returns:
        A string summarizing the execution results.
    """
    if self.state != AgentState.IDLE:
        logger.warning(f"Agent in {self.state} state, resetting to IDLE")
        self.state = AgentState.IDLE

    if request:
        self.update_memory("user", request)

    results: List[str] = []
    async with self.state_context(AgentState.RUNNING):
        while (
            self.current_step < self.max_steps and self.state != AgentState.FINISHED
        ):
            self.current_step += 1
            logger.info(f"Executing step {self.current_step}/{self.max_steps}")
            
            # Execute step with streaming for LLM responses
            try:
                step_result = await self.step_with_streaming(stream_handler)
                
                # Check for stuck state
                if self.is_stuck():
                    self.handle_stuck_state()

                results.append(f"Step {self.current_step}: {step_result}")
                
                # Stream step result to handler if provided
                if stream_handler and callable(stream_handler):
                    await stream_handler(f"Step {self.current_step}: {step_result}\n")
            except Exception as e:
                error_msg = f"Error in step {self.current_step}: {str(e)}"
                logger.error(error_msg)
                results.append(error_msg)
                
                # Stream error to handler if provided
                if stream_handler and callable(stream_handler):
                    await stream_handler(f"Error: {error_msg}\n")
                
                # Try to continue with next step unless agent is explicitly stopped
                if self.state == AgentState.STOPPED:
                    break

        if self.current_step >= self.max_steps and self.state != AgentState.FINISHED:
            self.current_step = 0
            self.state = AgentState.IDLE
            final_message = f"Terminated: Reached max steps ({self.max_steps})"
            results.append(final_message)
            
            # Stream final message
            if stream_handler and callable(stream_handler):
                await stream_handler(final_message)
                
    return "\n".join(results) if results else "No steps executed"
```

## Phase 2: WebSocket Integration (2 days)

### Task 2.1: Update WebSocket Handler in run_web.py

```python
# Modification to run_web.py

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    from app.agent.state import AgentState
    from app.controller.agent_controller import AgentController
    
    controller = AgentController()  # Create controller instance
    await manager.connect(websocket)
    
    try:
        while True:
            # Receive JSON data
            data = await websocket.receive_json()
            
            # Handle mode selection
            if "set_mode" in data:
                mode = data["set_mode"]
                manager.update_connection_data(websocket, "agent_mode", mode)
                await websocket.send_json({
                    "role": "system", 
                    "content": f"Agent mode set to: {mode}"
                })
                continue
                
            # Handle configuration updates
            if "update_config" in data:
                config = data["update_config"]
                connection_data = manager.get_connection_data(websocket)
                mode = connection_data.get("agent_mode", "standard")
                manager.update_connection_data(websocket, "agent_config", config)
                await websocket.send_json({
                    "role": "system", 
                    "content": f"Configuration updated for {mode} mode"
                })
                continue
            
            # Handle loading saved configurations
            if "load_config" in data:
                config_id = data["load_config"]
                connection_data = manager.get_connection_data(websocket)
                mode = connection_data.get("agent_mode", "standard")
                
                config = await controller.load_config(mode, config_id)
                if config:
                    manager.update_connection_data(websocket, "agent_config", config.get("params", {}))
                    await websocket.send_json({
                        "role": "system", 
                        "content": f"Loaded configuration: {config.get('name', config_id)}"
                    })
                else:
                    await websocket.send_json({
                        "role": "system", 
                        "content": f"Configuration not found: {config_id}"
                    })
                continue
                
            # Handle saving the current configuration
            if "save_config" in data:
                save_data = data["save_config"]
                connection_data = manager.get_connection_data(websocket)
                mode = connection_data.get("agent_mode", "standard")
                config = connection_data.get("agent_config", {})
                
                config_id = save_data.get("id")
                if not config_id:
                    await websocket.send_json({
                        "role": "system", 
                        "content": "Error: Configuration ID is required"
                    })
                    continue
                    
                config_data = {
                    "id": config_id,
                    "name": save_data.get("name", config_id),
                    "description": save_data.get("description", ""),
                    "params": config
                }
                
                if await controller.save_config(mode, config_id, config_data):
                    await websocket.send_json({
                        "role": "system", 
                        "content": f"Configuration saved: {save_data.get('name', config_id)}"
                    })
                else:
                    await websocket.send_json({
                        "role": "system", 
                        "content": "Error saving configuration"
                    })
                continue
            
            # Handle regular user prompts
            prompt = data.get("prompt", "")
            
            if prompt:
                # Send typing indicator
                await websocket.send_json({"role": "system", "content": "typing"})
                
                try:
                    # Get current agent mode and configuration
                    connection_data = manager.get_connection_data(websocket)
                    mode = connection_data.get("agent_mode", "standard")
                    config = connection_data.get("agent_config", {})
                    
                    # Create the appropriate agent using the controller
                    agent = await controller.create_agent(mode, config)
                    manager.update_connection_data(websocket, "current_agent", agent)
                    
                    # Create a streaming handler
                    async def stream_handler(chunk: str):
                        await websocket.send_json({
                            "role": "agent", 
                            "content": chunk,
                            "streaming": True,
                            "mode": mode
                        })
                    
                    # Process request based on agent mode
                    if mode == "multi_agent":
                        try:
                            # For multi-agent flow
                            result = await agent.execute(prompt)
                        except Exception as e:
                            logger.error(f"Error in multi-agent flow: {str(e)}")
                            result = f"Error processing request: {str(e)}"
                    elif hasattr(agent, "run_with_streaming") and callable(getattr(agent, "run_with_streaming")):
                        try:
                            # For agents that support streaming
                            result = await agent.run_with_streaming(prompt, stream_handler)
                        except Exception as e:
                            logger.error(f"Error in streaming execution: {str(e)}")
                            result = f"Error processing request: {str(e)}"
                    else:
                        try:
                            # Fallback to non-streaming execution
                            result = await agent.run(prompt)
                        except Exception as e:
                            logger.error(f"Error in execution: {str(e)}")
                            result = f"Error processing request: {str(e)}"
                    
                    # Send final result
                    await websocket.send_json({
                        "role": "agent", 
                        "content": result,
                        "streaming": False,
                        "final": True,
                        "mode": mode
                    })
                    
                except Exception as e:
                    logger.error(f"Error processing request: {str(e)}")
                    await websocket.send_json({
                        "role": "agent", 
                        "content": f"Error: {str(e)}",
                        "streaming": False,
                        "final": True,
                        "mode": connection_data.get("agent_mode", "standard")
                    })
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        logger.info("Client disconnected")
    except Exception as e:
        logger.error(f"WebSocket error: {str(e)}")
        manager.disconnect(websocket)
```

## Phase 3: UI Enhancements (1 day)

### Task 3.1: Update the Agent Mode Visualization Components

Update the JavaScript in the web interface to properly update visualizations based on agent mode and streaming content:

```javascript
function updateVisualization(mode, content) {
    // Update visualization based on content and mode
    if (mode === 'multi_agent') {
        // Multi-agent visualization updates
        updateMultiAgentVisualization(content);
    } else if (mode === 'planning') {
        // Planning visualization updates
        updatePlanningVisualization(content);
    } else if (mode === 'orchestration') {
        // Orchestration visualization updates
        updateOrchestrationVisualization(content);
    }
}

function updateMultiAgentVisualization(content) {
    const agentElements = {
        'coordinator': document.querySelector('.workflow-step.role-coordinator'),
        'researcher': document.querySelector('.workflow-step.role-researcher'),
        'executor': document.querySelector('.workflow-step.role-executor'),
        'critic': document.querySelector('.workflow-step.role-critic')
    };
    
    // Reset active state
    for (const key in agentElements) {
        if (agentElements[key]) {
            agentElements[key].classList.remove('active');
        }
    }
    
    // Set active agent based on content
    for (const key in agentElements) {
        if (content.toLowerCase().includes(key) && agentElements[key]) {
            agentElements[key].classList.add('active');
            
            // Mark previous agents as completed
            let markCompleted = true;
            for (const innerKey in agentElements) {
                if (innerKey === key) {
                    markCompleted = false;
                } else if (markCompleted && agentElements[innerKey]) {
                    agentElements[innerKey].classList.add('completed');
                }
            }
            break;
        }
    }
}

function updatePlanningVisualization(content) {
    // Extract plan information from content
    const planStepsElement = document.getElementById('plan-steps');
    if (!planStepsElement) return;
    
    // Look for step information in content
    const stepMatch = content.match(/Step \d+: (.+?)($|\n)/g);
    if (stepMatch) {
        // Clear existing steps
        planStepsElement.innerHTML = '';
        
        // Add steps from content
        stepMatch.forEach((step, index) => {
            const stepText = step.replace(/^Step \d+: /, '').trim();
            const stepElement = document.createElement('div');
            stepElement.className = 'd-flex align-items-center mb-1';
            
            if (index === stepMatch.length - 1) {
                // Current step
                stepElement.innerHTML = `
                    <i class="bi bi-arrow-right-circle-fill text-primary me-2"></i>
                    <span>Step ${index + 1}: ${stepText}</span>
                `;
            } else {
                // Completed step
                stepElement.innerHTML = `
                    <i class="bi bi-check-circle-fill text-success me-2"></i>
                    <span>Step ${index + 1}: ${stepText}</span>
                `;
            }
            
            planStepsElement.appendChild(stepElement);
        });
    }
}

function updateOrchestrationVisualization(content) {
    // Get all workflow steps
    const workflowSteps = document.querySelectorAll('#workflow-diagram .workflow-step');
    if (!workflowSteps || workflowSteps.length === 0) return;
    
    // Look for step status in content
    if (content.includes('Step ')) {
        // Reset steps
        workflowSteps.forEach(step => {
            step.classList.remove('active', 'completed', 'error');
        });
        
        // Try to extract current step number
        const stepMatch = content.match(/Step (\d+)[:]?/i);
        if (stepMatch && stepMatch[1]) {
            const stepNum = parseInt(stepMatch[1]);
            
            // Mark steps based on current step
            workflowSteps.forEach((step, index) => {
                if (index < stepNum - 1) {
                    step.classList.add('completed');
                } else if (index === stepNum - 1) {
                    step.classList.add('active');
                }
            });
        }
        
        // Check for errors
        if (content.toLowerCase().includes('error') || content.toLowerCase().includes('failed')) {
            const errorStepMatch = content.match(/Step (\d+)[:]? (.+?) failed/i);
            if (errorStepMatch && errorStepMatch[1]) {
                const errorStepNum = parseInt(errorStepMatch[1]);
                
                if (errorStepNum > 0 && errorStepNum <= workflowSteps.length) {
                    workflowSteps[errorStepNum - 1].classList.add('error');
                }
            }
        }
    }
}
```

## Phase 4: Configuration and API Endpoints (1 day)

### Task 4.1: Create/Update API Endpoints
```python
# API endpoints in run_web.py

@app.get("/api/modes")
async def get_agent_modes():
    """Get available agent modes"""
    controller = AgentController()
    return {"modes": controller.get_available_modes()}

@app.get("/api/configs/{mode}")
async def get_configs(mode: str):
    """Get available configurations for a mode"""
    import os
    from pathlib import Path
    
    mode_dir = Path("configs") / mode
    if not mode_dir.exists():
        return {"configs": []}
        
    configs = []
    for config_file in mode_dir.glob("*.json"):
        try:
            with open(config_file, "r") as f:
                import json
                config = json.load(f)
                configs.append({
                    "id": config_file.stem,
                    "name": config.get("name", config_file.stem),
                    "description": config.get("description", "")
                })
        except:
            pass
            
    return {"configs": configs}

@app.get("/api/config/{mode}/{config_id}")
async def get_config(mode: str, config_id: str):
    """Get a specific configuration"""
    controller = AgentController()
    config = await controller.load_config(mode, config_id)
    
    if not config:
        raise HTTPException(status_code=404, detail="Configuration not found")
        
    return config

@app.post("/api/config/{mode}")
async def save_config(mode: str, config: dict):
    """Save a configuration"""
    if "id" not in config:
        raise HTTPException(status_code=400, detail="Configuration ID is required")
        
    controller = AgentController()
    if await controller.save_config(mode, config["id"], config):
        return {"status": "success"}
    else:
        raise HTTPException(status_code=500, detail="Error saving configuration")
```

## Phase 5: Testing and Integration (2 days)

### Task 5.1: Comprehensive End-to-End Testing
Create test scripts for each agent mode to ensure proper integration:

1. Test the standard agent mode with streaming
2. Test multi-agent workflow with proper agent transitions
3. Test planning agent with plan creation and execution
4. Test tool orchestration workflow

### Task 5.2: Fix Any Integration Issues
Address any issues found during testing:

1. Resolve any state management issues
2. Fix WebSocket streaming problems
3. Ensure proper error handling and recovery
4. Optimize visualization updates

## Implementation Schedule

| Phase | Tasks | Timeline | Dependencies |
|-------|-------|----------|--------------|
| Phase 1 | Refactor Core Components | Days 1-2 | None |
| Phase 2 | WebSocket Integration | Days 3-4 | Phase 1 |
| Phase 3 | UI Enhancements | Day 5 | Phase 2 |
| Phase 4 | Configuration and API Endpoints | Day 6 | Phase 3 |
| Phase 5 | Testing and Integration | Days 7-8 | Phase 4 |

## Notes and Recommendations

1. **Code Organization**:
   - Follow the modular structure that already exists
   - Use the controller pattern to centralize agent creation and management
   - Properly handle state transitions and error recovery

2. **Performance Considerations**:
   - Use asynchronous code for all network and I/O operations
   - Implement proper cleanup for resources (especially in error cases)
   - Consider implementing logging or telemetry to track agent performance

3. **User Experience**:
   - Ensure streaming updates are smooth and don't overwhelm the UI
   - Provide clear visualizations of agent progress
   - Implement proper error messages that help users diagnose issues
