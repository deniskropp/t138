# API Reference

This document provides a high-level overview of the key classes, functions, and APIs within the Agent Framework. It's intended for developers looking to understand how to extend, configure, or interact with the system programmatically.

## Core Components

### 1. Configuration

-   **`src.config.Settings`** (Pydantic `BaseSettings`):
    -   **Purpose:** Manages application-wide configuration. Settings are loaded from `.env` files and environment variables.
    -   **Attributes:** `APP_NAME`, `LOG_LEVEL`, `PROMPTS_DIR`, `ARTIFACTS_DIR`, `GEMINI_API_KEY`, etc.
    -   **Usage:**
        ```python
        from src.config import settings
        app_name = settings.APP_NAME
        ```

### 2. Path Management

-   **`src.paths.get_root_dir() -> str`**:
    -   **Purpose:** Returns the absolute path to the project's root directory.
-   **`src.paths.ensure_dir(path: str)`**:
    -   **Purpose:** Ensures that a given directory path exists, creating it if necessary.

### 3. Logging

-   **`src.logger.setup_logging()`**:
    -   **Purpose:** Configures the application's logging system, including console (colored) and file (text, JSON) handlers based on `settings.LOG_LEVEL`.

### 4. File I/O

-   **`src.file_io.read_file(path: str, mode: str = 'r', encoding: str = 'utf-8') -> str | bytes | None`**:
    -   **Purpose:** Reads content from a file, supporting text and binary modes. Returns `None` on error.
-   **`src.file_io.write_file(path: str, content: str | bytes, mode: str = 'w', encoding: str = 'utf-8') -> bool`**:
    -   **Purpose:** Writes content to a file, supporting text and binary modes. Returns `True` on success, `False` on error.

### 5. Data Models (`src.models`)

Pydantic models defining the structure of core entities.

-   **`AgentSpec`**: `name: str`, `role: str`, `description: str`
-   **`TaskSpec`**: `id: str`, `name: str`, `description: str`, `agent_name: str`, `input_data: Dict[str, Any]`, `dependencies: List[str]`
-   **`Artifact`**: `name: str`, `type: str`, `data: Any`
-   **`Session`**: `id: str`, `start_time: str`, `end_time: Optional[str]`, `status: str`, `logs: List[str]`, `artifacts: List[Artifact]`
-   **`ExecutionContext`**: `session_id: str`, `env_vars: Dict[str, str]`, `runtime_flags: Dict[str, Any]`, `current_task_id: Optional[str]`
-   **`AgentResponse`**: `status: str`, `output: Dict[str, Any]`, `artifacts: List[Artifact]`

### 6. LLM Providers

-   **`src.llms.provider.LLMProvider`** (Abstract Base Class):
    -   **Purpose:** Defines the interface for all LLM providers.
    -   **Abstract Method:** `generate(self, prompt: str) -> str`
-   **`src.llms.gemini.GeminiLLMProvider`**, **`src.llms.ollama.OllamaLLMProvider`**, etc.:
    -   **Purpose:** Concrete implementations of `LLMProvider` for specific LLM services.
-   **`src.llms.client.LLMClient`**:
    -   **Purpose:** Manages the instantiation and retrieval of LLM provider instances.
    -   **Method:** `get_provider(self, name: str) -> Optional[LLMProvider]`

### 7. Prompt Management

-   **`src.prompt_manager.PromptManager`**:
    -   **Purpose:** Loads prompt templates from files and provides them by name.
    -   **Methods:**
        -   `load_prompts(self)`: Scans the prompts directory.
        -   `get_prompt(self, name: str) -> str`: Retrieves a template by name.
        -   `update_prompt(self, name: str, new_content: str)`: Modifies a prompt template in memory.
-   **`src.prompt_templates.load_template(path: str) -> str`**:
    -   **Purpose:** Loads a raw template string from a file.
