## Agent Framework: High-Level Architectural Overview

The agent framework is designed with a modular architecture, built upon clearly defined [Design Principles](#design-principles). Its core components and their interactions facilitate the creation, management, and execution of agent-based workflows. For definitions of key terms, please refer to the [Glossary](#glossary).

### Glossary

-   **Agent**: An autonomous entity within the framework responsible for executing specific tasks. Agents receive a `TaskSpec`, process it, and return an `AgentResponse` that includes output data and generated `Artifacts`.
-   **Task**: A discrete unit of work within a workflow, defined by a `TaskSpec`. Tasks are assigned to agents and can have dependencies on other tasks.
-   **Workflow**: A predefined sequence or graph of interconnected tasks that achieve a larger objective. Workflows are executed by the `Orchestrator`.
-   **Artifact**: A piece of data, such as a file, report, or structured output, produced or consumed by an agent during task execution. Artifacts are managed by the `ArtifactManager` and associated with a `Session`.
-   **Session**: Represents a single execution run of a workflow. It tracks the workflow's lifecycle, including start/end times, status, logs, and all associated artifacts.

### Design Principles

The agent framework is built upon several core design principles to ensure its robustness, flexibility, and maintainability:

-   **Modularity**: Components are designed to be independent and self-contained, allowing for easier development, testing, and replacement.
-   **Extensibility**: The framework is designed to be easily extended, enabling the addition of new agents, LLM providers, and workflow types without significant modifications to existing code.
-   **Separation of Concerns**: Each module and class has a clear, single responsibility, reducing complexity and improving code clarity.
-   **Configuration-Driven**: Key aspects of the framework, such as LLM providers and agent specifications, are configurable, promoting adaptability and reducing hard-coding.
-   **State Management**: Workflow and session states are explicitly managed through dedicated components, providing clear visibility and control over execution.
-   **Type Safety**: Utilizing Pydantic models for core data structures ensures data consistency and validation across the system.

### 1. Initialization and Configuration (`bootstrap.py`, `config.py`, `logger.py`, `paths.py`)

-   `bootstrap.py`: Orchestrates the initial setup of the entire system. It ensures directories are created (`paths.py`), logging is configured (`logger.py`), configuration settings are loaded (`config.py`), LLM clients are initialized (`llms/client.py`), the agent registry is populated (`agents/registry.py`), and the session manager is started (`session_manager.py`).
-   `config.py`: Manages application settings, including API keys, endpoints, and logging levels, typically loaded from environment variables or a `.env` file.
-   `logger.py`: Sets up a comprehensive logging system with different handlers for console output (colored) and file storage (standard and JSON formats).
-   `paths.py`: Provides utility functions for path manipulation, including locating the project root directory and ensuring directories exist.

### 2. Agent Management (`agents/` directory, `agent_loader.py`, `agents/registry.py`, `agents/factory.py`)

-   `agent_loader.py`: Responsible for discovering and parsing agent specifications (e.g., from YAML or JSON files) into structured `AgentSpec` models.
-   `agents/registry.py`: Acts as a central registry for both agent specifications and their corresponding Python class implementations. It loads specs via `agent_loader` and registers concrete agent classes (like `DummyAgent`).
-   `agents/factory.py`: A factory pattern implementation used to create instances of agent classes. It queries the `AgentRegistry` to find the appropriate agent class based on a given name.
-   `agents/base.py`: Defines the abstract base class (`Agent`) that all concrete agents must inherit from, specifying the core `run` method signature.

### 3. Workflow Execution (`orchestrator.py`, `task_manager.py`, `task_dependencies.py`, `workflow/` directory)

-   `orchestrator.py`: The heart of the execution engine. It receives a list of tasks, uses `task_dependencies` to sort them topologically, and then dispatches each task to an agent created by the `AgentFactory`. It manages task status updates and error handling during execution.
-   `task_manager.py`: Implements a `TaskQueue` to hold tasks, manage their states (pending, in_progress, completed, failed), and provide them to the `Orchestrator` in the correct order.
-   `task_dependencies.py`: Contains logic for validating task dependencies, including detecting circular dependencies and performing topological sorting to determine the correct execution order.
-   `workflow/planner.py`: Responsible for generating and validating the execution plan (the ordered list of tasks).
-   `workflow/state.py`: Manages the overall state of the workflow execution (e.g., RUNNING, COMPLETED, FAILED) using a state machine pattern.

### 4. Session and Artifact Management (`session_manager.py`, `artifacts.py`)

-   `session_manager.py`: Manages the lifecycle of an individual workflow execution session. It tracks session start/end times, status, logs, and associated artifacts. It coordinates with `artifact_manager` for storage.
-   `artifacts.py`: Handles the persistence and retrieval of artifacts generated by agents. It defines a directory structure for storing these artifacts, often organized by session ID.

### 5. LLM Integration (`llms/` directory)

-   `llms/client.py`: Initializes and provides access to various LLM providers configured in `config.py` (e.g., Gemini, Ollama, Kimi, Mistral).
-   `llms/provider.py`: Defines the abstract interface (`LLMProvider`) that all specific LLM integrations must adhere to, primarily the `generate` method.
-   `llms/gemini.py`, `llms/ollama.py`, etc.: Concrete implementations of `LLMProvider` for different LLM services.

### 6. Supporting Utilities (`context.py`, `error_handling.py`, `file_io.py`, `prompt_manager.py`, `prompt_templates.py`, `response_parser.py`, `models.py`)

-   `context.py`: Manages the execution context, including environment variables and runtime flags.
-   `error_handling.py`: Provides decorators for exception handling and retry logic.
-   `file_io.py`: Basic file read/write utilities.
-   `prompt_manager.py`: Loads and provides access to prompt templates.
-   `prompt_templates.py`: Handles rendering of prompt templates, potentially using Jinja2.
-   `response_parser.py`: Parses agent responses, attempting to deserialize JSON or falling back to plain text.
-   `models.py`: Defines the core data structures (Pydantic models) used throughout the system (e.g., `AgentSpec`, `TaskSpec`, `Artifact`, `AgentResponse`).

### Key Interaction Flows:

1.  **Workflow Execution**: This flow outlines the primary lifecycle of how a workflow is initiated and processed within the framework.
    -   `main.py` serves as the application's entry point, initiating the system.
    -   `bootstrap_system()` (from `bootstrap.py`) performs essential setup, ensuring configurations are loaded, logging is ready, and core components like LLM clients and the agent registry are initialized.
    -   `cli.py` parses user commands, typically including the specification of a workflow to be executed.
    -   `workflow_loader.load_workflow_from_file()` reads the workflow definition (e.g., from a YAML file) and translates it into a structured list of `TaskSpec` objects.
    -   `Orchestrator.run_workflow()` takes this list of tasks. It first uses `task_dependencies` to sort tasks topologically, ensuring that prerequisites are met before a task is attempted.
    -   The `Orchestrator` then iterates through the sorted tasks, dispatching each to an agent. This involves:
        -   Retrieving the appropriate agent class from `agents/registry.AgentRegistry`.
        -   Instantiating the agent via `agents/factory.AgentFactory`.
        -   Calling the agent's `run` method with the `TaskSpec`.
    -   During agent execution, `session_manager.add_artifact()` and `session_manager.add_log_entry()` are used to record outputs and significant events, associating them with the current session.
    -   The `workflow/state.WorkflowStateMachine` continuously updates the overall workflow status (e.g., from `RUNNING` to `COMPLETED` or `FAILED`) based on task outcomes.

2.  **Agent Loading**: This flow describes how agent specifications are discovered, loaded, and made available for instantiation.
    -   `bootstrap.py` initiates this process by calling `agents/registry.AgentRegistry._load_initial_agent_specs()`.
    -   This method, in turn, utilizes `agent_loader.load_agent_specs()`.
    -   `agent_loader.load_agent_specs()` scans a predefined directory (e.g., `agents/specs`) for agent definition files (YAML, JSON). It parses these files into `AgentSpec` models, validating their structure.
    -   The `AgentRegistry` then registers these `AgentSpec` objects and also registers concrete Python agent classes (like `DummyAgent`) that implement the `Agent` base class. This centralizes all agent-related metadata and implementations.

3.  **LLM Interaction**: This flow details how the framework integrates with and utilizes Large Language Models.
    -   The `Orchestrator` or individual agents, when they require LLM capabilities, interact with `llms.client.llm_client`.
    -   They call `llms.client.llm_client.get_provider(name: str)` to retrieve an initialized instance of a specific LLM provider (e.g., 'gemini', 'ollama'), based on configurations in `config.py`.
    -   The retrieved LLM provider (an instance of a class implementing `llms/provider.py::LLMProvider`) exposes a `generate(prompt: str)` method.
    -   The agent or orchestrator then calls this `generate` method with a constructed prompt, receiving the LLM's text response.
    -   The `bootstrap.py` module plays a crucial role by calling `llm_client._initialize_providers()` early in the system startup, ensuring that all configured LLM providers are ready for use.

## `models.py` - Core Data Structures

### Purpose

The `src/models.py` module defines the fundamental data structures used throughout the agent framework. These structures, implemented using Pydantic models, ensure data consistency and validation across different components.

### Core Components

The `models.py` module primarily consists of Pydantic classes that serve as data transfer objects (DTOs) and define the schema for various entities within the framework.

### Key Models (Core Components)

-   `AgentSpec`: Represents the specification for an agent, including its `name`, `role`, and a brief `description`.
-   `TaskSpec`: Defines a single task within a workflow. It includes a unique `id`, `name`, `description`, the `agent_name` responsible for executing it, any `input_data` required, and a list of `dependencies` (other task IDs it relies on).
-   `Artifact`: Represents a piece of data produced or consumed by an agent. It has a `name`, `type` (e.g., 'text/plain', 'application/json'), and the actual `data`.
-   `Session`: Encapsulates the state and results of a single workflow execution run. It includes a unique `id`, `start_time`, optional `end_time`, overall `status`, a list of `logs`, and a list of generated `artifacts`.
-   `ExecutionContext`: Holds the runtime context for an operation, such as the `session_id`, environment variables (`env_vars`), and other runtime flags (`runtime_flags`).
-   `AgentResponse`: Represents the output returned by an agent after executing a task. It includes a `status` (e.g., 'completed', 'failed'), any processed `output` data, and a list of `artifacts` produced.

### Interactions

These models are central to data exchange and validation across almost all components of the framework, including:
-   `agent_loader.py` (parsing `AgentSpec`)
-   `orchestrator.py` and `task_manager.py` (handling `TaskSpec` and `AgentResponse`)
-   `session_manager.py` and `artifacts.py` (managing `Session` and `Artifact` objects)
-   LLM integrations (potentially using `AgentResponse` for structured outputs).

They provide a standardized way to represent and exchange information between different parts of the agent framework, ensuring type safety and clarity.

# Configuration (`config.py`)

### Purpose

The `config.py` module is responsible for managing the application's configuration settings. It utilizes the `pydantic-settings` library to load settings from environment variables and a `.env` file, providing a robust and flexible way to configure the agent framework.

### Core Components

The core of this module is the `Settings` class, which inherits from `pydantic_settings.BaseSettings`. This class defines the structure and types of all configuration parameters.

#### Key Configuration Parameters

-   **Application Settings**:
    -   `APP_NAME`: (str) The name of the application. Defaults to "AgentFramework".
    -   `LOG_LEVEL`: (str) The minimum severity level for log messages to be processed. Defaults to "INFO". Supported levels include DEBUG, INFO, WARNING, ERROR, CRITICAL.
    -   `PROMPTS_DIR`: (str) The directory where prompt templates are stored. Defaults to "prompts".
    -   `ARTIFACTS_DIR`: (str) The directory where generated artifacts are stored. Defaults to "artifacts".

-   **LLM Settings**: These settings configure the connection details and API keys for various Large Language Model (LLM) providers.
    -   `GEMINI_API_KEY`: (Optional[str]) API key for the Gemini LLM. If not provided, the Gemini provider may not be initialized.
    -   `GEMINI_ENDPOINT`: (str) The API endpoint URL for Gemini. Defaults to "https://api.gemini.com/v1".
    -   `OLLAMA_HOST`: (str) The host address for the Ollama service. Defaults to "http://localhost:11434".
    -   `KIMI_API_KEY`: (Optional[str]) API key for the Kimi LLM. If not provided, the Kimi provider may not be initialized.
    -   `KIMI_ENDPOINT`: (str) The API endpoint URL for Kimi. Defaults to "https://api.kimi.ai/v1".
    -   `MISTRAL_API_KEY`: (Optional[str]) API key for the Mistral LLM. If not provided, the Mistral provider may not be initialized.
    -   `MISTRAL_ENDPOINT`: (str) The API endpoint URL for Mistral. Defaults to "https://api.mistral.ai/v1".
    -   `ACTIVE_LLM_PROVIDERS`: (str) A comma-separated string specifying which LLM providers should be activated. Example: "gemini,ollama".

### Loading Configuration (Key Methods/Mechanism)

Configuration is loaded automatically when the `Settings` class is instantiated, typically during system bootstrap. It prioritizes environment variables over values defined in a `.env` file, which in turn overrides the default values set in the class.

```json
{
  "APP_NAME": "AgentFramework",
  "LOG_LEVEL": "INFO",
  "PROMPTS_DIR": "prompts",
  "ARTIFACTS_DIR": "artifacts",
  "GEMINI_API_KEY": null,
  "GEMINI_ENDPOINT": "https://api.gemini.com/v1",
  "OLLAMA_HOST": "http://localhost:11434",
  "KIMI_API_KEY": null,
  "KIMI_ENDPOINT": "https://api.kimi.ai/v1",
  "MISTRAL_API_KEY": null,
  "MISTRAL_ENDPOINT": "https://api.mistral.ai/v1",
  "ACTIVE_LLM_PROVIDERS": "gemini"
}
```

*Note: The actual values for API keys and endpoints will depend on your environment setup.*

### Interactions

The `config.py` module is a foundational component that is implicitly or explicitly used by almost all other modules requiring application-wide settings.
-   `bootstrap.py`: Initiates the loading of configurations at system startup.
-   `logger.py`: Uses `settings.LOG_LEVEL` to configure logging verbosity.
-   `paths.py`: May use directory settings like `PROMPTS_DIR` and `ARTIFACTS_DIR`.
-   `llms/client.py`: Uses various `_API_KEY` and `_ENDPOINT` settings to initialize LLM providers.

### Usage

An instance of the `Settings` class, named `settings`, is exported and can be imported and used throughout the application to access configuration values.

```python
# Example usage in another module:
from src.config import settings

print(f"Application Name: {settings.APP_NAME}")
if settings.GEMINI_API_KEY:
    print("Gemini API key is configured.")
```

## `logger.py`: Logging Setup and Configuration

### Purpose

The `logger.py` module is responsible for establishing and configuring the application's logging system. It ensures that logs are captured, formatted, and directed to appropriate destinations, such as the console and log files.

### Core Components

-   `ColoredFormatter`: Extends `logging.Formatter` to add color-coding to log messages based on their severity level (e.g., red for ERROR, yellow for WARNING, green for INFO).
-   `JsonFormatter`: Extends `logging.Formatter` to format log records as JSON objects, useful for structured logging and analysis.

### Key Methods

-   `ColoredFormatter.format(record)`: Overrides the base `format` method to prepend ANSI escape codes for colors before the standard log message and reset them afterward.
-   `JsonFormatter.format(record)`: Overrides the base `format` method to create a dictionary representation of the log record and then serializes it into a JSON string.
-   `setup_logging()`: The main function that orchestrates the entire logging setup. It retrieves the desired log level from `settings.LOG_LEVEL`, ensures the log directory (`logs/`) exists, and configures handlers for console output (using `ColoredFormatter`) and file output (`app.log` with standard format and `app.json` with `JsonFormatter`). All configured handlers are added to the root logger.

### Interactions

-   `config.py`: The `setup_logging()` function retrieves the desired `LOG_LEVEL` from `settings.LOG_LEVEL`.
-   `bootstrap.py`: `setup_logging()` is called early in the application's lifecycle, typically within `bootstrap.py`, to ensure that all subsequent logging messages from any module are captured and processed according to this configuration.

### Usage

The `setup_logging()` function is invoked once during application initialization. After this setup, any module can use Python's standard `logging` module to emit log messages, and they will be processed by the configured handlers.

```python
# Example usage in another module after setup_logging() has been called:
import logging

logger = logging.getLogger(__name__)

logger.info("This is an informational message.")
logger.warning("This is a warning message.")
logger.error("This is an error message.")
```

## Module: src/artifacts.py

### Purpose

The `artifacts.py` module is responsible for managing the lifecycle of artifacts generated during workflow execution. This includes storing artifacts to disk, retrieving them when needed, and potentially providing mechanisms for contextualization based on previously generated artifacts.

### Core Components

The central class in this module is `ArtifactManager`, which handles the file-based persistence of artifacts.

### Key Methods of `ArtifactManager`

-   **`__init__(self, artifact_dir: str = 'artifacts')`**:
    -   Initializes the `ArtifactManager` with an optional `artifact_dir` argument, which defaults to `'artifacts'` relative to the project root.
    -   Ensures that this directory exists upon instantiation, creating it if necessary.
-   **`store_artifact(self, artifact: Artifact, session_id: str)`**:
    -   Takes an `Artifact` object and a `session_id` as input.
    -   Constructs a file path for the artifact, typically organized within a subdirectory named after the `session_id` inside the main artifact directory (e.g., `artifacts/<session_id>/<artifact_name>`).
    -   Ensures the target directory for the artifact exists.
    -   Writes the artifact's data to the specified file path (converts data to string using `str(artifact.data)`).
-   **`retrieve_artifact(self, name: str, session_id: str) -> Optional[Artifact]`**:
    -   Takes the artifact's `name` and `session_id` to locate the file on disk.
    -   If the artifact file exists, it reads the content using `read_file`.
    -   It then constructs and returns an `Artifact` object.
    -   Returns `None` if the artifact file is not found.
-   **`get_contextual_artifacts(self, session_id: str) -> Dict[str, Artifact]`**:
    -   This method is intended to provide artifacts that can be used for contextualizing future agent tasks.
    -   Currently, it's a placeholder that returns an empty dictionary.

### Interactions

-   The `ArtifactManager` is typically used by the `SessionManager` to store and retrieve artifacts associated with a specific session.
-   It relies on `src.file_io` for underlying file read/write operations and `src.paths` for directory management.
-   The `Artifact` model from `src.models` defines the structure of artifacts being managed.

### Usage

A singleton instance, `artifact_manager`, is created and exported for use throughout the application. It is primarily interacted with by the `SessionManager`.

```python
# Example usage within SessionManager (conceptual)
from src.artifacts import artifact_manager
from src.models import Artifact

# ...
# In a session management context
# artifact_manager.store_artifact(my_artifact, current_session_id)
# retrieved_artifact = artifact_manager.retrieve_artifact("my_artifact_name", current_session_id)
# ...
```

## Documentation for `session_manager.py`

### Purpose

The `session_manager.py` module is responsible for managing the lifecycle of individual workflow execution sessions. It tracks session start and end times, maintains the session's status, and persists logs and artifacts generated during the session.

### Core Components

The primary class within this module is `SessionManager`, which orchestrates session lifecycle, state management, log persistence, and artifact management.

### Key Methods of `SessionManager`

-   **`start_session(self) -> Session`**: Initializes a new session with a unique UUID, sets the start time, initializes the status to `WorkflowState.INIT`, and associates it with the `workflow_state_machine`. It returns the newly created `Session` object.
-   **`end_session(self, status: WorkflowState)`**: Marks the current session as ended by setting the `end_time` and updating the session's status to the provided `WorkflowState`. It also logs the session end and resets the `_current_session` attribute.
-   **`add_log_entry(self, entry: str)`**: Appends a given log string to the `logs` list of the current session.
-   **`add_artifact(self, artifact: Artifact)`**: Adds an `Artifact` object to the session's artifact list and calls `artifact_manager.store_artifact` to save the artifact to disk, organizing it by session ID.
-   **`get_current_session(self) -> Optional[Session]`**: Returns the currently active `Session` object, or `None` if no session is active.

### Interactions

-   `WorkflowStateMachine`: The `SessionManager` updates the state machine when starting and ending sessions, ensuring consistency between the session's status and the overall workflow state.
-   `ArtifactManager`: The `SessionManager` delegates the actual storage of artifacts to the `ArtifactManager`.
-   `uuid`: Used to generate unique identifiers for each session.
-   `datetime`: Used to timestamp session start and end times.
-   `logging`: Used for logging information related to session management activities.
-   `src.models.Session`: The `Session` model defines the data structure for a session managed by this module.

### Usage Example

```python
# In orchestrator.py or main execution flow:
from src.session_manager import session_manager
from src.workflow.state import WorkflowState
from src.models import Artifact
import logging

logger = logging.getLogger(__name__)

# Start a new session
session = session_manager.start_session()
logger.info(f"Starting workflow for session: {session.id}")

# During task execution, an agent might produce artifacts
# response = agent.run(task)
# if response.artifacts:
#     for artifact in response.artifacts:
#         session_manager.add_artifact(artifact)
#         logger.info(f"Stored artifact: {artifact.name}")

# Add a log entry
session_manager.add_log_entry(f"Task completed successfully.")

# At the end of the workflow, end the session
session_manager.end_session(status=WorkflowState.COMPLETED)
```

This module ensures that each run of the agent framework is properly tracked and its outputs are managed within the context of a specific session.

## LLM Integration Documentation

### Purpose

The agent framework supports integration with various Large Language Models (LLMs) through a modular provider-based system. This allows for flexibility in choosing and configuring different LLM services.

### Core Components

-   `llms/provider.py`: Defines the abstract base class `LLMProvider`, which establishes the contract for all LLM providers.
-   `llms/client.py`: The `LLMClient` class acts as a central manager for LLM providers, initializing them and providing access.
-   Specific Provider Implementations (`llms/gemini.py`, `llms/ollama.py`, `llms/kimi.py`, `llms/mistral.py`): Concrete implementations of `LLMProvider` for different LLM services.

### Key Methods

-   **`LLMProvider.generate(prompt: str) -> str`**: (Abstract method) Responsible for sending a prompt to the specific LLM and returning its text response. Each concrete provider implements this method.
-   **`LLMClient.get_provider(name: str) -> Optional[LLMProvider]`**: Allows other parts of the system to retrieve an initialized `LLMProvider` instance by its name (e.g., 'gemini', 'ollama').
-   **`LLMClient._initialize_providers(self)`**: (Internal method) Initializes available providers based on the `ACTIVE_LLM_PROVIDERS` setting in `config.py`, dynamically instantiating specific provider classes.

### Interactions

-   `config.py`: Centralizes all configuration, including API keys, endpoints, and the list of active LLM providers (`ACTIVE_LLM_PROVIDERS`), which `LLMClient` uses during initialization.
-   `bootstrap.py`: During system initialization, `bootstrap_system()` calls `llm_client._initialize_providers()` to ensure that the configured LLM clients are ready for use.
-   `Orchestrator` or specific agents: These components leverage LLMs by obtaining a provider instance from `LLMClient` and calling its `generate` method.

### Usage

Agents within the framework can leverage LLMs by obtaining an LLM provider instance from the `LLMClient`, calling the `generate` method with a specific prompt, and processing the returned text response.

```python
# Example usage within an agent:
from src.llms.client import llm_client
from src.models import TaskSpec, AgentResponse

class MyAgent:
    def run(self, task: TaskSpec) -> AgentResponse:
        llm_provider = llm_client.get_provider("gemini") # Or other configured LLM
        if llm_provider:
            prompt = f"Process the following task: {task.description}"
            response_text = llm_provider.generate(prompt)
            return AgentResponse(status="completed", output=response_text)
        else:
            return AgentResponse(status="failed", output="LLM provider not available.")

```

## Agent Package Documentation

### Purpose

This package is central to the framework's ability to define, manage, and instantiate agent functionalities, allowing for modular and extensible agent-based workflows.

### Core Components

-   **`Agent` Abstract Base Class (`src/agents/base.py`)**: The foundational class that all concrete agent implementations must inherit from.
-   **`agent_loader.py`**: Responsible for discovering and parsing agent specifications into structured `AgentSpec` models.
-   **`AgentRegistry` (`src/agents/registry.py`)**: A central hub for managing agent specifications and their corresponding Python class implementations.
-   **`AgentFactory` (`src/agents/factory.py`)**: Provides a mechanism for creating agent instances based on their registered names.
-   **`DummyAgent` (`src/agents/dummy_agent.py`)**: A basic implementation of the `Agent` base class for testing and demonstration.

### Key Methods

-   **`Agent.run(self, task: TaskSpec) -> AgentResponse`**: (Abstract method) Must be implemented by subclasses. It takes a `TaskSpec` as input, processes it, and returns an `AgentResponse` detailing the outcome, output data, and artifacts.
-   **`agent_loader.load_agent_specs(spec_dir: str = "agents/specs") -> List[AgentSpec]`**: Scans a directory for agent specification files (`.yaml`, `.yml`, or `.json`), validates them, and returns a list of `AgentSpec` objects.
-   **`AgentRegistry.register_agent_class(self, agent_class: Type[Agent])`**: Registers a concrete agent class, mapping its class name to the class itself.
-   **`AgentRegistry.get_agent_class(self, name: str) -> Optional[Type[Agent]]`**: Retrieves an agent class by its registered name.
-   **`AgentRegistry.get_agent_spec(self, name: str) -> Optional[AgentSpec]`**: Retrieves an agent specification by its name.
-   **`AgentFactory.create_agent(self, agent_name: str) -> Agent`**: Looks up the `AgentSpec` and corresponding class in the `AgentRegistry`, then instantiates and returns the agent object.

### Interactions

-   **Initialization (`bootstrap.py`)**: During system bootstrap, the `AgentRegistry` is populated with agent specifications loaded from files (`agent_loader.py`), and known concrete agent classes are registered (`registry.py`).
-   **Task Execution (`Orchestrator`)**: When the `Orchestrator` needs to execute a task, it uses the `AgentFactory` to create an agent instance. The `AgentFactory` queries the `AgentRegistry` to find the correct agent class based on the `agent_name` in the `TaskSpec`.

### Usage

New agents can be easily added by defining their specifications in YAML/JSON files and implementing the `Agent` base class.

```python
# Example: Creating and running an agent
from src.agents.factory import AgentFactory
from src.models import TaskSpec

# Assuming an agent named "my_agent" is registered
agent_instance = AgentFactory().create_agent("my_agent")
task = TaskSpec(id="1", name="sample_task", description="Perform a sample operation.", agent_name="my_agent")
response = agent_instance.run(task)
print(f"Agent response status: {response.status}")
```

### Module: src/prompt_manager.py

### Purpose

The `PromptManager` class is responsible for handling the loading, storage, and retrieval of prompt templates within the agent framework. It ensures that prompts are readily available for use by agents during their operations.

### Core Components

The primary component is the `PromptManager` class itself, which maintains an in-memory dictionary of loaded prompt templates.

### Key Methods of `PromptManager`

-   **`__init__(self, prompt_dir: Optional[str] = None)`**:
    -   Initializes a directory for prompt storage (defaulting to `settings.PROMPTS_DIR` or a specified path).
    -   Automatically calls `load_prompts()` to populate the initial set of prompts.
-   **`load_prompts(self)`**:
    -   Scans the `prompt_dir` for `.txt` files.
    -   Each filename (without extension) is treated as a prompt name, and its content becomes the prompt's template.
    -   Stores loaded prompts in the `self.prompts` dictionary.
-   **`get_prompt(self, name: str) -> str`**:
    -   Allows retrieval of a specific prompt template by its name.
    -   Returns an empty string if the prompt is not found.
-   **`update_prompt(self, name: str, new_content: str)`**:
    -   Enables dynamic updating of prompt templates in memory.

### Interactions

-   `config.py`: Uses `settings.PROMPTS_DIR` to determine the default location for prompt template files.
-   `bootstrap.py`: Typically instantiates `PromptManager` once during system bootstrap.
-   Agents and other modules: Access prompt content through the singleton `prompt_manager` instance.

### Usage

The `PromptManager` is typically instantiated once during system bootstrap and made available globally. Other modules or agents can then access prompt content through this singleton instance.

```python
# Example usage in an agent or another module:
from src.prompt_manager import prompt_manager

# Get a prompt by name
my_prompt_template = prompt_manager.get_prompt("my_agent_instruction_prompt")

if my_prompt_template:
    # Use the template, e.g., with f-strings or a templating engine
    formatted_prompt = f"Given the context: {context_data}, {my_prompt_template}"
    print(formatted_prompt)
else:
    print("Prompt not found.")
```

## `src/bootstrap.py` Module Documentation

### Purpose

The `bootstrap.py` module is responsible for initializing and configuring the entire agent framework system upon application startup. It orchestrates a sequence of setup operations to ensure all necessary components are ready before the main application logic begins execution.

### Core Components

The primary core component is the `bootstrap_system()` function itself, which acts as the orchestrator for the initial setup steps.

### Key Methods

-   **`bootstrap_system()`**: This is the primary function within the module. It executes a series of steps in a defined order to set up the system:
    1.  **Configuration Loading**: Ensures application settings are loaded (implicitly via `src.config.settings`).
    2.  **Path Management**: Verifies and creates essential directories such as `logs`, `artifacts`, `prompts`, and `agents/specs` using utilities from `src.paths`.
    3.  **Logging Setup**: Configures the application-wide logging system by calling `src.logger.setup_logging()`.
    4.  **LLM Client Initialization**: Initializes the Large Language Model client, preparing it to interact with configured LLM providers by calling `src.llms.client.llm_client._initialize_providers()`.
    5.  **Agent Registry Population**: Loads agent specifications from their defined locations into the agent registry using `src.agents.registry.agent_registry._load_initial_agent_specs()`.
    6.  **Session Management Initialization**: Starts the initial session management process via `src.session_manager.session_manager.start_session()`.

### Interactions

The `bootstrap.py` module interacts with many other core modules to perform its initialization duties:
-   `src.config`: For loading application settings.
-   `src.paths`: For directory management.
-   `src.logger`: For setting up the logging system.
-   `src.llms.client`: For initializing LLM providers.
-   `src.agents.registry`: For populating the agent registry.
-   `src.session_manager`: For starting the initial session.

### Usage

The `bootstrap_system()` function is typically called once at the very beginning of the application's execution (e.g., from `main.py`) to prepare the environment.

```python
# Example in main.py:
from src.bootstrap import bootstrap_system
import logging

if __name__ == "__main__":
    bootstrap_system()
    logger = logging.getLogger(__name__)
    logger.info("System successfully bootstrapped. Starting application logic...")
    # ... rest of the application logic
```

## Workflow Package Documentation

### Purpose

The `workflow` package is central to managing the execution flow of agent tasks. It provides the essential logic for defining the order of operations and tracking the progress of an agent-based workflow.

### Core Components

-   **`workflow/planner.py`**: This module is responsible for generating and validating the execution plan for a workflow, ensuring tasks can be executed in a logical order, respecting their dependencies.
-   **`workflow/state.py`**: This module manages the overall state of the workflow execution using a state machine pattern, tracking whether the workflow is initializing, running, completed, or has failed.
    -   `WorkflowState` (Enum): Defines the possible states a workflow can be in: `INIT`, `RUNNING`, `COMPLETED`, `FAILED`.

### Key Methods

-   **`WorkflowPlanner.generate_plan(self, tasks: List[TaskSpec]) -> List[TaskSpec]`**: Takes a list of `TaskSpec` objects and returns a topologically sorted list, representing the execution order. It raises a `ValueError` if circular dependencies are detected.
-   **`WorkflowPlanner.validate_plan(self, plan: List[TaskSpec]) -> bool`**: Validates an existing execution plan.
-   **`WorkflowStateMachine(initial_state: WorkflowState = WorkflowState.INIT)`**: Initializes the state machine with a starting state.
-   **`WorkflowStateMachine.set_session(self, session: Session)`**: Associates the state machine with a `Session` object, allowing it to update the session's status.
-   **`WorkflowStateMachine.transition_to(self, new_state: WorkflowState)`**: Changes the current state of the workflow to the `new_state`, also updating the associated session's status if one is set.
-   **`WorkflowStateMachine.get_state(self) -> WorkflowState`**: Returns the current state of the workflow.

### Interactions

-   `Orchestrator`: Utilizes `WorkflowPlanner` to get the execution plan and `WorkflowStateMachine` to manage and update the overall state of the workflow execution.
-   `session_manager`: `WorkflowStateMachine` interacts with `Session` objects managed by the `session_manager` to synchronize status.
-   `task_dependencies`: The `WorkflowPlanner` relies on `task_dependencies` for sorting tasks and detecting circular dependencies.

### Usage

The `WorkflowPlanner` is used early in the workflow execution process to determine the order of tasks, while the `WorkflowStateMachine` provides continuous visibility into the workflow's overall status throughout its lifecycle.

```python
# Example of WorkflowPlanner usage (conceptual)
from src.workflow.planner import WorkflowPlanner
from src.models import TaskSpec

tasks_to_plan = [
    TaskSpec(id="task_a", name="Task A", agent_name="agent_1"),
    TaskSpec(id="task_b", name="Task B", agent_name="agent_2", dependencies=["task_a"]),
]
planner = WorkflowPlanner()
planned_tasks = planner.generate_plan(tasks_to_plan)
print(f"Planned execution order: {[task.id for task in planned_tasks]}")

# Example of WorkflowStateMachine usage (conceptual)
from src.workflow.state import WorkflowStateMachine, WorkflowState
from src.session_manager import Session

state_machine = WorkflowStateMachine()
# session = Session(...) # Assume a session is created
# state_machine.set_session(session)
state_machine.transition_to(WorkflowState.RUNNING)
print(f"Current workflow state: {state_machine.get_state()}")
```

## Orchestrator Module Documentation (`orchestrator.py`)

### Purpose

The `Orchestrator` class is the central component responsible for managing and executing agent-based workflows. It orchestrates the flow of tasks, dispatches them to appropriate agents, and handles the overall workflow state.

### Core Components

The primary component is the `Orchestrator` class, which encapsulates the logic for workflow execution.

### Key Methods

-   **`run_workflow(self, tasks: List[TaskSpec])`**: This method initiates and manages the entire workflow process. It takes a list of `TaskSpec` objects, validates and sorts them based on their dependencies, and then processes them sequentially.
    -   **Task Dispatching**: For each task, it uses the `AgentFactory` to create an instance of the specified agent, then calls the agent's `run` method with the task details.
    -   **State Management**: Interacts with the `WorkflowStateMachine` to transition the workflow through different states (e.g., RUNNING, COMPLETED, FAILED).
    -   **Error Handling**: Catches exceptions during task execution or dependency resolution, marking the task as 'failed' and transitioning the workflow state to `FAILED`, halting execution.

### Interactions

-   `AgentFactory`: Used to instantiate agent objects based on task specifications.
-   `task_manager.task_queue`: Tasks are added to this queue after being sorted by dependencies. The orchestrator retrieves tasks from this queue.
-   `task_dependencies`: Utilized for validating task dependencies, detecting cycles, and performing topological sorting.
-   `session_manager`: Records logs and artifacts associated with the current workflow session.
-   `workflow_state_machine`: Manages and updates the overall state of the workflow execution.

### Usage (Workflow Lifecycle)

The `run_workflow` method defines the complete lifecycle of a workflow execution:

1.  **Initialization**: The method begins by setting the workflow state to `RUNNING` and populating the `task_manager.task_queue` with topologically sorted tasks.
2.  **Task Processing Loop**: The orchestrator continuously retrieves tasks from the `task_queue`.
3.  **Agent Invocation**: For each task, an agent is created and its `run` method is called.
4.  **Response Handling**: The `AgentResponse` is processed. Task status is updated, and any generated artifacts are stored via the `session_manager`.
5.  **Failure Handling**: If an agent reports failure or an exception occurs, the workflow state is set to `FAILED`, and the orchestration loop is terminated.
6.  **Completion**: If all tasks are processed successfully, the workflow state is set to `COMPLETED`.
7.  **Session Termination**: Finally, the `session_manager` is called to end the session with the determined final status.

## Task Manager (`task_manager.py`)

### Purpose

The `task_manager.py` module is responsible for managing the queue of tasks to be executed within the agent framework. It provides a centralized mechanism for adding tasks, retrieving the next available task, and updating the status of tasks as they progress through the workflow.

### Core Components

The primary component in this module is the `TaskQueue` class. It utilizes a `deque` (double-ended queue) from Python's `collections` module for efficient addition and removal of tasks.

### Key Methods of `TaskQueue`

-   **`add_task(self, task: TaskSpec)`**:
    -   Appends a given `TaskSpec` object to the internal queue.
    -   Initializes the task's status to `'pending'` in the internal status dictionary.
-   **`get_next_task(self) -> Optional[TaskSpec]`**:
    -   Removes and returns the task at the front of the queue (the next task to be processed).
    -   If the queue is empty, it returns `None`.
    -   Updates the status of the retrieved task to `'in_progress'`.
-   **`update_task_status(self, task_id: str, status: str)`**:
    -   Updates the status of a specific task, identified by its `task_id`, in the internal status dictionary.
    -   This is crucial for tracking the lifecycle of a task (e.g., from `'in_progress'` to `'completed'` or `'failed'`).
-   **`get_task_status(self, task_id: str) -> Optional[str]`**:
    -   Retrieves and returns the current status of a task based on its `task_id`.

### Interactions

-   `Orchestrator`: The `Orchestrator` is the primary consumer of the `TaskQueue`. It populates the queue with tasks (often after they have been topologically sorted) and then repeatedly calls `get_next_task()` to fetch tasks for execution.
-   `TaskSpec` (from `src.models`): The `TaskQueue` manages `TaskSpec` objects.

### Usage

The `TaskQueue` instance (`task_queue`) is typically used by the `Orchestrator` to manage the order and state of tasks throughout the workflow lifecycle.

```python
# Example usage within the Orchestrator (conceptual)
from src.task_manager import task_queue
from src.models import TaskSpec

# Assume tasks are sorted and ready
sorted_tasks = [
    TaskSpec(id="task_1", name="First Task", agent_name="agent_a"),
    TaskSpec(id="task_2", name="Second Task", agent_name="agent_b"),
]

for task in sorted_tasks:
    task_queue.add_task(task)

while True:
    next_task = task_queue.get_next_task()
    if not next_task:
        break
    print(f"Processing task: {next_task.name} (ID: {next_task.id})")
    # Simulate task execution and update status
    # agent.run(next_task)
    task_queue.update_task_status(next_task.id, "completed")

print("All tasks processed.")
```

## Contribution Guidelines

The agent framework is designed for extensibility and welcomes contributions. This section provides a high-level overview of how different components can be extended or added.

### Adding New Agents

To add a new agent to the framework:
1.  **Create an Agent Specification**: Define the agent's `AgentSpec` in a YAML or JSON file within the `agents/specs/` directory. This specification includes the agent's name, role, and description.
2.  **Implement the Agent Class**: Create a new Python class that inherits from `src/agents/base.py::Agent`. Implement the `run` method to define the agent's specific logic for processing a `TaskSpec` and returning an `AgentResponse`.
3.  **Register the Agent Class**: Ensure your new agent class is registered with the `AgentRegistry` during system bootstrap (refer to `src/agents/registry.py` for examples).

### Integrating New LLM Providers

To integrate a new Large Language Model (LLM) provider:
1.  **Implement `LLMProvider`**: Create a new Python class that inherits from `src/llms/provider.py::LLMProvider`. Implement the `generate` method to handle API calls to your new LLM service.
2.  **Configure API Keys/Endpoints**: Add relevant API keys and endpoint URLs for your new LLM provider to `src/config.py::Settings` and the `.env` file.
3.  **Update `LLMClient`**: Modify `src/llms/client.py` to initialize and manage your new LLM provider based on its configuration settings.
4.  **Activate Provider**: Add the name of your new provider to the `ACTIVE_LLM_PROVIDERS` setting in your `.env` file.

### Defining New Workflows

New workflows can be defined by creating YAML files that specify a sequence of tasks and their dependencies. These workflow definitions are loaded by `workflow_loader.load_workflow_from_file()`.

### General Contribution

For any other contributions, such as bug fixes, feature enhancements, or improvements to existing modules, please follow the standard development practices:
-   Fork the repository.
-   Create a new branch for your changes.
-   Write clear and concise commit messages.
-   Ensure existing tests pass and add new tests for your changes if applicable.
-   Submit a pull request.
