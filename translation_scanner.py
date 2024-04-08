import os
import re
import sys

def find_text_in_files(folder_path):
    text_set = set()  # Use a set to automatically avoid duplicates

    # Regular expression to match patterns like @lang("x"), @lang('x'), __("x"), or __('x')
    pattern = re.compile(r'[@]lang\(([\'"])([^\'"]+)\1\)|__\(([\'"])([^\'"]+)\3\)')

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
                    for group in match:
                        if group:
                            text_set.add(group)

    return list(text_set)  # Convert set back to list before returning

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py /path/to/project")
        sys.exit(1)
    
    folder_path = sys.argv[1]
    if not os.path.isdir(folder_path):
        print("Invalid directory path provided.")
        sys.exit(1)

    texts = find_text_in_files(folder_path)
    print(texts)
    print(len(texts))