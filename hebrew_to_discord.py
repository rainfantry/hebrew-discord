#!/usr/bin/env python3
"""
Hebrew Lyrics to Discord ANSI Formatter
Paste full Hebrew lyrics, get Discord-ready colored output.
Handles multiline paste, paragraphs, auto-translation.
"""
import sys
import re

try:
    import pyperclip
    HAS_CLIPBOARD = True
except ImportError:
    HAS_CLIPBOARD = False

try:
    from googletrans import Translator
    HAS_TRANSLATE = True
    translator = Translator()
except ImportError:
    HAS_TRANSLATE = False

# ANSI escape sequences (real escape char for Discord)
ESC = "\x1b"
YELLOW = f"{ESC}[2;33m"
WHITE = f"{ESC}[2;37m"
CYAN = f"{ESC}[2;36m"
RESET = f"{ESC}[0m"

# Hebrew Unicode range
HEBREW_PATTERN = re.compile(r'[֐-׿]')

def is_hebrew(text):
    """Check if text contains Hebrew characters"""
    return bool(HEBREW_PATTERN.search(text))

def transliterate_hebrew(text):
    """Hebrew to Latin transliteration"""
    mapping = {
        'א': "'", 'ב': 'v', 'ג': 'g', 'ד': 'd', 'ה': 'h', 'ו': 'o',
        'ז': 'z', 'ח': 'ch', 'ט': 't', 'י': 'i', 'כ': 'ch', 'ך': 'ch',
        'ל': 'l', 'מ': 'm', 'ם': 'm', 'נ': 'n', 'ן': 'n', 'ס': 's',
        'ע': "'", 'פ': 'f', 'ף': 'f', 'צ': 'tz', 'ץ': 'tz', 'ק': 'k',
        'ר': 'r', 'ש': 'sh', 'ת': 't',
    }

    # Handle common letter combinations
    combos = [('וו', 'v'), ('יי', 'ai'), ('וי', 'oi'), ('או', 'o'), ('אי', 'i'), ('יו', 'yo')]
    result = text
    for combo, replacement in combos:
        result = result.replace(combo, replacement)

    # Single character mapping
    output = []
    for char in result:
        if char in mapping:
            output.append(mapping[char])
        elif char.isascii() or char.isspace():
            output.append(char)
        elif '֐' <= char <= '׏':
            pass  # Skip Hebrew punctuation

    # Clean up
    text = ''.join(output)
    text = re.sub(r"'+", "'", text)
    text = re.sub(r"'\s", " ", text)
    text = re.sub(r"\s'", " ", text)
    text = text.strip("'").strip()

    # Capitalize each word
    return ' '.join(w.capitalize() for w in text.split())

def translate_line(text):
    """Translate Hebrew to English"""
    if not HAS_TRANSLATE:
        return "[install googletrans]"
    try:
        result = translator.translate(text, src='he', dest='en')
        return result.text
    except:
        return "[translation error]"

def format_for_discord(lines_data):
    """Format as Discord ANSI code block"""
    output = "```ansi\n"
    for item in lines_data:
        if item is None:
            output += "\n"
        else:
            translit, english = item
            output += f"{YELLOW}{translit}{RESET}\n"
            output += f"{WHITE}{english}{RESET}\n\n"
    output = output.rstrip('\n') + "\n```"
    return output

def get_multiline_paste():
    """Get multiline paste - type END when done"""
    print("Paste Hebrew lyrics below (type END on new line when done):")
    print("-" * 50)

    lines = []
    while True:
        try:
            line = input()
            if line.strip().upper() == 'END':
                break
            lines.append(line)
        except EOFError:
            break

    return '\n'.join(lines)

def process_lyrics(raw_text):
    """Process raw Hebrew text into formatted lines"""
    lines = raw_text.split('\n')
    result = []
    prev_empty = False

    print("\nTranslating", end="", flush=True)

    for line in lines:
        line = line.strip()

        if not line:
            if not prev_empty and result:
                result.append(None)  # Paragraph break
            prev_empty = True
            continue

        prev_empty = False

        if is_hebrew(line):
            translit = transliterate_hebrew(line)
            english = translate_line(line)
            result.append((translit, english))
            print(".", end="", flush=True)
        else:
            result.append((line, ""))

    print(" done!")

    while result and result[-1] is None:
        result.pop()

    return result

def main():
    print("=" * 50)
    print("  Hebrew Lyrics → Discord ANSI Formatter")
    print("  עברית → Discord")
    print("=" * 50)
    print()

    raw_text = get_multiline_paste()

    if not raw_text.strip():
        print("No input.")
        return

    lines_data = process_lyrics(raw_text)

    if not lines_data:
        print("No valid lines found.")
        return

    # Preview
    print("\nPreview (first 5 lines):")
    print("-" * 50)
    count = 0
    for item in lines_data:
        if item is None:
            print("  ---")
        else:
            print(f"  {item[0]}")
            print(f"  > {item[1]}")
            count += 1
            if count >= 5:
                remaining = len([x for x in lines_data if x]) - 5
                if remaining > 0:
                    print(f"  ... +{remaining} more lines")
                break
    print("-" * 50)

    # Generate output
    output = format_for_discord(lines_data)

    print("\n" + "=" * 50)
    print("DISCORD OUTPUT (paste this):")
    print("=" * 50)
    print(output)

    if HAS_CLIPBOARD:
        pyperclip.copy(output)
        print("\n✓ Copied to clipboard!")
    else:
        print("\nInstall pyperclip for auto-copy: pip install pyperclip")

if __name__ == "__main__":
    main()
