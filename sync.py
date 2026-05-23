import os
import re

# Source file path
source = "fletfly/docs/class/INTRO.md"

# Targets mapping
targets = {
    "README.md": "fletfly/",
    "fletfly/README.md": ""
}

# 1. Root Note (for the workspace)
root_note = "> 💡 **Note:** This is the workspace for the [`fletfly`](./fletfly) library project.\n\n---\n\n"

# 2. Polyglot Design Block (for navigation)
polyglot_block = "> 💡 **Polyglot Design:** `fletfly` adapts to your coding model. The core engine is unified, but the syntax is yours to choose.\n>\n> **Choose your weapon:**\n>\n> * **[Class-Based](docs/class/INTRO.md)** — *Django, Flutter, ASP.NET*\n> * **[Registry/Dictionary](docs/dict/INTRO.md)** — *Vue, Express, Angular*\n> * **[Declarative](docs/declare/INTRO.md)** — *React, SwiftUI, Flutter Trees*\n> * **[File-Based](docs/file/INTRO.md)** — *Next.js, Nuxt.js, SvelteKit*\n> * **[Decorator-Based](docs/decoration/INTRO.md)** — *FastAPI, Flask, NestJS*\n>\n> ---\n> 📌 **Note:** This guide uses **Class-Based Routing** as our primary example to demonstrate the engine's hierarchical power. You can find dedicated guides for other paradigms in their respective directories.\n---\n"

def sync_and_inject(source_path, target_path, prefix):
    # Read source content
    with open(source_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Remove the polyglot block from source if it exists
    content = "".join(lines)
    content = re.sub(r'> 💡 \*\*Polyglot Design:\*\*.*?(?=---)', '', content, flags=re.DOTALL)
    lines = content.splitlines(keepends=True)

    # Insert Polyglot block at line 6
    lines.insert(6, polyglot_block)

    # Insert Root Note at line 0 (only for root README)
    if target_path == "README.md":
        lines.insert(0, root_note)

    # Apply prefix to links in the content
    final_content = "".join(lines)
    def replace(match):
        text_content = match.group(1)
        link_path = match.group(2)
        return f"[{text_content}]({prefix}{link_path})"

    # Update links starting with 'docs/'
    final_content = re.sub(r'\[([^\]]+)\]\((docs/[^)]+)\)', replace, final_content)

    # Ensure directory exists before writing
    dir_name = os.path.dirname(target_path)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)
        
    # Write the result
    with open(target_path, 'w', encoding='utf-8') as f:
        f.write(final_content)

# Execution
for target, prefix in targets.items():
    sync_and_inject(source, target, prefix)
    print(f"Synced and injected content to: {target}")