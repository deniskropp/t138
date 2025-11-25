# tests/test_prompt_templates.py
import pytest
import os
from src.prompt_templates import load_template, render_template

@pytest.fixture
def create_template_file(tmp_path):
    """Fixture to create a temporary template file."""
    template_path = tmp_path / "test_template.j2"
    content = "Hello, {{ name }}! Today is {{ day }}."
    with open(template_path, "w") as f:
        f.write(content)
    return str(template_path)

def test_load_template(create_template_file):
    """Test that load_template reads the file content correctly."""
    content = load_template(create_template_file)
    assert content == "Hello, {{ name }}! Today is {{ day }}."

def test_render_template():
    """Test that render_template correctly processes Jinja2 syntax."""
    template_string = "My favorite color is {{ color }}."
    rendered_output = render_template(template_string, color="blue")
    assert rendered_output == "My favorite color is blue."

def test_render_template_with_multiple_variables(create_template_file):
    """Test rendering a template with multiple variables."""
    template_string = load_template(create_template_file)
    rendered_output = render_template(template_string, name="Alice", day="Monday")
    assert rendered_output == "Hello, Alice! Today is Monday."

def test_render_template_with_missing_variable():
    """Test rendering a template with a missing variable (Jinja2 default behavior)."""
    template_string = "Hello, {{ name }}!"
    rendered_output = render_template(template_string)
    assert rendered_output == "Hello, !" # Jinja2 renders missing variables as empty string

def test_load_template_non_existent():
    """Test loading a non-existent template returns None."""
    # Assuming read_file returns None for non-existent files
    assert load_template("non_existent.j2") is None

