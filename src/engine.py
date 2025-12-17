import re
from src.mappings import VOWELS, MATRAS, CONSONANTS, NUMERALS

class MarathiEngine:
    def __init__(self):
        # Create a combined dictionary for tokenization, sorted by length descending
        # We need to distinguish between Consonants, Vowels, etc. during processing
        
        self.consonants = CONSONANTS
        self.vowels = VOWELS
        self.numerals = NUMERALS
        self.matras = MATRAS

        # Master map for tokenization
        # Order matters! Longest keys first.
        self.all_keys = list(self.consonants.keys()) + list(self.vowels.keys()) + list(self.numerals.keys())
        self.all_keys.sort(key=len, reverse=True)
        
        # Regex for tokenization
        # Escape keys to handle regex special chars if any
        escaped_keys = [re.escape(k) for k in self.all_keys]
        self.token_pattern = re.compile('|'.join(escaped_keys))
        
        self.halant = '्'

    def tokenize(self, text):
        """
        Greedily tokenize the input text into valid mapping keys.
        Anything not matching a key remains as raw text.
        """
        tokens = []
        scanner = self.token_pattern.scanner(text)
        match = scanner.match()
        last_pos = 0
        
        while match:
            # Check for gaps (unmatched characters)
            if match.start() > last_pos:
                tokens.append(('OTHER', text[last_pos:match.start()]))
            
            # Identify token type
            key = match.group()
            if key in self.consonants:
                tokens.append(('CONSONANT', key))
            elif key in self.vowels:
                tokens.append(('VOWEL', key))
            elif key in self.numerals:
                tokens.append(('NUMERAL', key))
            
            last_pos = match.end()
            match = scanner.match()
            
        # Append remaining text
        if last_pos < len(text):
            tokens.append(('OTHER', text[last_pos:]))
            
        return tokens

    def transliterate(self, text):
        input_text = text.lower() # Normalize case for simpler logic? 
        # Wait, simple 't' vs 'T' logic in mappings implies we should NOT lower everything blindly.
        # But 'Namaskar' -> 'namaskar'.
        # Let's rely on the keys provided. If 'N' is in keys, it maps to Retroflex.
        # If 'n' is in keys, it maps to Dental.
        # If I convert to lower, I lose that distinction.
        # So I will NOT lower() the whole string unless I fail to match.
        # Actually Google Input Tools is usually case-insensitive for general letters but sensitive for T/D/N/L typically.
        # My tokenizer uses keys as defined.
        
        tokens = self.tokenize(text)
        output = []
        
        # Process tokens
        for i, (type, val) in enumerate(tokens):
            
            # Helper to get converted char from last output token
            # We store complex objects in output or just strings? 
            # Strings are easier, but back-modifying strings is annoying.
            # Let's clean the output list at the end.
            
            if type == 'CONSONANT':
                char = self.consonants[val]
                
                # Check previous token to see if we need to add Halant to it
                if i > 0 and tokens[i-1][0] == 'CONSONANT':
                    # Consonant followed by Consonant -> Previous Consonant gets Halant
                    # e.g. s, k -> s becomes half
                    output[-1] = output[-1] + self.halant
                
                output.append(char)
                
            elif type == 'VOWEL':
                # Check context
                if i > 0 and tokens[i-1][0] == 'CONSONANT':
                    # Consonant followed by Vowel -> Apply Matra
                    matra = self.matras.get(val, '')
                    # Note: 'a' maps to '' in matras, so we just append nothing (keeping the full consonant form)
                    output[-1] = output[-1] + matra
                else:
                    # Independent vowel (start of word or after another vowel/other)
                    char = self.vowels[val]
                    output.append(char)
                    
            elif type == 'NUMERAL':
                char = self.numerals[val]
                output.append(char)
                
            elif type == 'OTHER':
                # Just append the raw character (space, punctuation, etc.)
                output.append(val)
                
        return "".join(output)

