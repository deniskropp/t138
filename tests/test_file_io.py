# tests/test_file_io.py
import pytest
import os
from src.file_io import read_file, write_file

def test_write_read_text_file(tmp_path):
    """Test writing and reading a text file."""
    file_path = tmp_path / "test.txt"
    content = "Hello, world!"
    assert write_file(str(file_path), content)
    assert read_file(str(file_path)) == content

def test_write_read_binary_file(tmp_path):
    """Test writing and reading a binary file."""
    file_path = tmp_path / "test.bin"
    content = b"\x01\x02\x03\x04"
    assert write_file(str(file_path), content, mode='wb')
    assert read_file(str(file_path), mode='rb') == content

def test_read_non_existent_file():
    """Test reading a file that does not exist returns None."""
    assert read_file("non_existent_file.txt") is None

def test_write_error(tmp_path):
    """Test writing to a read-only location (simulated)."""
    # Create a read-only directory
    read_only_dir = tmp_path / "read_only"
    read_only_dir.mkdir(mode=0o555) # r-xr-xr-x
    file_path = read_only_dir / "cant_write.txt"
    assert not write_file(str(file_path), "some content")
