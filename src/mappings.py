# Phonetic mappings for Marathi

# Vowels (Independent)
VOWELS = {
    'a': 'अ',
    'aa': 'आ',
    'i': 'इ',
    'ee': 'ई',
    'u': 'उ',
    'oo': 'ऊ',
    'e': 'ए',
    'ai': 'ऐ',
    'o': 'ओ',
    'au': 'औ',
    'M': 'अं',
    'H': 'अः',
    'r': 'ऋ',
}

# Matras (Dependent Vowels)
# '' represents the inherent 'a' (schwa)
MATRAS = {
    'a': '',      # Inherent a
    'aa': 'ा',
    'i': 'ि',
    'ee': 'ी',
    'u': 'ु',
    'oo': 'ू',
    'e': 'े',
    'ai': 'ै',
    'o': 'ो',
    'au': 'ौ',
    'M': 'ं',
    'H': 'ः',
    'r': 'ृ', 
}

# Consonants
# These are mapped to their unicode char.
# NOTE: The logic should handle adding Halant (्) if not followed by a vowel.
# But conventionally, we store the base char 'क'.
# If we store 'क', it implies 'ka'.
# If we want pure consonant value, it is 'क' + '्'.
# Strategy: Store as base 'ka' form ('क'). 
# In logic: 
#   If C + C, add Halant to first C. 
#   If C + V, apply Matra to C. 
#   If C + Space/End, usually keep as 'C' (implied 'a') or 'C+Halant' depending on convention.
#   Hindi/Marathi usually implies 'a' at end unless explicitly halted, but sometimes halant is explicit. 
#   Let's assume implicit 'a' (schwa) for now, as in 'Namaskar' -> 'r' is 'र' (ra) not 'र्' (r-halant) strictly, though pronounced 'r'.
CONSONANTS = {
    'k': 'क', 'kh': 'ख', 'g': 'ग', 'gh': 'घ', 'ng': 'ङ',
    'ch': 'च', 'chh': 'छ', 'j': 'ज', 'z': 'झ', 'jh': 'झ', 'ny': 'ञ',
    't': 'ट', 'th': 'ठ', 'd': 'ड', 'dh': 'ढ', 'n': 'ण',
    't': 'त', 'th': 'थ', 'd': 'द', 'dh': 'ध', 'n': 'न', # Note: t/th/d/dh/n ambiguous for retroflex/dental. Usually mapped by context or capitalization. Let's simple map lowercase to dental (common) and Upper to retroflex? Or assume dental is default.
    # Let's map 'T', 'D', 'N' to retroflex for differentiation if users use it.
    'p': 'प', 'ph': 'फ', 'f': 'फ', 'b': 'ब', 'bh': 'भ', 'm': 'म',
    'y': 'य', 'r': 'र', 'l': 'ल', 'v': 'व', 'w': 'व',
    'sh': 'श', 's': 'स', 'ss': 'ष', 'shh': 'ष',
    'h': 'ह', 'l': 'ळ', 'ksh': 'क्ष', 'dny': 'ज्ञ',
}

# Corrections/Overwrites for specific multi-char inputs to ensure greedy match
# Sorted by length descending in logic
SPECIAL_CONSONANTS = {
    'sh': 'श',
    'shh': 'ष',
    'ksh': 'क्ष',
    'dny': 'ज्ञ',
    'kh': 'ख',
    'gh': 'घ',
    'ch': 'च',
    'chh': 'छ',
    'jh': 'झ',
    'th': 'थ',
    'dh': 'ध',
    'ph': 'फ',
    'bh': 'भ',
}

# Retroflex explicit mapping (optional, common convention)
RETROFLEX_CONSONANTS = {
    'T': 'ट',
    'Th': 'ठ',
    'D': 'ड',
    'Dh': 'ढ',
    'N': 'ण',
    'L': 'ळ',
}

CONSONANTS.update(SPECIAL_CONSONANTS)
CONSONANTS.update(RETROFLEX_CONSONANTS)

NUMERALS = {
    '0': '०', '1': '१', '2': '२', '3': '३', '4': '४',
    '5': '५', '6': '६', '7': '७', '8': '८', '9': '९'
}
