import json
import os
import re

class LanguageFileNotFoundError(Exception):
    """Custom exception for when a language file is not found."""
    pass

class TranslationKeyNotFoundError(Exception):
    """Custom exception for when a translation key is not found."""
    pass

class LocaleManager:
    """Class to manage localization and translations."""

    def __init__(self, language_folder="locales", default_language="en_US", fallback_language=None, languages=None, translations=None):
        """
        Initializes the LocaleManager class with the specified language folder, default language, fallback language, predefined languages, and predefined translations.

        :param language_folder: Directory where language files are stored.
        :param default_language: Default language to use. Defaults to "en_US".
        :param fallback_language: Fallback language to use if translation key is not found. Defaults to the default language.
        :param languages: List of predefined language codes.
        :param translations: Dictionary of predefined translations.
        """
        if not languages:
            raise ValueError("languages must be specified")

        self.language_folder = language_folder
        self.default_language = default_language
        self.fallback_language = fallback_language or default_language
        self.languages = languages
        self.predefined_translations = translations or {}
        self.translations_cache = {}
        self.translations = {}

        # Ensure all predefined language files exist and contain all keys
        self.ensure_predefined_language_files()

        self.translations = self.load_language(self.default_language)

    def ensure_predefined_language_files(self):
        """Ensures that all predefined language files exist and contain all predefined keys."""
        os.makedirs(self.language_folder, exist_ok=True)

        for language_code, predefined_trans in self.predefined_translations.items():
            language_file = os.path.join(self.language_folder, f"{language_code}.json")
            translations = {}

            if os.path.exists(language_file):
                with open(language_file, 'r', encoding='utf-8') as file:
                    translations = json.load(file)

            translations.update(predefined_trans)
            self.save_language_file(language_file, translations)

    def load_language(self, language_code):
        """
        Loads the specified language file, utilizing the cache if available.

        :param language_code: Language code to load.
        :return: Dictionary of translations.
        """
        if language_code in self.translations_cache:
            return self.translations_cache[language_code]

        language_file = os.path.join(self.language_folder, f"{language_code}.json")
        if not os.path.exists(language_file):
            raise LanguageFileNotFoundError(f"Translation file for {language_code} not found!")

        with open(language_file, 'r', encoding='utf-8') as file:
            translations = json.load(file)

        predefined_trans = self.predefined_translations.get(language_code, {})
        translations.update(predefined_trans)

        self.save_language_file(language_file, translations)
        self.translations_cache[language_code] = translations
        return translations

    def save_language_file(self, language_file, translations):
        """
        Saves the language file with the provided translations.

        :param language_file: Path to the language file to save.
        :param translations: Dictionary of translations to save.
        """
        with open(language_file, 'w', encoding='utf-8') as file:
            json.dump(translations, file, ensure_ascii=False, indent=4)

    def get_available_languages(self):
        """
        Returns a list of available languages based on the files in the language folder.

        :return: List of available language codes.
        """
        available_languages = [f.split('.')[0] for f in os.listdir(self.language_folder) if f.endswith('.json')]
        return [lang for lang in self.languages if lang in available_languages]

    def get_translation(self, key, language_code=None, **params):
        """
        Gets the translation for the specified key, handling nested translations and parameters.

        :param key: Translation key.
        :param language_code: Optional language code to use for translation.
        :param params: Parameters to format into the translation string.
        :return: Translated string.
        """
        language_code = language_code or self.default_language
        translations = self.translations if language_code == self.default_language else self.load_language(language_code)
        
        if key not in translations:
            # Fallback to default language
            translations = self.load_language(self.fallback_language)
            if key not in translations:
                raise TranslationKeyNotFoundError(f"Translation key '{key}' not found in both {language_code} and fallback language {self.fallback_language}!")

        translation = translations[key]

        # Handle nested translations
        def replace_nested(match):
            nested_key = match.group(1)
            return translations.get(nested_key, match.group(0))

        translation = re.sub(r'\{(\w+)\}', replace_nested, translation)

        if params:
            translation = translation.format(**params)
        return translation

    def set_language(self, language_code):
        """
        Sets the current language for translations.

        :param language_code: Language code to set.
        """
        self.translations = self.load_language(language_code)

    def reload_language(self):
        """
        Reloads the translations for the current language.
        """
        self.translations = self.load_language(self.default_language)

    def export_translations(self, language_code):
        """
        Exports all loaded translations for a specific language.

        :param language_code: Language code to export translations for.
        :return: Dictionary of translations.
        """
        return self.load_language(language_code)
