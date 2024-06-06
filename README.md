# LocaleManager

**LocaleManager** is a Python class to manage localization and translations. It provides functionalities to load, cache, and manage language files, handle missing translations, and switch between different languages.

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

```
import locale_manager

manager = locale_manager.LocaleManager(
    language_folder="locales",
    default_language="en_US",
    fallback_language="en_US",
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

#### `load_language(language_code)`
Loads the specified language file, utilizing the cache if available.

**Parameters:**
- `language_code` (str): Language code to load.

**Returns:**
- `dict`: Dictionary of translations.

#### `save_language_file(language_file, translations)`
Saves the language file with the provided translations.

**Parameters:**
- `language_file` (str): Path to the language file to save.
- `translations` (dict): Dictionary of translations to save.

#### `get_available_languages()`
Returns a list of available languages based on the files in the language folder.

**Returns:**
- `list`: List of available language codes.

#### `get_translation(key, language_code=None, **params)`
Gets the translation for the specified key, handling nested translations and parameters.

**Parameters:**
- `key` (str): Translation key.
- `language_code` (str, optional): Optional language code to use for translation.
- `params` (dict): Parameters to format into the translation string.

**Returns:**
- `str`: Translated string.

#### `set_language(language_code)`
Sets the current language for translations.

**Parameters:**
- `language_code` (str): Language code to set.

#### `reload_language()`
Reloads the translations for the current language.

#### `export_translations(language_code)`
Exports all loaded translations for a specific language.

**Parameters:**
- `language_code` (str): Language code to export translations for.

**Returns:**
- `dict`: Dictionary of translations.

### Examples

#### Set Language and Get Translation

```
manager.set_language("en_US")
print(manager.get_translation("welcome"))  # Output: Welcome
```

#### Get Translation for a Specific Language

```
print(manager.get_translation("greeting", language_code="hu_HU", name="John"))  # Output: Szevasz John!
```

#### List Available Languages

```
print(manager.get_available_languages())  # Output: ['en_US', 'hu_HU', 'de_DE']
```

#### Reload Current Language Translations

```
manager.reload_language()
```

#### Export Translations for a Specific Language

```
exported_translations = manager.export_translations("en_US")
print(exported_translations)
```

## Error Handling

The `LocaleManager` class raises specific exceptions for different error conditions:

- `LanguageFileNotFoundError`: Raised when a language file is not found.
- `TranslationKeyNotFoundError`: Raised when a translation key is not found.

### Example

```
try:
    manager.set_language("fr_FR")
except locale_manager.LanguageFileNotFoundError as e:
    print(f"Error: {e}")
```

## Contributing

If you would like to contribute to this project, please fork the repository and create a pull request with your changes. Ensure that your code follows the project's coding standards and includes tests for any new functionality.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
