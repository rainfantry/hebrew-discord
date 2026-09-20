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
    """Hebrew to Latin transliteration with vowel inference"""

    # Common Hebrew words with known transliterations
    known_words = {
        'שלום': 'shalom', 'ישראל': 'yisrael', 'עם': 'am', 'חי': 'chai',
        'אהבה': 'ahava', 'לב': 'lev', 'טוב': 'tov', 'הכל': 'hakol',
        'בקרוב': 'bekarov', 'תזרח': 'tizrach', 'השמש': 'hashemesh',
        'שמש': 'shemesh', 'ימים': 'yamim', 'יפים': 'yafim', 'נדע': 'neda',
        'הלב': 'halev', 'נלחם': 'nilcham', 'דאגות': 'de\'agot',
        'כולם': 'kulam', 'יחזרו': 'yachzeru', 'הביתה': 'habaita',
        'למטה': 'lemata', 'נחכה': 'nechake', 'להם': 'lahem',
        'הלוואי': 'halevai', 'בשורות': 'besorot', 'טובות': 'tovot',
        'לעולם': 'le\'olam', 'מפחד': 'mefached', 'הנצח': 'hanetzach',
        'אפילו': 'afilu', 'כשקשה': 'kshe\'kashe', 'לראות': 'lirot',
        'ביחד': 'beyachad', 'אחד': 'echad', 'פה': 'po', 'בודד': 'boded',
        'שישרפו': 'sheyisrefu', 'המלחמות': 'hamilchamot',
        'נשכח': 'nishkach', 'תמיד': 'tamid', 'להיות': 'lihiyot',
        'מאוחדים': 'me\'uchadim', 'בעליות': 'ba\'aliyot',
        'בירידות': 'biridot', 'גם': 'gam', 'בשעות': 'bisha\'ot',
        'הכי': 'hachi', 'קשות': 'kashot', 'הקדוש': 'hakadosh',
        'ברוך': 'baruch', 'הוא': 'hu', 'שומר': 'shomer', 'עלינו': 'aleinu',
        'יכול': 'yachol', 'מי': 'mi', 'אין': 'ein', 'לנו': 'lanu',
        'עוד': 'od', 'מדינה': 'medina', 'תעשה': 'ta\'ase',
        'בנינו': 'beneinu', 'שמור': 'shmor', 'על': 'al',
        'ילדינו': 'yaldeinu', 'אבדה': 'avda', 'האמונה': 'ha\'emuna',
        'כי': 'ki', 'אם': 'im', 'לא': 'lo', 'את': 'et', 'של': 'shel',
        'אני': 'ani', 'אתה': 'ata', 'היא': 'hi', 'הם': 'hem',
        'יודע': 'yode\'a', 'רוצה': 'rotze', 'אוהב': 'ohev',
        'חבר': 'chaver', 'חברה': 'chevra', 'בית': 'bayit',
        'משפחה': 'mishpacha', 'אלוהים': 'elohim', 'ארץ': 'eretz',
    }

    words = text.split()
    result_words = []

    for word in words:
        word_clean = word.strip()
        if word_clean in known_words:
            result_words.append(known_words[word_clean])
        else:
            # Fallback to letter-by-letter with vowel inference
            result_words.append(transliterate_word(word_clean))

    return ' '.join(w.capitalize() for w in result_words)

def transliterate_word(word):
    """Transliterate single word with vowel inference"""
    mapping = {
        'א': 'a', 'ב': 'v', 'ג': 'g', 'ד': 'd', 'ה': 'h', 'ו': 'o',
        'ז': 'z', 'ח': 'ch', 'ט': 't', 'י': 'i', 'כ': 'kh', 'ך': 'kh',
        'ל': 'l', 'מ': 'm', 'ם': 'm', 'נ': 'n', 'ן': 'n', 'ס': 's',
        'ע': 'a', 'פ': 'f', 'ף': 'f', 'צ': 'tz', 'ץ': 'tz', 'ק': 'k',
        'ר': 'r', 'ש': 'sh', 'ת': 't',
    }

    # Multi-char patterns (order matters)
    patterns = [
        ('וו', 'v'), ('יי', 'ai'), ('וי', 'oy'), ('או', 'o'),
        ('אי', 'i'), ('יו', 'yo'), ('אה', 'a'), ('הי', 'hi'),
        ('בר', 'bar'), ('שר', 'sar'),
    ]

    result = word
    for pattern, replacement in patterns:
        result = result.replace(pattern, f'_{replacement}_')

    output = []
    i = 0
    chars = list(result)

    while i < len(chars):
        char = chars[i]

        if char == '_':
            i += 1
            continue
        elif char in mapping:
            output.append(mapping[char])
            # Add schwa (e) between consecutive consonants
            if i + 1 < len(chars) and chars[i+1] in mapping and chars[i+1] not in 'אוי':
                next_char = mapping.get(chars[i+1], '')
                if next_char and next_char not in 'aeiou':
                    output.append('e')
        elif char.isascii():
            output.append(char)
        i += 1

    text = ''.join(output)
    # Clean up
    text = re.sub(r'([aeiou])\1+', r'\1', text)  # Remove double vowels
    text = re.sub(r'hh+', 'h', text)
    return text

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

def reverse_for_powershell(text):
    """Reverse Hebrew text so PowerShell's broken RTL displays it correctly"""
    return text[::-1]

def format_terminal_full(lines_data):
    """Terminal with all 3 lines - Hebrew pre-reversed for correct PowerShell display"""
    output = ""
    for item in lines_data:
        if item is None:
            output += f"{T_GRAY}---{T_RESET}\n\n"
        else:
            translit, english, hebrew = item
            hebrew_display = reverse_for_powershell(hebrew)
            output += f"{T_CYAN}{hebrew_display}{T_RESET}\n"
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
    print(f"  {T_YELLOW}8{T_RESET}. Save Discord format (.txt with ANSI)")
    print(f"  {T_YELLOW}9{T_RESET}. Save ALL formats")
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
            content = format_discord(lines_data)
            filename = save_file(content, "discord", "txt")
            print(f"{T_GREEN}✓ Saved: {filename}{T_RESET}")
            print(f"{T_GRAY}  (Copy contents and paste in Discord){T_RESET}")

        elif choice == "9":
            f1 = save_file(format_markdown(lines_data, True), "with_hebrew")
            f2 = save_file(format_markdown(lines_data, False), "translit_only")
            f3 = save_file(format_discord(lines_data), "discord", "txt")
            f4 = save_file(format_terminal_plain(lines_data), "plain", "txt")
            print(f"{T_GREEN}✓ Saved: {f1}, {f2}, {f3}, {f4}{T_RESET}")

        else:
            print(f"{T_GRAY}Invalid choice{T_RESET}")

if __name__ == "__main__":
    main()
