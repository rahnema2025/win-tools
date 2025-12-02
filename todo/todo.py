"""Core todo list functionality.

This module provides the TodoList class for managing todo items.
"""

import json
import os
from datetime import datetime
from pathlib import Path


DEFAULT_TODO_PATH = Path.home() / ".todo_items.json"


class TodoItem:
    """Represents a single todo item."""

    def __init__(self, text, completed=False, created_at=None, completed_at=None):
        """Initialize a todo item.
        
        Args:
            text: The text description of the todo item
            completed: Whether the item is completed
            created_at: ISO format timestamp of creation time
            completed_at: ISO format timestamp of completion time
        """
        self.text = text
        self.completed = completed
        self.created_at = created_at or datetime.now().isoformat()
        self.completed_at = completed_at

    def mark_complete(self):
        """Mark the todo item as complete."""
        self.completed = True
        self.completed_at = datetime.now().isoformat()

    def mark_incomplete(self):
        """Mark the todo item as incomplete."""
        self.completed = False
        self.completed_at = None

    def to_dict(self):
        """Convert the todo item to a dictionary."""
        return {
            'text': self.text,
            'completed': self.completed,
            'created_at': self.created_at,
            'completed_at': self.completed_at
        }

    @classmethod
    def from_dict(cls, data):
        """Create a TodoItem from a dictionary."""
        return cls(
            text=data['text'],
            completed=data.get('completed', False),
            created_at=data.get('created_at'),
            completed_at=data.get('completed_at')
        )

    def __str__(self):
        status = "✓" if self.completed else "○"
        return f"[{status}] {self.text}"


class TodoList:
    """Manages a list of todo items."""

    def __init__(self, storage_path=None):
        """Initialize the todo list.
        
        Args:
            storage_path: Path to the JSON file for storing todos.
                         Defaults to ~/.todo_items.json
        """
        self.storage_path = Path(storage_path) if storage_path else DEFAULT_TODO_PATH
        self.items = []
        self.load()

    def load(self):
        """Load todo items from storage."""
        if self.storage_path.exists():
            try:
                with open(self.storage_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.items = [TodoItem.from_dict(item) for item in data]
            except (json.JSONDecodeError, IOError):
                self.items = []
        else:
            self.items = []

    def save(self):
        """Save todo items to storage."""
        with open(self.storage_path, 'w', encoding='utf-8') as f:
            data = [item.to_dict() for item in self.items]
            json.dump(data, f, ensure_ascii=False, indent=2)

    def add(self, text):
        """Add a new todo item.
        
        Args:
            text: The text description of the todo item
            
        Returns:
            The created TodoItem
        """
        item = TodoItem(text)
        self.items.append(item)
        self.save()
        return item

    def remove(self, index):
        """Remove a todo item by index.
        
        Args:
            index: The index of the item to remove (0-based)
            
        Returns:
            The removed item, or None if index is invalid
        """
        if 0 <= index < len(self.items):
            item = self.items.pop(index)
            self.save()
            return item
        return None

    def complete(self, index):
        """Mark a todo item as complete.
        
        Args:
            index: The index of the item to complete (0-based)
            
        Returns:
            True if successful, False if index is invalid
        """
        if 0 <= index < len(self.items):
            self.items[index].mark_complete()
            self.save()
            return True
        return False

    def uncomplete(self, index):
        """Mark a todo item as incomplete.
        
        Args:
            index: The index of the item to uncomplete (0-based)
            
        Returns:
            True if successful, False if index is invalid
        """
        if 0 <= index < len(self.items):
            self.items[index].mark_incomplete()
            self.save()
            return True
        return False

    def list_all(self):
        """Get all todo items.
        
        Returns:
            A list of all TodoItem objects
        """
        return list(self.items)

    def list_pending(self):
        """Get all pending (incomplete) todo items.
        
        Returns:
            A list of pending TodoItem objects
        """
        return [item for item in self.items if not item.completed]

    def list_completed(self):
        """Get all completed todo items.
        
        Returns:
            A list of completed TodoItem objects
        """
        return [item for item in self.items if item.completed]

    def clear_completed(self):
        """Remove all completed items.
        
        Returns:
            The number of items removed
        """
        original_count = len(self.items)
        self.items = [item for item in self.items if not item.completed]
        self.save()
        return original_count - len(self.items)

    def __len__(self):
        return len(self.items)
