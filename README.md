# AI Agent Framework

This project provides a framework for defining and running AI agent-based workflows. It allows users to define a series of tasks in a YAML file and then execute them using a variety of AI agents.

## Getting Started

### Prerequisites

*   Python 3.x
*   pip

### Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/deniskropp/t138.git
    cd t138
    ```

2.  Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

### Running a Workflow

To run a workflow, use the `run` command and specify the path to your workflow YAML file:

```bash
python main.py run workflows/simple_workflow.yaml
```

## Project Structure

*   `src/`: The main source code for the framework.
    *   `agents/`: Contains the different AI agent implementations.
    *   `workflow/`: Components for loading and managing workflows.
    *   `cli.py`: Defines the command-line interface.
    *   `main.py`: The main entry point of the application.
*   `workflows/`: Contains example workflow YAML files.
*   `tests/`: Contains the test suite for the project.
*   `requirements.txt`: A list of the Python packages required to run the project.

## Architecture

For a more detailed explanation of the project's architecture, please see the [ARCHITECTURE.md](ARCHITECTURE.md) file.

## How to Contribute

For more detailed contribution guidelines, please see the [CONTRIBUTING.md](CONTRIBUTING.md) file.

We welcome contributions to this project! Please follow these steps:

1.  **Fork the repository.**
2.  **Create a new branch** for your feature or bug fix:
    ```bash
    git checkout -b feature/your-feature-name
    ```
3.  **Make your changes** and commit them with clear, descriptive messages.
4.  **Run the tests** to ensure that your changes don't break anything:
    ```bash
    pytest
    ```
5.  **Push your branch** to your fork:
    ```bash
    git push origin feature/your-feature-name
    ```
6.  **Create a pull request** to the `main` branch of the original repository.

## Canon

Shared concepts (runtime kernel with `Result`/`Error`, `ArtifactStore` with `AddArtifact`/`GetArtifact`, `Orchestrator.AssignAgent`, Task-Agnostic Steps, role IDs, JSON schemas) are defined in [deniskropp/t333](https://github.com/deniskropp/t333) on `main`, the neutral source of truth. Only `canon/` there is normative (see [`canon/SPEC.md`](https://github.com/deniskropp/t333/blob/main/canon/SPEC.md)). This repo references t333 `main` without version pinning ([ADR-0005](https://github.com/deniskropp/t333/blob/main/docs/adr/0005-referenz-auf-main.md)). Repo-specific extensions use the `⫻x-t138/` namespace.

The local `meta/TAS-*.md` files are a project-specific TAS list; the TAS shape and categories are defined by [`canon/tas.kl`](https://github.com/deniskropp/t333/blob/main/canon/tas.kl).

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.
