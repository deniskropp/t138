# QuickStart: Getting Started with the Agent Framework

Welcome to the Agent Framework! This guide will help you set up the project, understand its core concepts, and run your first workflow, enabling you to get new users started quickly.

## Prerequisites

Before you begin, ensure you have the following installed on your system:

*   **Python:** Version 3.9 or higher. You can check your Python version by running `python --version` or `python3 --version` in your terminal.
*   **pip:** The Python package installer. It usually comes bundled with Python.

## Installation

1.  **Clone the Repository:**
    If you haven't already, clone the Agent Framework repository from GitHub:
    ```bash
    git clone https://github.com/your-username/agent-framework.git # Replace with the actual repo URL if different
    cd agent-framework
    ```

2.  **Install Dependencies:**
    Install the required Python packages using pip. This command will read from the `requirements.txt` file (which will be generated/available in the project).
    ```bash
    pip install -r requirements.txt
    ```

## Understanding the Basics

The Agent Framework is designed around key concepts:

*   **Agents:** AI entities responsible for performing specific tasks. They can be configured using YAML specifications.
*   **Workflows:** Orchestrate sequences of agents to achieve a larger goal. Workflows define the dependencies and execution order of tasks.
*   **LLM Providers:** The framework supports various Large Language Models (e.g., Gemini, Ollama, Kimi, Mistral) through an abstracted interface.

## Running Your First Workflow

The framework includes a Command-Line Interface (CLI) for running workflows.

1.  **Define a Workflow:**
    Workflows are typically defined in YAML files (e.g., `workflows/simple_workflow.yaml`). You can create or modify one to experiment with.

2.  **Execute a Workflow:**
    Use the `main.py` script to run a workflow. For example, to run `simple_workflow.yaml`:
    ```bash
    python main.py --workflow workflows/simple_workflow.yaml
    ```
    *(Note: This is a placeholder command. Actual commands might vary based on the CLI implementation.)*

## Next Steps

*   Explore the `docs/ARCHITECTURE.md` for a deeper understanding of the framework's design.
*   Refer to the `prompts/` directory for examples of prompt templates.
*   Examine agent specifications in `agents/specs/` to see how agents are defined.
*   Check out `src/` for the detailed implementation of each component.
