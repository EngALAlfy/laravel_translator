import os
import re
import sys
import json
from deep_translator import GoogleTranslator
from tqdm import tqdm

def find_text_in_files(folder_path , ignored_folders=None):
    """
    Find text patterns in PHP files within the specified folder and its subfolders.

    Args:
        folder_path (str): Path to the folder to search for PHP files.

    Returns:
        list: A list of unique text patterns found in the PHP files.
    """
    if ignored_folders is None:
        ignored_folders = []
    
    try:
        text_set = set()  # Use a set to automatically avoid duplicates

        pattern = re.compile(r'__\(([\'"])([^\'"]+)\1\)')
        pattern = re.compile(r'[@]lang\(([\'"])([^\'"]+)\1\)|__\(([\'"])([^\'"]+)\3\)')
        # Walk through each file in the folder and its subfolders
        for root, dirs, files in os.walk(folder_path):
            # Remove ignored folders from the list of directories to avoid traversing them
            dirs[:] = [d for d in dirs if d not in ignored_folders]
        
            for file_name in files:
                # Skip non-PHP files
                if not file_name.endswith('.php'):
                    continue
                
                file_path = os.path.join(root, file_name)

                # Read the file
                try:
                    with open(file_path, 'r', encoding='utf-8') as file:
                        content = file.read()

                        # Search for patterns in the file content
                        matches = pattern.findall(content)

                        # Extract text from matches and add to set
                        for match in matches:
                            for group in match:
                                if group:
                                    text_set.add(group)
                except UnicodeDecodeError as e:
                    print(f"Error decoding file {file_path}: {e}")
        return list(text_set)  # Convert set back to list before returning
    except Exception as e:
        print(f"Error occurred while searching for text patterns: {e}")
        return []

def clean_text_list(text_list):
    """
    Clean a list of text patterns by removing empty strings, single quotes, double quotes,
    and patterns containing 'wireui'.

    Args:
        text_list (list): List of text patterns to clean.

    Returns:
        list: A cleaned list of text patterns.
    """
    try:
        cleaned_list = []
        for text in text_list:
            if text and text != "'" and text != '"' and 'wireui' not in text:
                cleaned_list.append(text)
        return cleaned_list
    except Exception as e:
        print(f"Error occurred while cleaning text patterns: {e}")
        return []

def translate_to_arabic(texts):
    """
    Translate a list of texts from the source language to Arabic using Google Translate API.

    Args:
        texts (list): List of texts to translate.

    Returns:
        dict: A dictionary mapping original texts to their Arabic translations.
    """
    try:
        translator = GoogleTranslator(source='auto', target='ar')
        ar_texts = {}
        with tqdm(total=len(texts), unit=' word', ncols=80, nrows=10, colour="green", desc="Translate into Arabic") as pbar:
            for text in texts:
                try:
                    translation = translator.translate(text)
                    ar_texts[text] = translation
                    pbar.update(1)
                except Exception as e:
                    print(f"Error occurred while translating '{text}': {e}")
        return ar_texts
    except Exception as e:
        print(f"Error occurred during translation: {e}")
        return {}

if __name__ == "__main__":
    try:
        if len(sys.argv) != 2:
            print("Usage: python script.py /path/to/folder")
            sys.exit(1)
        
        folder_path = sys.argv[1]
        if not os.path.isdir(folder_path):
            print("Invalid directory path provided.")
            sys.exit(1)

        # Extract texts
        texts = find_text_in_files(folder_path, ignored_folders=["vendor" , "node_modules" , "public" , "storage" , "lang" , "bootstrap"])

        # Clean the list of texts
        cleaned_texts = clean_text_list(texts)

        # Separate texts into Arabic and English translations
        # Translate texts to Arabic
        ar_texts = translate_to_arabic(cleaned_texts)
        en_texts = cleaned_texts.copy()

        # Extract project name from folder path
        project_name = os.path.basename(os.path.normpath(folder_path))

        # Create the output directory if it doesn't exist
        output_dir = os.path.join("output", project_name)
        os.makedirs(output_dir, exist_ok=True)

        # Write English translations to en.json
        with open(os.path.join(output_dir, "en.json"), 'w') as en_file:
            json.dump({text: text for text in en_texts}, en_file, indent=4)
        print(f"English translations have been saved to {project_name}/en.json")

        # Write Arabic translations to ar.json
        with open(os.path.join(output_dir, "ar.json"), 'w', encoding='utf-8') as ar_file:
            json.dump(ar_texts, ar_file, indent=4, ensure_ascii=False)
        print(f"Arabic translations have been saved to {project_name}/ar.json")
    except KeyboardInterrupt:
        print("\nTranslation interrupted. Exiting gracefully.")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")