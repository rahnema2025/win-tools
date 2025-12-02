"""Tests for the CLI module."""

import subprocess
import tempfile
import sys
from pathlib import Path

import pytest


@pytest.fixture
def temp_files():
    """Create temporary files for todo and patterns."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        f.write('[]')
        todo_path = f.name
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        f.write('{}')
        pattern_path = f.name
    yield todo_path, pattern_path
    Path(todo_path).unlink(missing_ok=True)
    Path(pattern_path).unlink(missing_ok=True)


def run_cli(*args, todo_file=None, pattern_file=None):
    """Run the CLI with the given arguments."""
    cmd = [sys.executable, '-m', 'todo.main']
    if todo_file:
        cmd.extend(['--todo-file', todo_file])
    if pattern_file:
        cmd.extend(['--pattern-file', pattern_file])
    cmd.extend(args)
    
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=str(Path(__file__).parent.parent))
    return result


class TestCLI:
    """Tests for the CLI."""

    def test_add_item(self, temp_files):
        """Test adding an item via CLI."""
        todo_file, pattern_file = temp_files
        result = run_cli('add', 'Buy groceries', todo_file=todo_file, pattern_file=pattern_file)
        assert result.returncode == 0
        assert 'Added' in result.stdout
        assert 'Buy groceries' in result.stdout

    def test_list_items(self, temp_files):
        """Test listing items via CLI."""
        todo_file, pattern_file = temp_files
        run_cli('add', 'Buy groceries', todo_file=todo_file, pattern_file=pattern_file)
        run_cli('add', 'Walk the dog', todo_file=todo_file, pattern_file=pattern_file)
        
        result = run_cli('list', todo_file=todo_file, pattern_file=pattern_file)
        assert result.returncode == 0
        assert 'Buy groceries' in result.stdout
        assert 'Walk the dog' in result.stdout

    def test_complete_item(self, temp_files):
        """Test completing an item via CLI."""
        todo_file, pattern_file = temp_files
        run_cli('add', 'Buy groceries', todo_file=todo_file, pattern_file=pattern_file)
        
        result = run_cli('complete', '1', todo_file=todo_file, pattern_file=pattern_file)
        assert result.returncode == 0
        assert 'complete' in result.stdout.lower()

    def test_remove_item(self, temp_files):
        """Test removing an item via CLI."""
        todo_file, pattern_file = temp_files
        run_cli('add', 'Buy groceries', todo_file=todo_file, pattern_file=pattern_file)
        
        result = run_cli('remove', '1', todo_file=todo_file, pattern_file=pattern_file)
        assert result.returncode == 0
        assert 'Removed' in result.stdout

    def test_pattern_add(self, temp_files):
        """Test adding a pattern via CLI."""
        todo_file, pattern_file = temp_files
        result = run_cli('pattern', 'add', 'mtg', 'Meeting with team', 
                        todo_file=todo_file, pattern_file=pattern_file)
        assert result.returncode == 0
        assert 'Added pattern' in result.stdout

    def test_pattern_list(self, temp_files):
        """Test listing patterns via CLI."""
        todo_file, pattern_file = temp_files
        run_cli('pattern', 'add', 'mtg', 'Meeting with team', 
                todo_file=todo_file, pattern_file=pattern_file)
        
        result = run_cli('pattern', 'list', todo_file=todo_file, pattern_file=pattern_file)
        assert result.returncode == 0
        assert 'mtg' in result.stdout
        assert 'Meeting with team' in result.stdout

    def test_pattern_remove(self, temp_files):
        """Test removing a pattern via CLI."""
        todo_file, pattern_file = temp_files
        run_cli('pattern', 'add', 'mtg', 'Meeting with team', 
                todo_file=todo_file, pattern_file=pattern_file)
        
        result = run_cli('pattern', 'remove', 'mtg', 
                        todo_file=todo_file, pattern_file=pattern_file)
        assert result.returncode == 0
        assert 'Removed pattern' in result.stdout

    def test_pattern_expansion(self, temp_files):
        """Test pattern expansion when adding todo items."""
        todo_file, pattern_file = temp_files
        # Add a pattern
        run_cli('pattern', 'add', 'mtg', 'Meeting with team', 
                todo_file=todo_file, pattern_file=pattern_file)
        
        # Add a todo with the pattern
        result = run_cli('add', 'mtg', todo_file=todo_file, pattern_file=pattern_file)
        assert result.returncode == 0
        assert 'Pattern expanded' in result.stdout
        assert 'Meeting with team' in result.stdout

    def test_expand_command(self, temp_files):
        """Test the expand command."""
        todo_file, pattern_file = temp_files
        run_cli('pattern', 'add', 'mtg', 'Meeting with team', 
                todo_file=todo_file, pattern_file=pattern_file)
        
        result = run_cli('expand', 'mtg at 3pm', todo_file=todo_file, pattern_file=pattern_file)
        assert result.returncode == 0
        assert 'Meeting with team at 3pm' in result.stdout
