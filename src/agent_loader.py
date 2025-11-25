# src/agent_loader.py
"""Loads agent specifications from files into AgentSpec models."""
import os
import yaml
import json
from typing import List
from src.models import AgentSpec
from src.file_io import read_file
from src.paths import get_root_dir
import logging

logger = logging.getLogger(__name__)

def load_agent_specs(spec_dir: str = "agents/specs") -> List[AgentSpec]:
    """
    Loads and parses agent specification files from a given directory
    into AgentSpec models. Supports YAML and JSON formats.
    """
    agent_specs: List[AgentSpec] = []
    full_spec_dir = os.path.join(get_root_dir(), spec_dir)

    if not os.path.exists(full_spec_dir):
        logger.warning(f"Agent specification directory not found: {full_spec_dir}")
        return agent_specs

    for filename in os.listdir(full_spec_dir):
        filepath = os.path.join(full_spec_dir, filename)
        content = read_file(filepath)
        if content is None:
            logger.warning(f"Could not read agent spec file: {filepath}")
            continue

        try:
            if filename.endswith((".yaml", ".yml")):
                data = yaml.safe_load(content)
            elif filename.endswith(".json"):
                data = json.loads(content)
            else:
                logger.debug(f"Skipping unknown file type: {filename}")
                continue
            
            agent_spec = AgentSpec(**data)
            agent_specs.append(agent_spec)
            logger.info(f"Loaded agent spec: {agent_spec.name}")
        except (yaml.YAMLError, json.JSONDecodeError) as e:
            logger.error(f"Error parsing agent spec file {filepath}: {e}")
        except Exception as e:
            logger.error(f"Unexpected error loading agent spec {filepath}: {e}")
            
    return agent_specs
