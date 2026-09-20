#!/usr/bin/env python3
"""
Hebrew Lyrics to Discord ANSI Formatter
Paste full Hebrew lyrics, get Discord-ready colored output.
Multiple output formats: Discord ANSI, Terminal, Markdown.

Note: PowerShell cannot render RTL (Hebrew displays backwards).
      Hebrew is preserved for Discord/Markdown export only.
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
    from deep_translator import MyMemoryTranslator
    HAS_TRANSLATE = True
except ImportError:
    HAS_TRANSLATE = False

# ANSI escape sequences for Discord
ESC = "\x1b"
D_YELLOW = f"{ESC}[2;33m"
D_WHITE = f"{ESC}[2;37m"
D_CYAN = f"{ESC}[2;36m"
D_RESET = f"{ESC}[0m"

# Terminal colors (standard ANSI)
T_YELLOW = "\033[93m"
T_WHITE = "\033[97m"
T_CYAN = "\033[96m"
T_GREEN = "\033[92m"
T_GRAY = "\033[90m"
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

_translator = None
def translate_line(text):
    global _translator
    if not HAS_TRANSLATE:
        return "[pip install deep-translator]"
    try:
        if _translator is None:
            _translator = MyMemoryTranslator(source='he-IL', target='en-GB')
        return _translator.translate(text)
    except Exception as e:
        return "[translation error]"

# ============= OUTPUT FORMATTERS =============

def format_discord(lines_data):
    """Discord ANSI code block - transliteration + english"""
    output = "```ansi\n"
    for item in lines_data:
        if item is None:
            output += "\n"
        else:
            translit, english, hebrew = item
            output += f"{D_YELLOW}{translit}{D_RESET}\n"
            output += f"{D_WHITE}{english}{D_RESET}\n\n"
    output = output.rstrip('\n') + "\n```"
    return output

def format_terminal(lines_data):
    """Terminal colored - transliteration + english (no Hebrew - displays broken)"""
    output = ""
    for item in lines_data:
        if item is None:
            output += f"{T_GRAY}---{T_RESET}\n\n"
        else:
            translit, english, hebrew = item
            output += f"{T_YELLOW}{T_BOLD}{translit}{T_RESET}\n"
            output += f"{T_WHITE}{english}{T_RESET}\n\n"
    return output.rstrip('\n')

def format_terminal_full(lines_data):
    """Terminal with all 3 lines (Hebrew will display backwards but included)"""
    output = ""
    for item in lines_data:
        if item is None:
            output += f"{T_GRAY}---{T_RESET}\n\n"
        else:
            translit, english, hebrew = item
            output += f"{T_CYAN}{hebrew}{T_RESET}  {T_GRAY}(displays backwards in terminal){T_RESET}\n"
            output += f"{T_YELLOW}{T_BOLD}{translit}{T_RESET}\n"
            output += f"{T_WHITE}{english}{T_RESET}\n\n"
    return output.rstrip('\n')

def format_terminal_plain(lines_data):
    """Plain text no colors"""
    output = ""
    for item in lines_data:
        if item is None:
            output += "---\n\n"
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
            result.append((translit, english, line))
            print(".", end="", flush=True)
        else:
            result.append((line, "", line))

    print(" done!")

    while result and result[-1] is None:
        result.pop()

    return result

# ============= MENU =============

def show_menu():
    print()
    print(f"{T_GREEN}{'=' * 50}{T_RESET}")
    print(f"{T_GREEN}  DISPLAY OPTIONS{T_RESET}")
    print(f"{T_GREEN}{'=' * 50}{T_RESET}")
    print(f"  {T_YELLOW}1{T_RESET}. Show in terminal (transliteration + english)")
    print(f"  {T_YELLOW}2{T_RESET}. Show in terminal (all 3: hebrew + translit + english)")
    print(f"  {T_YELLOW}3{T_RESET}. Show plain text (no colors)")
    print()
    print(f"{T_CYAN}  COPY OPTIONS{T_RESET}")
    print(f"{T_CYAN}{'=' * 50}{T_RESET}")
    print(f"  {T_YELLOW}4{T_RESET}. Copy for Discord (ANSI colors)")
    print(f"  {T_YELLOW}5{T_RESET}. Copy plain text")
    print()
    print(f"{T_WHITE}  EXPORT OPTIONS{T_RESET}")
    print(f"{T_WHITE}{'=' * 50}{T_RESET}")
    print(f"  {T_YELLOW}6{T_RESET}. Save Markdown (with Hebrew)")
    print(f"  {T_YELLOW}7{T_RESET}. Save Markdown (transliteration only)")
    print(f"  {T_YELLOW}8{T_RESET}. Save all formats")
    print()
    print(f"  {T_GRAY}0{T_RESET}. Exit")
    print("-" * 50)
    return input("Choice: ").strip()

def save_file(content, suffix, ext="md"):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"lyrics_{suffix}_{timestamp}.{ext}"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    return filename

def main():
    print(f"{T_GREEN}{'=' * 50}{T_RESET}")
    print(f"{T_GREEN}  Hebrew Lyrics Converter{T_RESET}")
    print(f"{T_GRAY}  Terminal / Discord / Markdown{T_RESET}")
    print(f"{T_GREEN}{'=' * 50}{T_RESET}")
    print()

    raw_text = get_multiline_paste()

    if not raw_text.strip():
        print("No input.")
        return

    lines_data = process_lyrics(raw_text)

    if not lines_data:
        print("No valid lines found.")
        return

    # Quick preview (transliteration + english only - no broken Hebrew)
    print(f"\n{T_GREEN}Preview:{T_RESET}")
    print("-" * 50)
    count = 0
    for item in lines_data:
        if item is None:
            print(f"  {T_GRAY}---{T_RESET}")
        else:
            translit, english, hebrew = item
            print(f"  {T_YELLOW}{translit}{T_RESET}")
            print(f"  {T_WHITE}> {english}{T_RESET}")
            count += 1
            if count >= 3:
                remaining = len([x for x in lines_data if x]) - 3
                if remaining > 0:
                    print(f"  {T_GRAY}... +{remaining} more lines{T_RESET}")
                break
    print("-" * 50)
    print(f"{T_GRAY}(Hebrew preserved for Discord/Markdown export){T_RESET}")

    # Menu loop
    while True:
        choice = show_menu()

        if choice == "0" or choice == "":
            print(f"{T_GREEN}lehitraot! (goodbye){T_RESET}")
            break

        elif choice == "1":
            print("\n" + format_terminal(lines_data))

        elif choice == "2":
            print("\n" + format_terminal_full(lines_data))

        elif choice == "3":
            print("\n" + format_terminal_plain(lines_data))

        elif choice == "4":
            output = format_discord(lines_data)
            if HAS_CLIPBOARD:
                pyperclip.copy(output)
                print(f"{T_GREEN}✓ Discord ANSI copied!{T_RESET}")
            else:
                print(output)
                print(f"\n{T_GRAY}(pip install pyperclip for clipboard){T_RESET}")

        elif choice == "5":
            output = format_terminal_plain(lines_data)
            if HAS_CLIPBOARD:
                pyperclip.copy(output)
                print(f"{T_GREEN}✓ Plain text copied!{T_RESET}")
            else:
                print(f"{T_GRAY}(pip install pyperclip for clipboard){T_RESET}")

        elif choice == "6":
            content = format_markdown(lines_data, include_hebrew=True)
            filename = save_file(content, "with_hebrew")
            print(f"{T_GREEN}✓ Saved: {filename}{T_RESET}")

        elif choice == "7":
            content = format_markdown(lines_data, include_hebrew=False)
            filename = save_file(content, "translit_only")
            print(f"{T_GREEN}✓ Saved: {filename}{T_RESET}")

        elif choice == "8":
            f1 = save_file(format_markdown(lines_data, True), "with_hebrew")
            f2 = save_file(format_markdown(lines_data, False), "translit_only")
            f3 = save_file(format_terminal_plain(lines_data), "plain", "txt")
            print(f"{T_GREEN}✓ Saved: {f1}, {f2}, {f3}{T_RESET}")

        else:
            print(f"{T_GRAY}Invalid choice{T_RESET}")

if __name__ == "__main__":
    main()