-   **`src.prompt_templates.render_template(template_string: str, **kwargs) -> str`**:
    -   **Purpose:** Renders a Jinja2 template string with provided data.

### 8. Agent Core

-   **`src.agents.base.Agent`** (Abstract Base Class):
    -   **Purpose:** Base class for all agents.
    -   **Abstract Method:** `run(self, task: TaskSpec) -> AgentResponse`
-   **`src.agents.registry.AgentRegistry`**:
    -   **Purpose:** Stores and retrieves `AgentSpec`s and `Agent` class references.
    -   **Methods:** `_load_initial_agent_specs()`, `register_agent_class()`, `get_agent_spec()`, `get_agent_class()`, `list_agent_specs()`.
-   **`src.agents.factory.AgentFactory`**:
    -   **Purpose:** Creates concrete `Agent` instances.
    -   **Method:** `create_agent(self, agent_name: str) -> Agent`

### 9. Task & Workflow Management

-   **`src.task_manager.TaskQueue`**:
    -   **Purpose:** Manages a queue of `TaskSpec`s and their execution status.
    -   **Methods:** `add_task()`, `get_next_task()`, `update_task_status()`, `get_task_status()`.
-   **`src.task_dependencies.topological_sort(tasks: List[TaskSpec]) -> List[TaskSpec]`**:
    -   **Purpose:** Orders tasks based on dependencies, raising `ValueError` on cycles.
-   **`src.task_dependencies.detect_cycles(tasks: List[TaskSpec]) -> bool`**:
    -   **Purpose:** Detects circular dependencies within a list of tasks.
-   **`src.workflow.state.WorkflowState`** (Enum):
    -   **Purpose:** Defines possible states of a workflow (`INIT`, `RUNNING`, `COMPLETED`, `FAILED`).
-   **`src.workflow.state.WorkflowStateMachine`**:
    -   **Purpose:** Manages transitions between workflow states.
    -   **Methods:** `set_session()`, `transition_to()`, `get_state()`.
-   **`src.workflow.planner.WorkflowPlanner`**:
    -   **Purpose:** Generates and validates workflow execution plans.
    -   **Methods:** `generate_plan(tasks: List[TaskSpec]) -> List[TaskSpec]`, `validate_plan(plan: List[TaskSpec]) -> bool`.
-   **`src.orchestrator.Orchestrator`**:
    -   **Purpose:** Orchestrates the execution of a workflow.
    -   **Method:** `run_workflow(self, initial_tasks: List[TaskSpec])`

### 10. Session & Artifacts

-   **`src.session_manager.SessionManager`**:
    -   **Purpose:** Manages the lifecycle of a single workflow execution session.
    -   **Methods:** `start_session()`, `end_session()`, `add_log_entry()`, `add_artifact()`, `get_current_session()`.
-   **`src.artifacts.ArtifactManager`**:
    -   **Purpose:** Manages the storage and retrieval of `Artifact`s.
    -   **Methods:** `store_artifact()`, `retrieve_artifact()`, `get_contextual_artifacts()`.

### 11. Utility Functions

-   **`src.error_handling.handle_exception(func)`** (Decorator):
    -   **Purpose:** Logs exceptions and re-raises them (or handles as per policy).
-   **`src.error_handling.retry_policy(retries: int, delay: int)`** (Decorator):
    -   **Purpose:** Retries a function a specified number of times on failure.
-   **`src.response_parser.parse_response(response_text: str) -> Dict[str, Any]`**:
    -   **Purpose:** Parses a response string, attempting JSON deserialization first.

## Command Line Interface (`src.cli`)

The `main_cli()` function parses command-line arguments and dispatches to appropriate handlers.

-   `python main.py run <workflow_definition>`: Executes a specified workflow.
-   `python main.py init`: Initializes a new project environment.
-   `python main.py status`: Displays the current system status.

---
*(This API reference will be continually updated as the framework evolves and new features are added.)*
