import os
import json
from pathlib import Path

IGNORE_DIRS = {
    '.git', 'node_modules', '.venv', 'venv', '__pycache__',
    '.agents', 'dist', 'build', '.idea', '.vscode', '.next',
    '.nuxt', '.output', 'coverage', '.pytest_cache', '.mypy_cache',
    '.svn', '.hg', '.tox', '__snapshots__',
}

IGNORE_EXTS = {
    '.pyc', '.pyo', '.pyd', '.so', '.dll', '.exe',
    '.png', '.jpg', '.jpeg', '.gif', '.mp4', '.mp3', '.wav',
    '.zip', '.tar', '.gz', '.lock', '.ico', '.svg', '.woff', '.woff2'
}

def generate_map(root_dir='.'):
    root_path = Path(root_dir)
    tree_lines = []
    file_details = []

    for current_root, dirs, files in os.walk(root_path):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]

        rel_path = Path(current_root).relative_to(root_path)
        level = len(rel_path.parts) if rel_path.name else 0
        indent = '  ' * level

        if rel_path.name:
            tree_lines.append(f"{indent}📂 {rel_path.name}/")

        sub_indent = '  ' * (level + 1)
        for f in sorted(files):
            file_path = Path(current_root) / f

            if f.startswith('.'):
                continue

            tree_lines.append(f"{sub_indent}📄 {f}")

            if file_path.suffix.lower() in IGNORE_EXTS:
                continue

            context = ""
            try:
                with open(file_path, 'r', encoding='utf-8') as file_obj:
                    lines = []
                    for _ in range(5):
                        try:
                            line = next(file_obj).strip()
                            if line and not line.startswith(('import', 'from', '//', '/*', '*', '#!')):
                                lines.append(line)
                        except StopIteration:
                            break
                    context = " ".join(lines)
            except Exception:
                context = "[Binary or unreadable]"

            file_details.append({
                "path": str(file_path.relative_to(root_path)).replace('\\', '/'),
                "ext": file_path.suffix,
                "context": context[:150] + "..." if len(context) > 150 else context
            })

    return tree_lines, file_details

def write_project_map(tree_lines, file_details):
    agents_dir = Path('.agents')
    agents_dir.mkdir(exist_ok=True)

    map_path = agents_dir / 'PROJECT_MAP.md'
    json_path = agents_dir / 'graph.json'

    with open(map_path, 'w', encoding='utf-8') as f:
        f.write("# Project Map\n\n")
        f.write("> Auto-generated. Read this first to understand the codebase.\n\n")
        f.write("## File Tree\n```\n")
        f.write("\n".join(tree_lines))
        f.write("\n```\n\n")
        f.write("## File Contexts\n\n")
        for detail in file_details:
            f.write(f"- **`{detail['path']}`**")
            if detail['context']:
                f.write(f" — {detail['context']}")
            f.write("\n")

    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(file_details, f, indent=2)

    print(f"Generated: {map_path}")
    print(f"Generated: {json_path}")
    print(f"Total files mapped: {len(file_details)}")

if __name__ == '__main__':
    print("Generating Agent Project Map...")
    tree, details = generate_map()
    write_project_map(tree, details)
