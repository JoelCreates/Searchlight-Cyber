"""
SICS (Searchlight Inefficient Compression Scheme)

Provides:
- CountFrequencies: tally characters in a text
- SortCharacters: order by descending frequency, tie‐break by Unicode
- GenerateCodes: yield '0'..'E', then 'F0'..'FE', 'FF0'..'FFE', etc.
- BuildMapping: assign each character its code
- CompressText: replace text → codes
- DecompressText: parse codes → text

Example usage in __main__.
"""

import sys

def CountFrequencies(text):
    """
    Build a dict mapping each character to its occurrence count.
    """
    freqs = {}
    for ch in text:
        if ch in freqs:
            freqs[ch] += 1
        else:
            freqs[ch] = 1
    return freqs

def SortCharacters(freqs):
    """
    Given freqs (char→count), return a list of characters
    sorted by descending count, then ascending character.
    """
    items = list(freqs.items())  # [(char, count), ...]
    # Define a sort key: negative count, then character
    def SortKey(pair):
        # pair[0] is char, pair[1] is count
        return (-pair[1], pair[0])
    items.sort(key=SortKey)
    sorted_chars = [pair[0] for pair in items]
    return sorted_chars

def GenerateCodes():
    """
    Generator that yields:
      '0','1',...,'E',
      'F0','F1',...,'FE',
      'FF0','FF1',...,'FFE', etc.
    """
    # Single-nibble: 0..14 → '0'..'E'
    for number in range(15):
        # format(n, 'X') gives '0'..'9','A'..'E'
        yield format(number, 'X')
    # Then multi-nibble with 'F' prefixes
    prefix = 'F'
    while True:
        for number in range(15):
            yield prefix + format(number, 'X')
        prefix = prefix + 'F'

def BuildMapping(sorted_chars):
    """
    Given sorted_chars (most→least frequent),
    assign each the next code from GenerateCodes().
    Returns dict: char→code.
    """
    mapping = {}
    code_gen = GenerateCodes()
    for ch in sorted_chars:
        mapping[ch] = next(code_gen)
    return mapping

def CompressText(text, mapping):
    """
    Replace each character in text with its code.
    """
    parts = []
    for ch in text:
        parts.append(mapping[ch])
    return ''.join(parts)

def DecompressText(compressed, mapping):
    """
    Restore original text from compressed string and mapping.
    """
    # Build inverse map: code→char
    inverse_map = {}
    for ch, code in mapping.items():
        inverse_map[code] = ch

    i = 0
    result = []
    length = len(compressed)
    while i < length:
        if compressed[i] != 'F':
            # single-nibble code
            key = compressed[i]
            i += 1
        else:
            # count how many 'F's
            start = i
            while i < length and compressed[i] == 'F':
                i += 1
            # include the next nibble
            if i < length:
                i += 1
            key = compressed[start:i]
        # append the decoded character
        result.append(inverse_map.get(key, '?'))
    return ''.join(result)

def main():
    # Read the test text (hardcoded or from file)
    sample = (
        "Marley was dead: to begin with. There is no doubt whatever about that. "
        "The register of his burial was signed by the clergyman, the clerk, the undertaker, "
        "and the chief mourner. Scrooge signed it: and Scrooge’s name was good upon ’Change, "
        "for anything he chose to put his hand to. Old Marley was as dead as a door-nail. "
        "Mind! I don’t mean to say that I know, of my own knowledge, what there is particularly "
        "dead about a door-nail. I might have been inclined, myself, to regard a coffin-nail as "
        "the deadest piece of ironmongery in the trade. But the wisdom of our ancestors is in the "
        "simile; and my unhallowed hands shall not disturb it, or the Country’s done for. You will "
        "therefore permit me to repeat, emphatically, that Marley was as dead as a door-nail."
    )

    # 1) Count frequencies
    freqs = CountFrequencies(sample)

    # 2) Sort characters
    sorted_chars = SortCharacters(freqs)

    # 3) Build mapping
    mapping = BuildMapping(sorted_chars)

    # 4) Compress
    compressed = CompressText(sample, mapping)
    print("Compressed length:", len(compressed))
    # (You can print compressed here if you wish)

    # 5) Decompress and verify
    restored = DecompressText(compressed, mapping)
    if restored == sample:
        print("Success: decompressed text matches original.")
    else:
        print("Error: mismatch after decompression.")

if __name__ == "__main__":
    main()
