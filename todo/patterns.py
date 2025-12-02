"""Pattern management for todo list application.

This module provides pattern storage and autocomplete functionality.
Users can define patterns (shortcuts) that expand to full text when
the pattern prefix is typed.
"""

import json
import os
from pathlib import Path


DEFAULT_CONFIG_PATH = Path.home() / ".todo_patterns.json"


class PatternManager:
    """Manages patterns for text expansion in todo items."""

    def __init__(self, config_path=None):
        """Initialize the pattern manager.
        
        Args:
            config_path: Path to the JSON config file for patterns.
                         Defaults to ~/.todo_patterns.json
        """
        self.config_path = Path(config_path) if config_path else DEFAULT_CONFIG_PATH
        self.patterns = {}
        self.load_patterns()

    def load_patterns(self):
        """Load patterns from the config file."""
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    self.patterns = json.load(f)
            except (json.JSONDecodeError, IOError):
                self.patterns = {}
        else:
            self.patterns = {}

    def save_patterns(self):
        """Save patterns to the config file."""
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(self.patterns, f, ensure_ascii=False, indent=2)

    def add_pattern(self, prefix, full_text):
        """Add a new pattern.
        
        Args:
            prefix: The shortcut/prefix to type (e.g., 'mtg')
            full_text: The full text to expand to (e.g., 'Meeting with team')
        """
        self.patterns[prefix] = full_text
        self.save_patterns()

    def remove_pattern(self, prefix):
        """Remove a pattern by its prefix.
        
        Args:
            prefix: The prefix of the pattern to remove
            
        Returns:
            True if pattern was removed, False if not found
        """
        if prefix in self.patterns:
            del self.patterns[prefix]
            self.save_patterns()
            return True
        return False

    def get_pattern(self, prefix):
        """Get the full text for a pattern prefix.
        
        Args:
            prefix: The prefix to look up
            
        Returns:
            The full text if found, None otherwise
        """
        return self.patterns.get(prefix)

    def expand_text(self, text):
        """Expand text by replacing pattern prefixes with full text.
        
        If the text starts with a registered pattern prefix, it will be
        replaced with the full text.
        
        Args:
            text: The input text to expand
            
        Returns:
            The expanded text (or original if no pattern matches)
        """
        # Check if text starts with any pattern prefix
        for prefix, full_text in self.patterns.items():
            if text.startswith(prefix):
                # Replace the prefix with full text
                remainder = text[len(prefix):]
                if remainder:
                    return full_text + remainder
                return full_text
        return text

    def list_patterns(self):
        """List all registered patterns.
        
        Returns:
            A dictionary of all patterns {prefix: full_text}
        """
        return dict(self.patterns)

    def find_matching_patterns(self, partial_prefix):
        """Find patterns that start with the given partial prefix.
        
        Args:
            partial_prefix: The beginning of a pattern prefix
            
        Returns:
            A list of (prefix, full_text) tuples that match
        """
        matches = []
        for prefix, full_text in self.patterns.items():
            if prefix.startswith(partial_prefix):
                matches.append((prefix, full_text))
        return matches
