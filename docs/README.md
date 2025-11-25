# Agent Framework

## Overview

The Agent Framework is a multi-persona system designed to produce production-ready codebases through an orchestrated workflow of AI agents. It aims to automate complex software engineering tasks, from design to implementation and documentation, using a structured, iterative approach.

## High-Level Goal

To produce a production-ready codebase that implements all 40 runtime components listed in its blueprint, together with a complete, validated development pipeline and accompanying documentation.

## Features

-   **Modular Design:** Composed of independent, interchangeable components.
-   **Pydantic-based Configuration:** Robust application configuration and schema validation.
-   **Dynamic Path Management:** Flexible handling of project directories.
-   **Comprehensive Logging:** Configurable logging with custom formatters (colors, JSON).
-   **File I/O Utilities:** Safe and efficient file operations.
-   **Structured Data Models:** Pydantic models for core entities like agents, tasks, artifacts, and sessions.
-   **Prompt Management:** Centralized loading and dynamic updating of prompt templates.
-   **Agent Management:**
    -   Abstract Agent Base Class for consistent agent development.
    -   Agent Specification Loading for declarative agent definitions (YAML/JSON).
    -   Agent Discovery/Lookup and Instantiation Factory for dynamic agent usage.
-   **LLM Provider Abstraction:** Interface for seamless integration of various Large Language Models (Gemini, Ollama, Kimi, Mistral).
-   **Task & Workflow Management:**
    -   Core task management with queues and status tracking.
    -   Task Dependency Management with topological sorting and cycle detection.
    -   Workflow State Management (state machine: INIT → RUNNING → COMPLETED / FAILED).
    -   Workflow Orchestration Loop for iterative task execution.
-   **Artifact & Session Management:** Tracking, storage, retrieval, and versioning of artifacts and session data.
-   **Execution Context:** Management of environment variables, runtime flags, and current session context.
-   **Error Handling:** Robust exception wrappers and retry policies.
-   **Response Parsing:** Intelligent detection and deserialization of various response formats (JSON/plain text).
-   **Plan Generation & Validation:** Tools for orchestrators to build and validate execution plans.
-   **CLI Interface:** Command-line tools for running, initializing, and checking the status of workflows.

## Getting Started

*(Further instructions on installation, setup, and running workflows will be added here.)*

### Prerequisites

-   Python 3.9+
-   `pip` (Python package installer)

### Installation

```bash
# Clone the repository
git clone https://github.com/your-username/agent-framework.git
cd agent-framework

# Install dependencies
pip install -r requirements.txt # (requirements.txt to be generated)
```

## Project Structure

```
.
├── main.py
├── src/
│   ├── agents/
│   │   ├── base.py
│   │   ├── factory.py
│   │   └── registry.py
│   ├── artifacts.py
│   ├── bootstrap.py
│   ├── cli.py
│   ├── config.py
│   ├── context.py
│   ├── error_handling.py
│   ├── file_io.py
│   ├── llms/
│   │   ├── client.py
│   │   ├── gemini.py
│   │   ├── kimi.py
│   │   ├── mistral.py
│   │   ├── ollama.py
│   │   └── provider.py
│   ├── logger.py
│   ├── models.py
│   ├── orchestrator.py
│   ├── paths.py
│   ├── prompt_manager.py
│   ├── prompt_templates.py
│   ├── response_parser.py
│   ├── runtime.py
│   ├── task_dependencies.py
│   ├── task_manager.py
│   └── workflow/
│       ├── planner.py
│       └── state.py
├── tests/
│   ├── ... (unit test files)
├── agents/
│   └── specs/
│       └── ... (agent specification files)
├── prompts/
│   └── ... (prompt template files)
├── database/
│   ├── migration.sql
│   ├── schema.mdl
│   └── schema.sql
├── docs/
│   ├── README.md
│   ├── ARCHITECTURE.md
│   └── API.md
└── .env (example environment file)
```

## Usage

*(Detailed usage instructions for the CLI and API will be provided here.)*

## Contributing

*(Guidelines for contributing to the project.)*

## License

*(License information.)*
