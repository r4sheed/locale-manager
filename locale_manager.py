import json
import os
import re
from typing import Dict, Optional, List, Tuple
from collections import OrderedDict

class LanguageFileNotFoundError(Exception):
    """Custom exception for when a language file is not found."""
    pass

class TranslationKeyNotFoundError(Exception):
    """Custom exception for when a translation key is not found."""
    pass

class LocaleManager:
    """Class to manage localization and translations."""

    def __init__(self, language_folder: str = "locales", default_language: str = "en_US", languages: Optional[List[str]] = None, translations: Optional[Dict[str, Dict[str, str]]] = None):
        """
        Initializes the LocaleManager class with the specified language folder, default language, predefined languages, and predefined translations.

        :param language_folder: Directory where language files are stored.
        :param default_language: Default language to use. Defaults to "en_US".
        :param languages: List of predefined language codes.
        :param translations: Dictionary of predefined translations.
        """
        if not languages:
            raise ValueError("languages must be specified")

        self.language_folder = language_folder
        self.default_language = default_language
        self.current_language = default_language
        self.languages = languages
        self.predefined_translations = translations or {}
        self.translations_cache = {}
        self.translations = {}

        # Ensure all predefined language files exist and contain all keys
        self.ensure_predefined_language_files()

        # Load default language translations
        self.translations = self.load_language(self.default_language)

    def ensure_predefined_language_files(self) -> None:
        """Ensures that all predefined language files exist and contain all predefined keys without overwriting existing values."""
        os.makedirs(self.language_folder, exist_ok=True)

        for language_code, predefined_trans in self.predefined_translations.items():
            language_file = os.path.join(self.language_folder, f"{language_code}.json")
            if os.path.exists(language_file):
                with open(language_file, 'r', encoding='utf-8') as file:
                    translations = json.load(file)
                    if not isinstance(translations, dict):
                        translations = {}
            else:
                translations = {}

            updated_translations, updated = self.ensure_all_keys(translations, predefined_trans)

            # Only save if there are changes or if the file doesn't exist
            if updated or not os.path.exists(language_file):
                ordered_translations = self.order_keys_as_predefined(updated_translations, predefined_trans)
                with open(language_file, 'w', encoding='utf-8') as file:
                    json.dump(ordered_translations, file, ensure_ascii=False, indent=4)

    def ensure_all_keys(self, current_translations: Dict[str, str], predefined_translations: Dict[str, str]) -> Tuple[Dict[str, str], bool]:
        """
        Ensures all keys from the predefined translations are present in the loaded translations without overwriting existing values.

        :param current_translations: Dictionary of currently loaded translations.
        :param predefined_translations: Dictionary of predefined translations.
        :return: Updated dictionary of translations and a boolean indicating if there were any updates.
        """
        updated = False
        for key, value in predefined_translations.items():
            if key not in current_translations:
                current_translations[key] = value
                updated = True
        return current_translations, updated

    def order_keys_as_predefined(self, translations: Dict[str, str], predefined_translations: Dict[str, str]) -> OrderedDict:
        """
        Orders the keys in translations as in predefined_translations.

        :param translations: Dictionary of translations to be ordered.
        :param predefined_translations: Dictionary of predefined translations to determine the order.
        :return: Ordered dictionary of translations.
        """
        ordered_translations = OrderedDict()
        for key in predefined_translations:
            if key in translations:
                ordered_translations[key] = translations[key]
        return ordered_translations

    def load_language(self, language_code: str) -> Dict[str, str]:
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

        try:
            with open(language_file, 'r', encoding='utf-8') as file:
                translations = json.load(file)
                if not isinstance(translations, dict):
                    translations = {}
        except json.JSONDecodeError as e:
            raise LanguageFileNotFoundError(f"Error loading language file {language_file}: {e}")

        predefined_trans = self.predefined_translations.get(language_code, {})
        updated_translations, updated = self.ensure_all_keys(translations, predefined_trans)

        if updated:
            ordered_translations = self.order_keys_as_predefined(updated_translations, predefined_trans)
            self.save_language_file(language_file, ordered_translations)
            self.translations_cache[language_code] = ordered_translations
        else:
            self.translations_cache[language_code] = translations

        return self.translations_cache[language_code]

    def save_language_file(self, language_file: str, translations: Dict[str, str]) -> None:
        """
        Saves the language file with the provided translations.

        :param language_file: Path to the language file to save.
        :param translations: Dictionary of translations to save.
        """
        with open(language_file, 'w', encoding='utf-8') as file:
            json.dump(translations, file, ensure_ascii=False, indent=4)

    def get_available_languages(self) -> List[str]:
        """
        Returns a list of available languages based on the files in the language folder.

        :return: List of available language codes.
        """
        available_languages = [f.split('.')[0] for f in os.listdir(self.language_folder) if f.endswith('.json')]
        return [lang for lang in self.languages if lang in available_languages]

    def get_translation(self, key: str, language_code: Optional[str] = None, **params) -> str:
        """
        Gets the translation for the specified key, handling nested translations and parameters.

        :param key: Translation key.
        :param language_code: Optional language code to use for translation.
        :param params: Parameters to format into the translation string.
        :return: Translated string.
        """
        language_code = language_code or self.current_language

        try:
            translations = self.translations if language_code == self.default_language else self.load_language(language_code)
        except LanguageFileNotFoundError:
            translations = self.translations

        if key not in translations and language_code != self.default_language:
            try:
                translations = self.load_language(self.default_language)
            except LanguageFileNotFoundError:
                translations = {}

        if key not in translations:
            raise TranslationKeyNotFoundError(f"Translation key '{key}' not found in both {language_code} and default language {self.default_language}!")

        translation = translations[key]

        def replace_nested(match):
            nested_key = match.group(1)
            return translations.get(nested_key, match.group(0))

        translation = re.sub(r'\{(\w+)\}', replace_nested, translation)

        if params:
            translation = translation.format(**params)
        return translation

    def set_language(self, language_code: str) -> None:
        """
        Sets the current language for translations.

        :param language_code: Language code to set.
        """
        if language_code not in self.languages:
            raise ValueError(f"Language '{language_code}' is not supported.")
        
        if language_code in self.translations_cache:
            self.translations = self.translations_cache[language_code]
        else:
            self.translations = self.load_language(language_code)
        self.current_language = language_code

    def export_translations(self, language_code: str) -> Dict[str, str]:
        """
        Exports all loaded translations for a specific language.

        :param language_code: Language code to export translations for.
        :return: Dictionary of translations.
        """
        return self.load_language(language_code)
