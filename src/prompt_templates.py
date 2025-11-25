# src/prompt_templates.py
"""Loads and renders prompt templates, supporting Jinja2."""
from jinja2 import Template
from src.file_io import read_file

def load_template(template_path: str) -> str:
    """Loads a prompt template from a file."""
    return read_file(template_path)

def render_template(template_string: str, **kwargs) -> str:
    """Renders a Jinja2 template with provided arguments."""
    template = Template(template_string)
    return template.render(**kwargs)
