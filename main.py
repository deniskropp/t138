# main.py
"""The main entry point of the application."""
import sys
from src.bootstrap import bootstrap_system
from src.cli import main_cli # Assuming main_cli will handle the parsing and calling of components
from src.runtime import system_runtime
import logging

def main():
    # Bootstrap the system
    bootstrap_system()

    # Run the CLI
    main_cli()

if __name__ == "__main__":
    main()
