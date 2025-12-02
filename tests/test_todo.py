"""Tests for the todo list module."""

import json
import tempfile
from pathlib import Path

import pytest

from todo.todo import TodoItem, TodoList


@pytest.fixture
def temp_storage():
    """Create a temporary storage file for testing."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        f.write('[]')
        temp_path = f.name
    yield temp_path
    Path(temp_path).unlink(missing_ok=True)


@pytest.fixture
def todo_list(temp_storage):
    """Create a TodoList with a temporary storage file."""
    return TodoList(temp_storage)


class TestTodoItem:
    """Tests for TodoItem class."""

    def test_create_item(self):
        """Test creating a todo item."""
        item = TodoItem('Buy groceries')
        assert item.text == 'Buy groceries'
        assert item.completed is False
        assert item.created_at is not None
        assert item.completed_at is None

    def test_mark_complete(self):
        """Test marking an item as complete."""
        item = TodoItem('Buy groceries')
        item.mark_complete()
        assert item.completed is True
        assert item.completed_at is not None

    def test_mark_incomplete(self):
        """Test marking an item as incomplete."""
        item = TodoItem('Buy groceries')
        item.mark_complete()
        item.mark_incomplete()
        assert item.completed is False
        assert item.completed_at is None

    def test_to_dict(self):
        """Test converting item to dictionary."""
        item = TodoItem('Buy groceries')
        data = item.to_dict()
        assert data['text'] == 'Buy groceries'
        assert data['completed'] is False
        assert 'created_at' in data

    def test_from_dict(self):
        """Test creating item from dictionary."""
        data = {
            'text': 'Buy groceries',
            'completed': True,
            'created_at': '2024-01-01T12:00:00',
            'completed_at': '2024-01-01T13:00:00'
        }
        item = TodoItem.from_dict(data)
        assert item.text == 'Buy groceries'
        assert item.completed is True
        assert item.created_at == '2024-01-01T12:00:00'
        assert item.completed_at == '2024-01-01T13:00:00'

    def test_str_representation(self):
        """Test string representation of items."""
        item = TodoItem('Buy groceries')
        assert str(item) == '[○] Buy groceries'
        item.mark_complete()
        assert str(item) == '[✓] Buy groceries'


class TestTodoList:
    """Tests for TodoList class."""

    def test_add_item(self, todo_list):
        """Test adding an item to the list."""
        item = todo_list.add('Buy groceries')
        assert item.text == 'Buy groceries'
        assert len(todo_list) == 1

    def test_remove_item(self, todo_list):
        """Test removing an item from the list."""
        todo_list.add('Buy groceries')
        todo_list.add('Walk the dog')
        removed = todo_list.remove(0)
        assert removed.text == 'Buy groceries'
        assert len(todo_list) == 1

    def test_remove_invalid_index(self, todo_list):
        """Test removing an item with invalid index."""
        todo_list.add('Buy groceries')
        removed = todo_list.remove(99)
        assert removed is None
        assert len(todo_list) == 1

    def test_complete_item(self, todo_list):
        """Test completing an item."""
        todo_list.add('Buy groceries')
        assert todo_list.complete(0) is True
        items = todo_list.list_all()
        assert items[0].completed is True

    def test_complete_invalid_index(self, todo_list):
        """Test completing an item with invalid index."""
        todo_list.add('Buy groceries')
        assert todo_list.complete(99) is False

    def test_uncomplete_item(self, todo_list):
        """Test uncompleting an item."""
        todo_list.add('Buy groceries')
        todo_list.complete(0)
        assert todo_list.uncomplete(0) is True
        items = todo_list.list_all()
        assert items[0].completed is False

    def test_list_pending(self, todo_list):
        """Test listing pending items."""
        todo_list.add('Buy groceries')
        todo_list.add('Walk the dog')
        todo_list.complete(0)
        pending = todo_list.list_pending()
        assert len(pending) == 1
        assert pending[0].text == 'Walk the dog'

    def test_list_completed(self, todo_list):
        """Test listing completed items."""
        todo_list.add('Buy groceries')
        todo_list.add('Walk the dog')
        todo_list.complete(0)
        completed = todo_list.list_completed()
        assert len(completed) == 1
        assert completed[0].text == 'Buy groceries'

    def test_clear_completed(self, todo_list):
        """Test clearing completed items."""
        todo_list.add('Buy groceries')
        todo_list.add('Walk the dog')
        todo_list.complete(0)
        count = todo_list.clear_completed()
        assert count == 1
        assert len(todo_list) == 1
        assert todo_list.list_all()[0].text == 'Walk the dog'

    def test_persistence(self, temp_storage):
        """Test that items are persisted to file."""
        list1 = TodoList(temp_storage)
        list1.add('Buy groceries')
        
        # Create a new list with the same storage
        list2 = TodoList(temp_storage)
        assert len(list2) == 1
        assert list2.list_all()[0].text == 'Buy groceries'

    def test_unicode_items(self, todo_list):
        """Test items with Unicode characters (Persian text)."""
        item = todo_list.add('خرید نان از نانوایی')
        assert item.text == 'خرید نان از نانوایی'
