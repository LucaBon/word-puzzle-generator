"""Build the per-language word lists used by the web demo (dictionaries/<lang>.txt).

Words come from the wordfreq frequency lists (most common first). A word is kept only if
  - the Hunspell dictionary for the language accepts it (drops names, slang and typos),
  - it is not in the LDNOOBW list of offensive words, also catching inflected forms
    (FUCKS, FUCKED from FUCK; CAZZI from CAZZO). Ordinary words that the list includes for a
    slang meaning (REGINA, PESCE, PEDALE, ...) are kept, see NOT_OFFENSIVE and ALWAYS_KEEP,
  - it has 3-15 letters once written in plain A-Z (accents removed, German umlauts as AE/OE/UE).

Requirements: pip install wordfreq spylls

Usage: python scripts/build_dictionaries.py [--size 50000] [--cache DIR]
"""

import argparse
import tempfile
import unicodedata
import urllib.request
from pathlib import Path

from spylls.hunspell import Dictionary
from wordfreq import top_n_list

LANGUAGES = {'en': 'en-us', 'it': 'it', 'es': 'es', 'fr': 'fr', 'de': 'de'}
HUNSPELL_URL = 'https://cdn.jsdelivr.net/npm/dictionary-{pkg}/index.{ext}'
BAD_WORDS_URL = ('https://raw.githubusercontent.com/LDNOOBW/'
                 'List-of-Dirty-Naughty-Obscene-and-Otherwise-Bad-Words/master/{lang}')
SPECIAL_LETTERS = {'ä': 'ae', 'ö': 'oe', 'ü': 'ue', 'ß': 'ss', 'æ': 'ae', 'œ': 'oe'}
VOWELS = 'AEIOU'
INFLECTION_ENDINGS = ('S', 'ES', 'ED', 'ING', 'EN', 'T', 'ST')
NOT_OFFENSIVE = {
    'en': {'escort', 'domination', 'eunuch', 'snatch', 'hardcore', 'fingering'},
    'it': {'battere', 'balle', 'palle', 'biga', 'cadavere', 'cozza', 'fava', 'finocchio', 'monta', 'montare',
           'pesce', 'pompa', 'porca', 'porco', 'quaglia', 'regina', 'spagnola', 'tirare', 'vacca', 'vangare',
           'sega', 'patacca', 'sbattere', 'cagna', 'bagnarsi', 'pistolotto', 'ingoio', 'rizzarsi'},
    'es': {'asesinato', 'asno', 'concha', 'drogas', 'infierno', 'martillo', 'maldito', 'orina', 'trio',
           'racista', 'maciza'},
    'fr': {'baiser', 'bander', 'bordel', 'bourré', 'bourrée', 'folle', 'gerbe', 'gueule', 'jouir', 'pédale',
           'péter', 'ramoner', 'tanche', 'trique', 'bitte'},
    'de': {'bonze', 'fratze', 'kimme', 'mufti', 'nackt', 'popel', 'rosette'},
}
# Offensive words missing from the LDNOOBW lists
EXTRA_OFFENSIVE = {
    'en': {'arse', 'arsed', 'crap', 'bugger', 'wanker', 'prick', 'piss', 'pissed', 'bollock'},
    'it': set(), 'es': set(), 'fr': set(), 'de': set(),
}
# Harmless words that look like an inflected form of an offensive one
ALWAYS_KEEP = {
    'en': {'BUTTING', 'SPICING'},
    'it': {'TETTO', 'TETTI', 'PECORINO', 'CESSA', 'SORCI', 'BATTONO', 'CACCE', 'CASCA', 'CASCO', 'MUSSO'},
    'es': {'PINCHA', 'PINCHO'},
    'fr': set(),
    'de': set(),
}
MIN_LENGTH, MAX_LENGTH = 3, 15
CANDIDATES_PER_WORD = 4  # frequency-list entries read for each word we want to keep

OUTPUT_DIR = Path(__file__).resolve().parent.parent / 'dictionaries'


def download(url: str, target: Path) -> Path:
    if not target.exists():
        with urllib.request.urlopen(url) as response:
            target.write_bytes(response.read())
    return target


def to_plain_letters(word: str) -> str:
    word = ''.join(SPECIAL_LETTERS.get(ch, ch) for ch in word.lower())
    decomposed = unicodedata.normalize('NFD', word)
    return ''.join(ch for ch in decomposed if not unicodedata.combining(ch)).upper()


def load_bad_words(lang: str, cache: Path) -> set:
    path = download(BAD_WORDS_URL.format(lang=lang), cache / f'bad_{lang}.txt')
    # Multi-word entries are skipped: their single words are often harmless on their own
    lines = [line.strip() for line in path.read_text(encoding='utf-8').splitlines()]
    allowed = {to_plain_letters(word) for word in NOT_OFFENSIVE[lang]}
    words = {line for line in lines if line and ' ' not in line} | EXTRA_OFFENSIVE[lang]
    return {to_plain_letters(word) for word in words} - allowed


def is_offensive(word: str, bad_words: set) -> bool:
    if word in bad_words or any(word.endswith(end) and word[:-len(end)] in bad_words
                                for end in INFLECTION_ENDINGS):
        return True
    # Same stem with a different final vowel, e.g. CAZZI / CAZZO
    stem = word[:-1]
    return (len(stem) >= 4 and word[-1] in VOWELS
            and any(bad[:-1] == stem and bad[-1] in VOWELS for bad in bad_words))


def is_known(dictionary: Dictionary, word: str, lang: str) -> bool:
    if dictionary.lookup(word):
        return True
    # German nouns are capitalised in the dictionary
    return lang == 'de' and dictionary.lookup(word.capitalize())


def build(lang: str, size: int, cache: Path) -> list:
    pkg = LANGUAGES[lang]
    for ext in ('aff', 'dic'):
        download(HUNSPELL_URL.format(pkg=pkg, ext=ext), cache / f'{lang}.{ext}')
    dictionary = Dictionary.from_files(str(cache / lang))
    bad_words = load_bad_words(lang, cache)

    words, seen = [], set()
    for word in top_n_list(lang, size * CANDIDATES_PER_WORD):
        if not word.isalpha():
            continue
        plain = to_plain_letters(word)
        if (not plain.isascii() or not plain.isalpha() or plain in seen
                or not MIN_LENGTH <= len(plain) <= MAX_LENGTH
                or (plain not in ALWAYS_KEEP[lang] and is_offensive(plain, bad_words)) or not is_known(dictionary, word, lang)):
            continue
        seen.add(plain)
        words.append(plain)
        if len(words) == size:
            break
    return words


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--size', type=int, default=50000, help='words per language (default: 50000)')
    parser.add_argument('--cache', type=Path, help='folder for downloaded files (default: a temp folder)')
    parser.add_argument('languages', nargs='*', default=list(LANGUAGES), help='languages to build')
    args = parser.parse_args()

    cache = args.cache or Path(tempfile.mkdtemp(prefix='dictionaries-'))
    cache.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(exist_ok=True)
    for lang in args.languages:
        words = build(lang, args.size, cache)
        (OUTPUT_DIR / f'{lang}.txt').write_text('\n'.join(words) + '\n', encoding='ascii')
        print(f'{lang}: {len(words)} words')


if __name__ == '__main__':
    main()
