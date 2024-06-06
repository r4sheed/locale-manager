# Home

**LocaleManager** is a Python class to manage localization and translations. It provides functionalities to load, cache, and manage language files, handle missing translations, and switch between different languages.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
  - [Initialization](#initialization)
  - [Methods](#methods)
  - [Examples](#examples)
- [Error Handling](#error-handling)
- [Contributing](#contributing)
- [License](#license)
- [Sample Script](#sample-script)

## Features

- Load and manage language files from a specified directory
- Cache translations for improved performance
- Support for fallback language if a translation key is not found
- Handle nested translations and parameters
- Export translations for a specific language
- Easily switch between different languages

## Installation

To use the `LocaleManager` class, you can simply clone the repository and import the class in your project.

```
git clone https://github.com/r4sheed/locale-manager.git
```

## Usage

### Initialization

To initialize the `LocaleManager`, you need to specify the directory where language files are stored, the default language, and the list of supported languages. Optionally, you can also provide predefined translations.

```python
import locale_manager

manager = locale_manager.LocaleManager(
    language_folder="locales",
    default_language="en_US",
    languages=["en_US", "hu_HU", "de_DE"],
    translations={
        "en_US": {
            "welcome": "Welcome",
            "goodbye": "Goodbye",
            "greeting": "{welcome} {name}!"
        },
        "hu_HU": {
            "welcome": "Szia",
            "goodbye": "Viszlát",
            "greeting": "{welcome} {name}!"
        },
        "de_DE": {
            "welcome": "Willkommen",
            "goodbye": "Auf Wiedersehen",
            "greeting": "{welcome} {name}!"
        },
    }
)
```

### Methods

#### `ensure_predefined_language_files()`
Ensures that all predefined language files exist and contain all predefined keys.

**Example**
```python
manager.ensure_predefined_language_files()
```

#### `load_language(language_code)`
Loads the specified language file, utilizing the cache if available.

**Parameters:**
- `language_code` (str): Language code to load.

**Returns:**
- `dict`: Dictionary of translations.

**Example**
```python
translations = manager.load_language("en_US")
print(translations)
```

#### `save_language_file(language_file, translations)`
Saves the language file with the provided translations.

**Parameters:**
- `language_file` (str): Path to the language file to save.
- `translations` (dict): Dictionary of translations to save.

**Example**
```python
manager.save_language_file("locales/en_US.json", {"welcome": "Welcome"})
```

#### `get_available_languages()`
Returns a list of available languages based on the files in the language folder.

**Returns:**
- `list`: List of available language codes.

**Example**
```python
available_languages = manager.get_available_languages()
print(available_languages)  # Output: ['en_US', 'hu_HU', 'de_DE']
```

#### `get_translation(key, language_code=None, **params)`
Gets the translation for the specified key, handling nested translations and parameters.

**Parameters:**
- `key` (str): Translation key.
- `language_code` (str, optional): Optional language code to use for translation.
- `params` (dict): Parameters to format into the translation string.

**Returns:**
- `str`: Translated string.

**Example**
```python
translation = manager.get_translation("greeting", name="John")
print(translation)  # Output: Welcome John!
```

#### `set_language(language_code)`
Sets the current language for translations.

**Parameters:**
- `language_code` (str): Language code to set.

**Example**
```python
manager.set_language("hu_HU")
print(manager.get_translation("welcome"))  # Output: Szia
```

#### `export_translations(language_code)`
Exports all loaded translations for a specific language.

**Parameters:**
- `language_code` (str): Language code to export translations for.

**Returns:**
- `dict`: Dictionary of translations.

**Example**
```python
exported_translations = manager.export_translations("en_US")
print(exported_translations)
```

### Examples

#### Set Language and Get Translation

```python
manager.set_language("en_US")
print(manager.get_translation("welcome"))  # Output: Welcome
```

#### Get Translation for a Specific Language

```python
print(manager.get_translation("greeting", language_code="hu_HU", name="John"))  # Output: Szevasz John!
```

#### List Available Languages

```python
print(manager.get_available_languages())  # Output: ['en_US', 'hu_HU', 'de_DE']
```

#### Export Translations for a Specific Language

```python
exported_translations = manager.export_translations("en_US")
print(exported_translations)
```

## Error Handling

The `LocaleManager` class raises specific exceptions for different error conditions:

- `LanguageFileNotFoundError`: Raised when a language file is not found.
- `TranslationKeyNotFoundError`: Raised when a translation key is not found.

### Example

```python
try:
    manager.set_language("fr_FR")
except locale_manager.LanguageFileNotFoundError as e:
    print(f"Error: {e}")
```

## Contributing

If you would like to contribute to this project, please fork the repository and create a pull request with your changes. Ensure that your code follows the project's coding standards and includes tests for any new functionality.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Sample Script

Here is a sample script that demonstrates how to use the `LocaleManager` class:

```python
import locale_manager

def main():
    manager = locale_manager.LocaleManager(
        language_folder="locales",
        default_language="en_US",
        languages=["en_US", "hu_HU", "de_DE"],
        translations={
            "en_US": {
                "welcome": "Welcome",
                "goodbye": "Goodbye",
                "greeting": "{welcome} {name}!"
            },
            "hu_HU": {
                "welcome": "Szia",
                "goodbye": "Viszlát",
                "greeting": "{welcome} {name}!"
            },
            "de_DE": {
                "welcome": "Willkommen",
                "goodbye": "Auf Wiedersehen",
                "greeting": "{welcome} {name}!"
            },
        }
    )

    # Set language and get translation
    manager.set_language("en_US")
    print(manager.get_translation("welcome"))  # Output: Welcome

    # Get translation for a specific language
    print(manager.get_translation("greeting", language_code="hu_HU", name="John"))  # Output: Szia John!

    # List available languages
    print(manager.get_available_languages())  # Output: ['en_US', 'hu_HU', 'de_DE']

    # Export translations for a specific language
    exported_translations = manager.export_translations("en_US")
    print(exported_translations)

if __name__ == "__main__":
    main()
```
