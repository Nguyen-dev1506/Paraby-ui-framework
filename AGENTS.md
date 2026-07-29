# Workspace Agent Rules

This file contains rules specific to this workspace.

## Code Modification & Transparency
- **Transparent Editing:** Do NOT use background Python scripts, scratch directory regex scripts, or shell commands (e.g., sed, awk, PowerShell replacements) to manipulate or modify project source code.
- **Use Native Tools:** You MUST strictly use the native, dedicated file-editing tools (like `replace_file_content` or `multi_replace_file_content`) when editing files.
- **Reasoning:** This guarantees that all code modifications are fully transparent, properly diffed, and clearly visible to the user within the IDE UI. Avoid "hacky" mass-replacements that hide changes from the user.
