import os
import re

# Source file path
source = "fletfly_lib/docs/class/README.md"

# Targets mapping
targets = {
    "README.md": "fletfly/",
    "fletfly_lib/README.md": ""
}

# 1. Root Note (for the workspace)
root_note = "> 💡 **Note:** This is the workspace for the [`fletfly`](./fletfly) library project.\n\n"

# 2. Polyglot Design Block (for navigation)
polyglot_block = "> 💡 **Polyglot Design Note:** This guide uses **Class-Based Routes** as our primary example to demonstrate the engine's hierarchical power. Choose a dedicated guide for other paradigms based on your technical background:\n>\n> * **[Class-Based Routes](docs/class/README.md)** — *Django (CBV), ASP.NET Controllers, Spring Boot*\n> * **[Dict-Based Routes](docs/dict/README.md)** — *Vue Router, Angular Router, React Router (Objects)*\n> * **[Declarative Routes](docs/declare/README.md)** — *SwiftUI, Flutter (GoRouter), React Router (JSX)*\n> * **[File-Based Routes](docs/file/README.md)** — *Next.js, Nuxt.js, SvelteKit*\n> * **[Route-Based Decorators](docs/decoration/README.md)** — *FastAPI, Flask, NestJS*\n> * **[Chain-Based Routes](docs/chain/README.md)** — *Laravel Core, Express.js (Chained)*\n---\n"
def sync_and_inject(source_path, target_path, prefix):
    # Read source content
    with open(source_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

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