# Laravel Translator

Laravel Translator is a Python tool designed to facilitate the translation process within Laravel projects. Its main purpose is to scan a Laravel project and extract all translation keys, making it easier for developers to manage and translate language files manually.

## Features

- Scans Laravel project files to extract translation keys and texts.
- Supports manual translation of extracted texts into language files.
- Automatic translation of extracted texts into specified languages.
- Supports JSON translation for Laravel's `__("x")` and `__('x')` and `@lang('x')` and `@lang("x")` syntax.
- Future plans include implementing AI-powered editing of translations.

## Usage

1. **Installation**: Clone this repository to your local machine.

    ```bash
    git clone https://github.com/EngALAlfy/laravel_translator.git
    ```
2. **Setup**: Ensure you have Python installed on your system. Install the required Python packages by running:

    ```bash
    pip install -r requirements.txt
    ```

3. **Run**: Execute the script with the path to your Laravel project folder as an argument:

    ```bash
    python translation_scanner.py /path/to/your/laravel_project
    ```

4. **Output**: The script will generate English (`en.json`) and Arabic (`ar.json`) translation files under the `output` folder within your project directory.

## Dependencies

- [Python](https://www.python.org/) (3.6 or higher)
- [deep-translator](https://pypi.org/project/deep-translator/)
- [tqdm](https://pypi.org/project/tqdm/)

## Authors

- [@EngAlalfy](https://www.github.com/engalalfy)

## Contributing

Contributions are welcome! If you have any suggestions, bug fixes, or feature requests, feel free to open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).
