import os
import re

# Source file path
source = "fletfly/docs/class/INTRO.md"

# Targets mapping: target_file -> link_prefix
targets = {
    "README.md": "fletfly/",           # Root README
    "fletfly/README.md": ""           # Library README
}

# The note to prepend to the root README
root_note = "> 💡 **Note:** This is the workspace for the `fletfly` library project [`fletfly`](./fletfly).\n---\n"

# Read the source content
with open(source, 'r', encoding='utf-8') as f:
    content = f.read()

def sync_links(text, prefix):
    # Update links starting with 'docs/' to match the target's relative path
    def replace(match):
        text_content = match.group(1)
        link_path = match.group(2)
        return f"[{text_content}]({prefix}{link_path})"

    return re.sub(r'\[([^\]]+)\]\((docs/[^)]+)\)', replace, text)

# Execution loop
for target, prefix in targets.items():
    # Ensure directory exists before writing
    dir_name = os.path.dirname(target)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)
    
    # Process the content
    new_content = sync_links(content, prefix)
    
    # Prepend the note only to the root README.md
    if target == "README.md":
        new_content = root_note + new_content
    
    # Write to target
    with open(target, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"Synced to: {target}")