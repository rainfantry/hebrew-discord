#!/usr/bin/env python3
"""
Hebrew Lyrics to Discord ANSI Formatter
Paste Hebrew lyrics, get Discord-ready colored output.
"""
import sys

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

# ANSI escape sequences (real escape char)
ESC = "\x1b"
YELLOW = f"{ESC}[2;33m"
WHITE = f"{ESC}[2;37m"
CYAN = f"{ESC}[2;36m"
RESET = f"{ESC}[0m"

def transliterate_hebrew(text):
    """Basic Hebrew to Latin transliteration"""
    mapping = {
        'א': '', 'ב': 'v', 'ג': 'g', 'ד': 'd', 'ה': 'h', 'ו': 'v',
        'ז': 'z', 'ח': 'ch', 'ט': 't', 'י': 'y', 'כ': 'ch', 'ך': 'ch',
        'ל': 'l', 'מ': 'm', 'ם': 'm', 'נ': 'n', 'ן': 'n', 'ס': 's',
        'ע': '', 'פ': 'f', 'ף': 'f', 'צ': 'tz', 'ץ': 'tz', 'ק': 'k',
        'ר': 'r', 'ש': 'sh', 'ת': 't',
        # Vowels (niqqud)
        'ְ': 'e', 'ֱ': 'e', 'ֲ': 'a', 'ֳ': 'o',
        'ִ': 'i', 'ֵ': 'e', 'ֶ': 'e', 'ַ': 'a',
        'ָ': 'a', 'ֹ': 'o', 'ֺ': 'o', 'ֻ': 'u',
        'ּ': '', 'ֽ': '', '־': '-', 'ֿ': '',
        'ׁ': '', 'ׂ': '',
    }
    result = []
    for char in text:
        if char in mapping:
            result.append(mapping[char])
        elif char.isascii():
            result.append(char)
        elif char.isspace():
            result.append(char)
    return ''.join(result)

def format_for_discord(hebrew_lines, english_lines):
    """Format as Discord ANSI code block"""
    output = "```ansi\n"
    for heb, eng in zip(hebrew_lines, english_lines):
        transliteration = transliterate_hebrew(heb).strip()
        # Capitalize first letter of each word
        transliteration = ' '.join(w.capitalize() for w in transliteration.split())
        output += f"{YELLOW}{transliteration}{RESET}\n"
        output += f"{WHITE}{eng.strip()}{RESET}\n\n"
    output += "```"
    return output

def get_multiline_input(prompt):
    """Get multiline input until empty line"""
    print(prompt)
    print("(Enter empty line when done)")
    lines = []
    while True:
        try:
            line = input()
            if line == "":
                break
            lines.append(line)
        except EOFError:
            break
    return lines

def main():
    print("=" * 50)
    print("  Hebrew Lyrics → Discord ANSI Formatter")
    print("=" * 50)
    print()
    
    # Get Hebrew input
    hebrew_lines = get_multiline_input("Paste Hebrew lyrics (one line per verse):")
    
    if not hebrew_lines:
        print("No input. Exiting.")
        return
    
    print()
    
    # Try auto-translate or ask for English
    if HAS_TRANSLATE:
        print("Auto-translating...")
        english_lines = []
        for line in hebrew_lines:
            try:
                result = translator.translate(line, src='he', dest='en')
                english_lines.append(result.text)
                print(f"  {line[:30]}... → {result.text[:40]}...")
            except:
                english_lines.append("[translation failed]")
        print()
        print("Edit translations? (y/n): ", end="")
        if input().lower() == 'y':
            print("Enter English translations (one per line):")
            english_lines = get_multiline_input("")
    else:
        english_lines = get_multiline_input("Enter English translations (one per line):")
    
    # Pad if needed
    while len(english_lines) < len(hebrew_lines):
        english_lines.append("")
    
    # Generate output
    output = format_for_discord(hebrew_lines, english_lines)
    
    print()
    print("=" * 50)
    print("OUTPUT (paste into Discord):")
    print("=" * 50)
    print(output)
    
    if HAS_CLIPBOARD:
        pyperclip.copy(output)
        print()
        print("✓ Copied to clipboard!")
    else:
        print()
        print("(Install pyperclip for auto-copy: pip install pyperclip)")

if __name__ == "__main__":
    main()
