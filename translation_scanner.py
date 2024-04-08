import os
import re

def find_text_in_files(folder_path):
    text_set = set()  # Use a set to automatically avoid duplicates

    # Regular expression to match patterns like __("text") or __('text')
    pattern = re.compile(r'__\(([\'"])([^\'"]+)\1\)')

    # Walk through each file in the folder and its subfolders
    for root, _, files in os.walk(folder_path):
        for file_name in files:
            # Skip non-PHP files
            if not file_name.endswith('.php'):
                continue
            
            file_path = os.path.join(root, file_name)

            # Read the file
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()

                # Search for patterns in the file content
                matches = pattern.findall(content)

                # Extract text from matches and add to set
                for match in matches:
                    text_set.add(match[1])

    return list(text_set)  # Convert set back to list before returning

# Example usage:
folder_path = 'C:\\Users\\alalfy\\IdeaProjects\\followers-backend'
texts = find_text_in_files(folder_path)
print(texts)
