# src/workflow_loader.py
"""Loads workflow definitions from YAML/JSON files."""
import os
import yaml
import json
from typing import List, Dict, Any
from src.models import TaskSpec
from src.file_io import read_file
from src.paths import get_root_dir
import logging

logger = logging.getLogger(__name__)

class WorkflowLoader:
    def __init__(self):
        pass

    def load_workflow_from_file(self, filepath: str) -> List[TaskSpec]:
        """
        Loads a workflow definition from a YAML or JSON file and returns a list of TaskSpec objects.
        """
        full_filepath = os.path.join(get_root_dir(), filepath)
        content = read_file(full_filepath)
        if content is None:
            raise FileNotFoundError(f"Workflow file not found or unreadable: {full_filepath}")

        data: Dict[str, Any]
        try:
            if filepath.endswith((".yaml", ".yml")):
                data = yaml.safe_load(content)
            elif filepath.endswith(".json"):
                data = json.loads(content)
            else:
                raise ValueError(f"Unsupported workflow file type: {filepath}. Must be .yaml, .yml, or .json")

            tasks_data = data.get("tasks", [])
            if not isinstance(tasks_data, list):
                raise ValueError("Workflow 'tasks' key must be a list.")
            
            task_specs: List[TaskSpec] = []
            for task_dict in tasks_data:
                task_specs.append(TaskSpec(**task_dict))
            
            logger.info(f"Loaded workflow from {filepath} with {len(task_specs)} tasks.")
            return task_specs

        except (yaml.YAMLError, json.JSONDecodeError) as e:
            raise ValueError(f"Error parsing workflow file {full_filepath}: {e}")
        except Exception as e:
            raise ValueError(f"Unexpected error loading workflow from {full_filepath}: {e}")

workflow_loader = WorkflowLoader()
