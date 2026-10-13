# Dictionaries

One file per language (`en`, `it`, `es`, `fr`, `de`) with the 50,000 most common words, one per line,
most common first. They feed the "Whole dictionary" option of the web demo (`index.html`).

Words are written in plain A–Z: accents are removed and German umlauts become AE/OE/UE (ß becomes SS).
Only words of 3–15 letters that the language's Hunspell spell-checker accepts are kept, and offensive
words are filtered out.

Regenerate them with:

```bash
pip install wordfreq spylls
python scripts/build_dictionaries.py
```

## Sources and licenses

- Word frequencies: [wordfreq](https://github.com/rspeer/wordfreq) by Robyn Speer, data licensed
  [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). These word lists are derived from it
  and are shared under the same license.
- Spell-checking (used only to filter words): Hunspell dictionaries from
  [wooorm/dictionaries](https://github.com/wooorm/dictionaries).
- Offensive words (used only to filter words):
  [LDNOOBW](https://github.com/LDNOOBW/List-of-Dirty-Naughty-Obscene-and-Otherwise-Bad-Words), CC BY 4.0.
