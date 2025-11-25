# src/models.py
"""Pydantic models and dataclasses for core system entities."""
from pydantic import BaseModel
from typing import Any, Dict, List, Optional

class AgentSpec(BaseModel):
    name: str
    role: str
    description: str

class TaskSpec(BaseModel):
    id: str
    name: str
    description: str
    agent_name: str
    input_data: Dict[str, Any] = {}
    dependencies: List[str] = []

class Artifact(BaseModel):
    name: str
    type: str
    data: Any

class Session(BaseModel):
    id: str
    start_time: str
    end_time: Optional[str] = None
    status: str
    logs: List[str] = []
    artifacts: List[Artifact] = []

class ExecutionContext(BaseModel):
    session_id: str
    env_vars: Dict[str, str] = {}
    runtime_flags: Dict[str, Any] = {}
    current_task_id: Optional[str] = None

class AgentResponse(BaseModel):
    status: str
    output: Dict[str, Any] = {}
    artifacts: List[Artifact] = []
