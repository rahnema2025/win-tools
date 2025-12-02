# Win Tools

A collection of Windows utility tools.

## Todo List with Pattern Autocomplete

A Python-based todo list application with a pattern autocomplete feature. Users can define patterns (shortcuts) in settings, and when typing the beginning of a pattern, the full text is automatically expanded.

### Installation

```bash
# Clone the repository
git clone https://github.com/rahnema2025/win-tools.git
cd win-tools

# Install pytest for running tests (optional)
pip install pytest
```

### Usage

#### Managing Todo Items

```bash
# Add a new todo item
python -m todo.main add "Buy groceries"

# List all todo items
python -m todo.main list

# List only pending items
python -m todo.main list --filter pending

# List only completed items
python -m todo.main list --filter completed

# Mark an item as complete (use 1-based index)
python -m todo.main complete 1

# Mark an item as incomplete
python -m todo.main uncomplete 1

# Remove an item
python -m todo.main remove 1

# Clear all completed items
python -m todo.main clear
```

#### Managing Patterns (Shortcuts)

The pattern feature allows you to define shortcuts that automatically expand to full text when you add a todo item.

```bash
# Add a pattern
python -m todo.main pattern add "mtg" "Meeting with team"
python -m todo.main pattern add "جلسه" "جلسه هفتگی تیم توسعه"

# List all patterns
python -m todo.main pattern list

# Remove a pattern
python -m todo.main pattern remove "mtg"

# Test pattern expansion
python -m todo.main expand "mtg at 3pm"
# Output: Meeting with team at 3pm
```

#### Using Patterns with Todo Items

When you add a todo item that starts with a pattern prefix, it will be automatically expanded:

```bash
# First, add a pattern
python -m todo.main pattern add "mtg" "Meeting with team"

# Now add a todo using the pattern
python -m todo.main add "mtg at 3pm"
# Output: Pattern expanded: 'mtg at 3pm' -> 'Meeting with team at 3pm'
#         Added: [○] Meeting with team at 3pm
```

### Custom Storage Paths

By default, todo items are stored in `~/.todo_items.json` and patterns in `~/.todo_patterns.json`. You can specify custom paths:

```bash
python -m todo.main --todo-file /path/to/todos.json --pattern-file /path/to/patterns.json add "Task"
```

### Running Tests

```bash
pip install pytest
python -m pytest tests/ -v
```

### Features

- ✅ Add, remove, complete, and uncomplete todo items
- ✅ Filter items by status (pending/completed)
- ✅ Pattern autocomplete - define shortcuts that expand to full text
- ✅ Unicode support (Persian/Farsi text)
- ✅ Persistent storage in JSON files
- ✅ Command-line interface

### License

MIT License
