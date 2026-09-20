#!/usr/bin/env python3
"""
Hebrew Lyrics to Discord ANSI Formatter
Paste full Hebrew lyrics, get Discord-ready colored output.
Multiple output formats: Discord ANSI, Terminal, Markdown.
"""
import sys
import re
import os
from datetime import datetime

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

# ANSI escape sequences for Discord
ESC = "\x1b"
YELLOW = f"{ESC}[2;33m"
WHITE = f"{ESC}[2;37m"
CYAN = f"{ESC}[2;36m"
RESET = f"{ESC}[0m"

# Terminal colors (standard ANSI)
T_YELLOW = "\033[93m"
T_WHITE = "\033[97m"
T_CYAN = "\033[96m"
T_RESET = "\033[0m"
T_BOLD = "\033[1m"

HEBREW_PATTERN = re.compile(r'[֐-׿]')

def is_hebrew(text):
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

    combos = [('וו', 'v'), ('יי', 'ai'), ('וי', 'oi'), ('או', 'o'), ('אי', 'i'), ('יו', 'yo')]
    result = text
    for combo, replacement in combos:
        result = result.replace(combo, replacement)

    output = []
    for char in result:
        if char in mapping:
            output.append(mapping[char])
        elif char.isascii() or char.isspace():
            output.append(char)
        elif '֐' <= char <= '׏':
            pass

    text = ''.join(output)
    text = re.sub(r"'+", "'", text)
    text = re.sub(r"'\s", " ", text)
    text = re.sub(r"\s'", " ", text)
    text = text.strip("'").strip()

    return ' '.join(w.capitalize() for w in text.split())

def translate_line(text):
    if not HAS_TRANSLATE:
        return "[install googletrans]"
    try:
        result = translator.translate(text, src='he', dest='en')
        return result.text
    except:
        return "[translation error]"

# ============= OUTPUT FORMATTERS =============

def format_discord(lines_data):
    """Discord ANSI code block"""
    output = "```ansi\n"
    for item in lines_data:
        if item is None:
            output += "\n"
        else:
            translit, english, hebrew = item
            output += f"{YELLOW}{translit}{RESET}\n"
            output += f"{WHITE}{english}{RESET}\n\n"
    output = output.rstrip('\n') + "\n```"
    return output

def format_terminal(lines_data):
    """Terminal-friendly colored output"""
    output = ""
    for item in lines_data:
        if item is None:
            output += "\n"
        else:
            translit, english, hebrew = item
            output += f"{T_YELLOW}{T_BOLD}{translit}{T_RESET}\n"
            output += f"{T_WHITE}{english}{T_RESET}\n\n"
    return output.rstrip('\n')

def format_terminal_plain(lines_data):
    """Terminal without colors (plain text)"""
    output = ""
    for item in lines_data:
        if item is None:
            output += "\n"
        else:
            translit, english, hebrew = item
            output += f"{translit}\n"
            output += f"  {english}\n\n"
    return output.rstrip('\n')

def format_markdown(lines_data, include_hebrew=True):
    """Markdown format"""
    output = "# Hebrew Lyrics\n\n"
    for item in lines_data:
        if item is None:
            output += "---\n\n"
        else:
            translit, english, hebrew = item
            if include_hebrew:
                output += f"**{translit}** — {hebrew}\n"
            else:
                output += f"**{translit}**\n"
            output += f"> {english}\n\n"
    return output.rstrip('\n')

# ============= INPUT =============

def get_multiline_paste():
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
    """Process raw Hebrew text - returns (translit, english, hebrew) tuples"""
    lines = raw_text.split('\n')
    result = []
    prev_empty = False

    print("\nTranslating", end="", flush=True)

    for line in lines:
        line = line.strip()

        if not line:
            if not prev_empty and result:
                result.append(None)
            prev_empty = True
            continue

        prev_empty = False

        if is_hebrew(line):
            translit = transliterate_hebrew(line)
            english = translate_line(line)
            result.append((translit, english, line))  # Keep original Hebrew
            print(".", end="", flush=True)
        else:
            result.append((line, "", line))

    print(" done!")

    while result and result[-1] is None:
        result.pop()

    return result

# ============= MENU =============

def show_menu():
    print("\n" + "=" * 50)
    print("  OUTPUT OPTIONS")
    print("=" * 50)
    print("  1. Copy to clipboard (Discord ANSI)")
    print("  2. Display in terminal (colored)")
    print("  3. Display in terminal (plain)")
    print("  4. Save as Markdown (with Hebrew)")
    print("  5. Save as Markdown (without Hebrew)")
    print("  6. Copy all formats to clipboard")
    print("  0. Exit")
    print("-" * 50)
    return input("Choice [1]: ").strip() or "1"

def save_markdown(content, include_hebrew):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    suffix = "with_heb" if include_hebrew else "translit_only"
    filename = f"lyrics_{suffix}_{timestamp}.md"

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

    return filename

def main():
    print("=" * 50)
    print("  Hebrew Lyrics → Multi-Format Converter")
    print("  עברית → Discord / Terminal / Markdown")
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
            translit, english, hebrew = item
            print(f"  {T_YELLOW}{translit}{T_RESET}")
            print(f"  {T_WHITE}> {english}{T_RESET}")
            count += 1
            if count >= 5:
                remaining = len([x for x in lines_data if x]) - 5
                if remaining > 0:
                    print(f"  ... +{remaining} more lines")
                break
    print("-" * 50)

    # Menu loop
    while True:
        choice = show_menu()

        if choice == "0":
            print("להתראות (lehitraot - goodbye)!")
            break

        elif choice == "1":
            output = format_discord(lines_data)
            if HAS_CLIPBOARD:
                pyperclip.copy(output)
                print("✓ Discord ANSI copied to clipboard!")
            else:
                print(output)
                print("\n(Install pyperclip for clipboard support)")

        elif choice == "2":
            print("\n" + format_terminal(lines_data))

        elif choice == "3":
            print("\n" + format_terminal_plain(lines_data))

        elif choice == "4":
            content = format_markdown(lines_data, include_hebrew=True)
            filename = save_markdown(content, include_hebrew=True)
            print(f"✓ Saved to {filename}")

        elif choice == "5":
            content = format_markdown(lines_data, include_hebrew=False)
            filename = save_markdown(content, include_hebrew=False)
            print(f"✓ Saved to {filename}")

        elif choice == "6":
            if HAS_CLIPBOARD:
                all_output = "=== DISCORD ===\n"
                all_output += format_discord(lines_data)
                all_output += "\n\n=== MARKDOWN (with Hebrew) ===\n"
                all_output += format_markdown(lines_data, include_hebrew=True)
                all_output += "\n\n=== PLAIN ===\n"
                all_output += format_terminal_plain(lines_data)
                pyperclip.copy(all_output)
                print("✓ All formats copied to clipboard!")
            else:
                print("Need pyperclip for clipboard")

        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()
