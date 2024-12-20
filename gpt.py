#!/usr/bin/env python3
import os

def print_tree_and_files(base_dir):
    print("Tree below:\n'''")

    def print_tree(directory, prefix=""):
        allowed_extensions = {'.py', '.rs', '.js', '.css', '.html'}

        def contains_allowed_files(dir_path):
            for root, _, files in os.walk(dir_path):
                for file in files:
                    if any(file.endswith(ext) for ext in allowed_extensions):
                        return True
            return False

        entries = sorted(os.listdir(directory))
        entries_count = len(entries)

        for i, entry in enumerate(entries):
            path = os.path.join(directory, entry)
            if entry.startswith('.') or (os.path.isdir(path) and not contains_allowed_files(path)):
                continue
            connector = "├── " if i < entries_count - 1 else "└── "
            print(f"{prefix}{connector}{entry}")
            if os.path.isdir(path):
                new_prefix = f"{prefix}{'│   ' if i < entries_count - 1 else '    '}"
                print_tree(path, new_prefix)

    print_tree(base_dir)
    print("'''\n\n")

    print("\nFiles below:\n")

    def is_binary(file_path):
        try:
            with open(file_path, 'rb') as f:
                chunk = f.read(1024)
                if b'\x00' in chunk:
                    return True
        except Exception as e:
            return True
        return False

    def print_file_paths_and_contents(directory, base_directory):
        allowed_extensions = {'.py', '.rs', '.js', '.css', '.html'}
        for root, dirs, files in os.walk(directory):
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            for file in files:
                if not any(file.endswith(ext) for ext in allowed_extensions):
                    continue
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, base_directory)
                if is_binary(file_path):
                    continue
                print(relative_path)
                print("```")
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        print(f.read())
                except Exception as e:
                    print(f"Error reading file: {e}")
                print("```\n")

    print_file_paths_and_contents(base_dir, base_dir)

if __name__ == "__main__":
    current_directory = os.getcwd()
    print_tree_and_files(current_directory)
