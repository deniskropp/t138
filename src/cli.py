# src/cli.py
"""Defines and parses command-line interface arguments and subcommands."""
import argparse
import os
from src.paths import get_root_dir
from src.logger import setup_logging
from src.workflow_loader import workflow_loader
from src.orchestrator import Orchestrator
from src.agents.factory import AgentFactory
import logging

logger = logging.getLogger(__name__)

def main_cli():
    parser = argparse.ArgumentParser(description="Agent Framework CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Run command
    run_parser = subparsers.add_parser("run", help="Run a workflow")
    run_parser.add_argument("workflow_file", type=str, help="Path to workflow definition file (e.g., workflows/my_workflow.yaml)")

    # Init command
    init_parser = subparsers.add_parser("init", help="Initialize a new project")

    # Status command
    status_parser = subparsers.add_parser("status", help="Show current system status")

    args = parser.parse_args()

    if args.command == "run":
        logger.info(f"Attempting to run workflow from: {args.workflow_file}")
        try:
            tasks = workflow_loader.load_workflow_from_file(args.workflow_file)
            agent_factory = AgentFactory()
            orchestrator = Orchestrator(agent_factory)
            orchestrator.run_workflow(tasks)
        except FileNotFoundError as e:
            logger.error(f"Error: {e}")
            sys.exit(1)
        except ValueError as e:
            logger.error(f"Workflow configuration error: {e}")
            sys.exit(1)
        except Exception as e:
            logger.error(f"An unexpected error occurred during workflow execution: {e}", exc_info=True)
            sys.exit(1)
    elif args.command == "init":
        print("Initializing new project...")
        # Placeholder: Call project initialization logic
    elif args.command == "status":
        print("Showing system status...")
        # Placeholder: Call status display logic
    else:
        parser.print_help()

if __name__ == "__main__":
    setup_logging()
    main_cli()
