import json
import os
import sys
from src.engine import MarathiEngine

class IMController:
    def __init__(self):
        self.engine = MarathiEngine()
        self.static_dictionary = {}
        self.user_dictionary = {}
        
        # Paths
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.static_dict_path = os.path.join(self.base_dir, 'dictionary_data.json')
        
        # User dict path (OS dependent logic could be better, but simple for now)
        # On Linux, typically ~/.local/share/ibus-marathi/user_dict.json
        # On Windows (dev), just local
        if sys.platform.startswith('linux'):
            self.user_data_dir = os.path.expanduser('~/.local/share/maza-marathi')
        else:
            self.user_data_dir = self.base_dir
            
        self.user_dict_path = os.path.join(self.user_data_dir, 'user_dict.json')
        
        self.load_dictionaries()

    def load_dictionaries(self):
        # Load Static
        try:
            if os.path.exists(self.static_dict_path):
                with open(self.static_dict_path, 'r', encoding='utf-8') as f:
                    self.static_dictionary = json.load(f)
        except Exception as e:
            print(f"Warning: Could not load static dictionary: {e}")

        # Load User
        try:
            if os.path.exists(self.user_dict_path):
                with open(self.user_dict_path, 'r', encoding='utf-8') as f:
                    self.user_dictionary = json.load(f)
        except Exception as e:
            print(f"Warning: Could not load user dictionary: {e}")

    def save_user_dictionary(self):
        try:
            if not os.path.exists(self.user_data_dir):
                os.makedirs(self.user_data_dir, exist_ok=True)
            
            with open(self.user_dict_path, 'w', encoding='utf-8') as f:
                json.dump(self.user_dictionary, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error saving user dictionary: {e}")

    def train(self, input_text, selected_word):
        """
        Remember that for 'input_text', the user selected 'selected_word'.
        We promote it to the top of the user dictionary for this input.
        """
        input_lower = input_text.lower()
        
        if input_lower not in self.user_dictionary:
            self.user_dictionary[input_lower] = []
            
        # Remove if exists to re-insert at top
        if selected_word in self.user_dictionary[input_lower]:
            self.user_dictionary[input_lower].remove(selected_word)
            
        self.user_dictionary[input_lower].insert(0, selected_word)
        
        # Keep list size manageable? (e.g. max 10 favorites per word)
        self.user_dictionary[input_lower] = self.user_dictionary[input_lower][:10]
        
        self.save_user_dictionary()

    def get_suggestions(self, input_text):
        """
        Returns a list of 5+ suggestions.
        Priority: User Dict > Static Dict > Strict Transliteration > Fuzzy Variations
        """
        candidates = []
        seen = set()
        input_lower = input_text.lower()
        
        # 1. User Dictionary
        if input_lower in self.user_dictionary:
            for word in self.user_dictionary[input_lower]:
                if word not in seen:
                    candidates.append(word)
                    seen.add(word)
        
        # 2. Static Dictionary
        if input_lower in self.static_dictionary:
            for word in self.static_dictionary[input_lower]:
                if word not in seen:
                    candidates.append(word)
                    seen.add(word)
            
        # 3. Strict Transliteration
        transliterated = self.engine.transliterate(input_text)
        if transliterated not in seen:
            candidates.append(transliterated)
            seen.add(transliterated)
            
        # 4. Generate Variations to fill up to 5 slots
        # We can ask the engine for alternatives or simple heuristic hacks
        if len(candidates) < 5:
            more = self.generate_fuzzy_variations(input_text, transliterated)
            for m in more:
                if m not in seen:
                    candidates.append(m)
                    seen.add(m)
                    
        return candidates[:5]

    def generate_fuzzy_variations(self, input_text, base_transliteration):
        """
        Simple heuristics to generate alternatives when we don't have enough.
        E.g. small 'i' vs big 'I' (pair/matched), or forcing N/n etc.
        """
        variations = []
        
        # Example 1: If word ends in 'a', maybe try without Schwa deletion (explicit Aa) or vice versa?
        # Current engine is greedy.
        
        # Heuristic: Try replacing last char with Halant if it's a consonant ending?
        # Or try different standard mappings.
        
        # Let's try to capitalize first letter to trigger Retroflex if applicable
        # (This depends on engine implementation)
        t_title = self.engine.transliterate(input_text.capitalize())
        variations.append(t_title)
        
        t_upper = self.engine.transliterate(input_text.upper())
        variations.append(t_upper)
        
        # Fake variation: Add Anusvara?
        # variations.append(base_transliteration + 'ं')
        
        return variations

