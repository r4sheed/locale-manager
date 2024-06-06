import locale_manager
import os
import json

def setup_test_environment():
    # Create directories and files for testing
    os.makedirs("test_locales", exist_ok=True)
    
    en_us_translations = {
        "welcome": "Welcome",
        "goodbye": "Goodbye",
        "greeting": "Hello, {name}!",
        "choose_language": "Choose Language:"
    }
    
    hu_hu_translations = {
        "welcome": "Szia",
        "goodbye": "Viszlát",
        "greeting": "Szia, {name}!",
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
        manager = locale_manager.LocaleManager(
            language_folder="test_locales",
            default_language="en_US",
            languages=["en_US", "hu_HU"],
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
                }
            }
        )
        
        # Test default language translation
        assert manager.get_translation("welcome") == "Welcome"
        print("Default language translation test passed.")
        
        # Test setting a different language
        manager.set_language("hu_HU")
        assert manager.get_translation("welcome") == "Szia"
        print("Set language translation test passed.")
        
        # Test fallback language
        manager.set_language("hu_HU")
        assert manager.get_translation("choose_language") == "Válassz nyelvet:"
        print("Fallback language translation test passed.")
        
        # Test parameters in translation
        assert manager.get_translation("greeting", name="John") == "Szia John!"
        print("Translation with parameters test passed.")
        
        # Test nested translations
        manager.set_language("en_US")
        assert manager.get_translation("greeting", name="John") == "Welcome John!"
        print("Nested translation test passed.")
        
        # Test available languages
        available_languages = manager.get_available_languages()
        assert "en_US" in available_languages
        assert "hu_HU" in available_languages
        print("Available languages test passed.")
        
        # Test exporting translations
        exported_translations = manager.export_translations("hu_HU")
        assert exported_translations["welcome"] == "Szia"
        print("Export translations test passed.")
        
        # Test caching
        manager.load_language("hu_HU")
        assert manager.translations_cache["hu_HU"]["welcome"] == "Szia"
        print("Caching test passed.")
    
    except AssertionError as e:
        print(f"Test failed: {e}")
    finally:
        cleanup_test_environment()

if __name__ == "__main__":
    run_tests()
