#!/usr/bin/env python3
"""Command-line interface for the todo list application.

This module provides the CLI for managing todo items with pattern autocomplete.
"""

import argparse
import sys
from pathlib import Path

from .todo import TodoList
from .patterns import PatternManager


def create_parser():
    """Create the argument parser for the CLI."""
    parser = argparse.ArgumentParser(
        prog='todo',
        description='Todo list application with pattern autocomplete'
    )
    
    parser.add_argument(
        '--todo-file',
        type=str,
        help='Path to the todo items file (default: ~/.todo_items.json)'
    )
    
    parser.add_argument(
        '--pattern-file',
        type=str,
        help='Path to the patterns file (default: ~/.todo_patterns.json)'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Add todo item
    add_parser = subparsers.add_parser('add', help='Add a new todo item')
    add_parser.add_argument('text', type=str, help='Todo item text (patterns will be expanded)')
    
    # List todo items
    list_parser = subparsers.add_parser('list', help='List todo items')
    list_parser.add_argument(
        '--filter',
        choices=['all', 'pending', 'completed'],
        default='all',
        help='Filter items (default: all)'
    )
    
    # Complete a todo item
    complete_parser = subparsers.add_parser('complete', help='Mark a todo item as complete')
    complete_parser.add_argument('index', type=int, help='Index of the item to complete (1-based)')
    
    # Uncomplete a todo item
    uncomplete_parser = subparsers.add_parser('uncomplete', help='Mark a todo item as incomplete')
    uncomplete_parser.add_argument('index', type=int, help='Index of the item to uncomplete (1-based)')
    
    # Remove a todo item
    remove_parser = subparsers.add_parser('remove', help='Remove a todo item')
    remove_parser.add_argument('index', type=int, help='Index of the item to remove (1-based)')
    
    # Clear completed items
    subparsers.add_parser('clear', help='Clear all completed items')
    
    # Pattern commands
    pattern_parser = subparsers.add_parser('pattern', help='Manage patterns')
    pattern_subparsers = pattern_parser.add_subparsers(dest='pattern_command', help='Pattern commands')
    
    # Add pattern
    pattern_add = pattern_subparsers.add_parser('add', help='Add a new pattern')
    pattern_add.add_argument('prefix', type=str, help='Pattern prefix (shortcut)')
    pattern_add.add_argument('text', type=str, help='Full text to expand to')
    
    # Remove pattern
    pattern_remove = pattern_subparsers.add_parser('remove', help='Remove a pattern')
    pattern_remove.add_argument('prefix', type=str, help='Pattern prefix to remove')
    
    # List patterns
    pattern_subparsers.add_parser('list', help='List all patterns')
    
    # Expand text (for testing)
    expand_parser = subparsers.add_parser('expand', help='Expand a pattern prefix to full text')
    expand_parser.add_argument('text', type=str, help='Text to expand')
    
    return parser


def main():
    """Main entry point for the CLI."""
    parser = create_parser()
    args = parser.parse_args()
    
    # Initialize managers
    todo_list = TodoList(args.todo_file) if args.todo_file else TodoList()
    pattern_manager = PatternManager(args.pattern_file) if args.pattern_file else PatternManager()
    
    if args.command == 'add':
        # Expand patterns in the text
        expanded_text = pattern_manager.expand_text(args.text)
        item = todo_list.add(expanded_text)
        if expanded_text != args.text:
            print(f"Pattern expanded: '{args.text}' -> '{expanded_text}'")
        print(f"Added: {item}")
        
    elif args.command == 'list':
        if args.filter == 'pending':
            items = todo_list.list_pending()
        elif args.filter == 'completed':
            items = todo_list.list_completed()
        else:
            items = todo_list.list_all()
        
        if not items:
            print("No todo items found.")
        else:
            for i, item in enumerate(items, 1):
                print(f"{i}. {item}")
                
    elif args.command == 'complete':
        index = args.index - 1  # Convert to 0-based
        if todo_list.complete(index):
            print(f"Marked item {args.index} as complete.")
        else:
            print(f"Error: Invalid item index {args.index}")
            sys.exit(1)
            
    elif args.command == 'uncomplete':
        index = args.index - 1  # Convert to 0-based
        if todo_list.uncomplete(index):
            print(f"Marked item {args.index} as incomplete.")
        else:
            print(f"Error: Invalid item index {args.index}")
            sys.exit(1)
            
    elif args.command == 'remove':
        index = args.index - 1  # Convert to 0-based
        item = todo_list.remove(index)
        if item:
            print(f"Removed: {item}")
        else:
            print(f"Error: Invalid item index {args.index}")
            sys.exit(1)
            
    elif args.command == 'clear':
        count = todo_list.clear_completed()
        print(f"Cleared {count} completed item(s).")
        
    elif args.command == 'pattern':
        if args.pattern_command == 'add':
            pattern_manager.add_pattern(args.prefix, args.text)
            print(f"Added pattern: '{args.prefix}' -> '{args.text}'")
            
        elif args.pattern_command == 'remove':
            if pattern_manager.remove_pattern(args.prefix):
                print(f"Removed pattern: '{args.prefix}'")
            else:
                print(f"Error: Pattern '{args.prefix}' not found.")
                sys.exit(1)
                
        elif args.pattern_command == 'list':
            patterns = pattern_manager.list_patterns()
            if not patterns:
                print("No patterns defined.")
            else:
                print("Patterns:")
                for prefix, text in patterns.items():
                    print(f"  '{prefix}' -> '{text}'")
        else:
            parser.parse_args(['pattern', '--help'])
            
    elif args.command == 'expand':
        expanded = pattern_manager.expand_text(args.text)
        print(expanded)
        
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
