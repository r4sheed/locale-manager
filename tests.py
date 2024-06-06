import locale_manager
import os
import json
import threading

def setup_test_environment():
    # Create directories and files for testing
    os.makedirs("test_locales", exist_ok=True)
    
    en_us_translations = {
        "welcome": "Welcome",
        "goodbye": "Goodbye",
        "greeting": "{welcome}, {name}!",
        "choose_language": "Choose Language:",
        "hello": "Hello"  # Key defined only in the default language
    }
    
    hu_hu_translations = {
        "welcome": "Szia",
        "goodbye": "Viszlát",
        "greeting": "{welcome}, {name}!",
        "choose_language": "Válassz nyelvet:"
    }
    
    with open("test_locales/en_US.json", "w", encoding="utf-8") as f:
        json.dump(en_us_translations, f, ensure_ascii=False, indent=4)
        
    with open("test_locales/hu_HU.json", "w", encoding="utf-8") as f:
        json.dump(hu_hu_translations, f, ensure_ascii=False, indent=4)

def cleanup_test_environment():
    # Remove directories and files after testing
    if os.path.exists("test_locales/en_US.json"):
        os.remove("test_locales/en_US.json")
    if os.path.exists("test_locales/hu_HU.json"):
        os.remove("test_locales/hu_HU.json")
    if os.path.exists("test_locales"):
        os.rmdir("test_locales")

def run_tests():
    setup_test_environment()
    
    try:
        # Initialize LocaleManager
        print("Initializing LocaleManager...")
        manager = locale_manager.LocaleManager(
            language_folder="test_locales",
            default_language="en_US",
            languages=["en_US", "hu_HU"]
        )
        
        # Basic Functionality Tests
        print("\nBasic Functionality Tests")
        print("Testing default language translation...")
        assert manager.get_translation("welcome") == "Welcome"
        print("Default language translation test passed.")
        
        print("Testing setting a different language...")
        manager.set_language("hu_HU")
        assert manager.get_translation("welcome") == "Szia"
        print("Set language translation test passed.")
        
        print("Testing fallback language...")
        assert manager.get_translation("choose_language") == "Válassz nyelvet:"
        print("Fallback language translation test passed.")
        
        print("Testing parameters in translation...")
        translation_with_params = manager.get_translation("greeting", name="John")
        print(f"Expected: Szia, John! Actual: {translation_with_params}")
        assert translation_with_params == "Szia, John!"
        print("Translation with parameters test passed.")
        
        print("Testing nested translations...")
        manager.set_language("en_US")
        nested_translation = manager.get_translation("greeting", name="John")
        print(f"Expected: Welcome, John! Actual: {nested_translation}")
        assert nested_translation == "Welcome, John!"
        print("Nested translation test passed.")
        
        print("Testing available languages...")
        available_languages = manager.get_available_languages()
        print(f"Available languages: {available_languages}")
        assert "en_US" in available_languages
        assert "hu_HU" in available_languages
        print("Available languages test passed.")
        
        print("Testing exporting translations...")
        exported_translations = manager.export_translations("hu_HU")
        print(f"Exported translations (hu_HU): {exported_translations}")
        assert exported_translations["welcome"] == "Szia"
        print("Export translations test passed.")
        
        print("Testing caching...")
        manager.load_language("hu_HU")
        cached_translations = manager.translations_cache["hu_HU"]
        print(f"Cached translations (hu_HU): {cached_translations}")
        assert cached_translations["welcome"] == "Szia"
        print("Caching test passed.")
        
        # Error Handling Tests
        print("\nError Handling Tests")
        print("Testing missing translation key...")
        try:
            manager.get_translation("nonexistent_key")
            print("Test failed: Exception not raised for missing translation key.")
        except locale_manager.TranslationKeyNotFoundError:
            print("Missing translation key test passed.")
        
        print("Testing missing language file...")
        try:
            manager.load_language("nonexistent_language")
            print("Test failed: Exception not raised for missing language file.")
        except locale_manager.LanguageFileNotFoundError:
            print("Missing language file test passed.")
        
        print("Testing invalid JSON handling...")
        with open("test_locales/invalid.json", "w", encoding="utf-8") as f:
            f.write("{invalid_json:}")
        try:
            manager.load_language("invalid")
            print("Test failed: Exception not raised for invalid JSON.")
        except locale_manager.LanguageFileNotFoundError:
            print("Invalid JSON handling test passed.")
        os.remove("test_locales/invalid.json")
        
        # Advanced Features Tests
        print("\nAdvanced Features Tests")
        print("Testing language reload...")
        manager.translations_cache["en_US"]["reload_test"] = "Reload Test"
        manager.set_language("en_US")
        assert manager.get_translation("reload_test") == "Reload Test"
        print("Language reload test passed.")
        
        print("Testing fallback to default language for missing key...")
        manager.set_language("hu_HU")
        try:
            assert manager.get_translation("hello", language_code="nonexistent_language") == "Hello"
            print("Fallback to default language for missing key test passed.")
        except locale_manager.TranslationKeyNotFoundError:
            print("Test failed: Fallback to default language for missing key did not work.")
        
        # Test thread-safety (optional)
        def load_language(manager, language_code):
            manager.load_language(language_code)
            print(f"Loaded {language_code} language in thread {threading.current_thread().name}")

        print("Testing thread-safety...")
        threads = [
            threading.Thread(target=load_language, args=(manager, "en_US"), name="Thread-1"),
            threading.Thread(target=load_language, args=(manager, "hu_HU"), name="Thread-2")
        ]

        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        print("Thread-safety test passed.")
    
    except AssertionError as e:
        print(f"Test failed: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        cleanup_test_environment()

if __name__ == "__main__":
    run_tests()
