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

import subprocess
import tempfile

def speak_hebrew(text, voice="he-IL-HilaNeural"):
    """Speak Hebrew text using edge-tts"""
    try:
        with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as f:
            temp_path = f.name

        result = subprocess.run(
            [sys.executable, "-m", "edge_tts", "--voice", voice, "--text", text, "--write-media", temp_path],
            capture_output=True, text=True
        )

        if result.returncode == 0:
            subprocess.Popen(["cmd", "/c", "start", "", temp_path], shell=True)
            return True
    except:
        pass
    return False

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
T_MAGENTA = "\033[95m"
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

def typing_hebrew(text):
    """Convert Hebrew to Windows Standard Hebrew keyboard keys.
    Shows exactly what QWERTY keys to press."""

    # Windows Standard Hebrew keyboard mapping (Israeli layout)
    # Hebrew letter → QWERTY key to press
    win_hebrew_map = {
        'א': 't', 'ב': 'c', 'ג': 'd', 'ד': 's', 'ה': 'v', 'ו': 'u',
        'ז': 'z', 'ח': 'j', 'ט': 'y', 'י': 'h', 'כ': 'f', 'ך': 'l',
        'ל': 'k', 'מ': 'n', 'ם': 'o', 'נ': 'b', 'ן': 'i', 'ס': 'x',
        'ע': 'g', 'פ': 'p', 'ף': ';', 'צ': 'm', 'ץ': '.', 'ק': 'e',
        'ר': 'r', 'ש': 'a', 'ת': ',',
    }

    words = text.split()
    result = []

    for word in words:
        typed = []
        for char in word:
            if char in win_hebrew_map:
                typed.append(win_hebrew_map[char])
            elif char.isascii():
                typed.append(char)
        result.append(''.join(typed).upper())

    return ' '.join(result)

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
            translit, english, hebrew, typing = item
            output += f"{D_YELLOW}{translit}{D_RESET}\n"
            output += f"{D_WHITE}{english}{D_RESET}\n\n"
    output = output.rstrip('\n') + "\n```"
    return output

def format_discord_chunked(lines_data, max_chars=1900, include_hebrew=False):
    """Discord ANSI split into chunks for non-Nitro (2000 char limit)"""
    chunks = []
    current_chunk = "```ansi\n"

    for item in lines_data:
        if item is None:
            line_content = "\n"
        else:
            translit, english, hebrew, typing = item
            if include_hebrew:
                line_content = f"{D_CYAN}{hebrew}{D_RESET}\n{D_YELLOW}{translit}{D_RESET}\n{D_WHITE}{english}{D_RESET}\n\n"
            else:
                line_content = f"{D_YELLOW}{translit}{D_RESET}\n{D_WHITE}{english}{D_RESET}\n\n"

        # Check if adding this would exceed limit
        if len(current_chunk) + len(line_content) + 4 > max_chars:  # +4 for closing ```
            current_chunk = current_chunk.rstrip('\n') + "\n```"
            chunks.append(current_chunk)
            current_chunk = "```ansi\n"

        current_chunk += line_content

    # Add final chunk
    if current_chunk != "```ansi\n":
        current_chunk = current_chunk.rstrip('\n') + "\n```"
        chunks.append(current_chunk)

    return chunks

def format_terminal(lines_data):
    """Terminal colored - transliteration + english (no Hebrew - displays broken)"""
    output = ""
    for item in lines_data:
        if item is None:
            output += f"{T_GRAY}---{T_RESET}\n\n"
        else:
            translit, english, hebrew, typing = item
            output += f"{T_YELLOW}{T_BOLD}{translit}{T_RESET}\n"
            output += f"{T_WHITE}{english}{T_RESET}\n\n"
    return output.rstrip('\n')

def reverse_for_powershell(text):
    """Reverse Hebrew portions only, keep English intact.
    PowerShell breaks RTL, so we pre-reverse Hebrew parts."""
    if not is_hebrew(text):
        return text

    result = []
    current_chunk = []
    current_is_hebrew = False

    for char in text:
        char_is_heb = '֐' <= char <= '׿'

        if char_is_heb != current_is_hebrew and current_chunk:
            # Flush current chunk
            chunk_text = ''.join(current_chunk)
            if current_is_hebrew:
                chunk_text = chunk_text[::-1]  # Reverse Hebrew
            result.append(chunk_text)
            current_chunk = []

        current_chunk.append(char)
        current_is_hebrew = char_is_heb

    # Flush last chunk
    if current_chunk:
        chunk_text = ''.join(current_chunk)
        if current_is_hebrew:
            chunk_text = chunk_text[::-1]
        result.append(chunk_text)

    return ''.join(result)

def format_terminal_full(lines_data):
    """Terminal with all 3 lines - Hebrew pre-reversed for correct PowerShell display"""
    output = ""
    for item in lines_data:
        if item is None:
            output += f"{T_GRAY}---{T_RESET}\n\n"
        else:
            translit, english, hebrew, typing = item
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
            translit, english, hebrew, typing = item
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
            translit, english, hebrew, typing = item
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
            typing = typing_hebrew(line)
            result.append((translit, english, line, typing))
            print(".", end="", flush=True)
        else:
            result.append((line, "", line, ""))

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
    print(f"  {T_YELLOW}8{T_RESET}. Save Discord (transliteration + english)")
    print(f"  {T_YELLOW}9{T_RESET}. Save Discord (hebrew + translit + english)")
    print(f"  {T_YELLOW}10{T_RESET}. Save ALL formats")
    print()
    print(f"{T_MAGENTA}  TYPING MODE (keyboard keys){T_RESET}")
    print(f"{T_MAGENTA}{'=' * 50}{T_RESET}")
    print(f"  {T_YELLOW}11{T_RESET}. Show typing (consonants only)")
    print(f"  {T_YELLOW}12{T_RESET}. Copy typing for Discord")
    print()
    print(f"  {T_GRAY}M{T_RESET}. Back to main menu (letter reference)")
    print(f"  {T_GRAY}0{T_RESET}. Exit")
    print("-" * 50)
    return input("Choice: ").strip()

def save_file(content, suffix, ext="md"):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"lyrics_{suffix}_{timestamp}.{ext}"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    return filename

def show_letter_reference():
    """Show Windows Standard Hebrew keyboard mapping"""
    print()
    print(f"{T_MAGENTA}{'=' * 60}{T_RESET}")
    print(f"{T_MAGENTA}  Windows Hebrew Keyboard Reference{T_RESET}")
    print(f"{T_GRAY}  Press these QWERTY keys to get Hebrew letters{T_RESET}")
    print(f"{T_MAGENTA}{'=' * 60}{T_RESET}")
    print()

    # Visual QWERTY keyboard with Hebrew mappings
    print(f"{T_CYAN}  QWERTY Keyboard Layout:{T_RESET}")
    print()
    print(f"  {T_YELLOW}┌───┬───┬───┬───┬───┬───┬───┬───┬───┬───┐{T_RESET}")
    print(f"  {T_YELLOW}│{T_RESET} Q {T_YELLOW}│{T_RESET} W {T_YELLOW}│{T_RESET} E {T_YELLOW}│{T_RESET} R {T_YELLOW}│{T_RESET} T {T_YELLOW}│{T_RESET} Y {T_YELLOW}│{T_RESET} U {T_YELLOW}│{T_RESET} I {T_YELLOW}│{T_RESET} O {T_YELLOW}│{T_RESET} P {T_YELLOW}│{T_RESET}")
    print(f"  {T_YELLOW}│{T_RESET} {T_CYAN}/{T_RESET} {T_YELLOW}│{T_RESET} {T_CYAN}'{T_RESET} {T_YELLOW}│{T_RESET} {T_CYAN}ק{T_RESET} {T_YELLOW}│{T_RESET} {T_CYAN}ר{T_RESET} {T_YELLOW}│{T_RESET} {T_CYAN}א{T_RESET} {T_YELLOW}│{T_RESET} {T_CYAN}ט{T_RESET} {T_YELLOW}│{T_RESET} {T_CYAN}ו{T_RESET} {T_YELLOW}│{T_RESET} {T_CYAN}ן{T_RESET} {T_YELLOW}│{T_RESET} {T_CYAN}ם{T_RESET} {T_YELLOW}│{T_RESET} {T_CYAN}פ{T_RESET} {T_YELLOW}│{T_RESET}")
    print(f"  {T_YELLOW}├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤{T_RESET}")
    print(f"  {T_YELLOW}│{T_RESET} A {T_YELLOW}│{T_RESET} S {T_YELLOW}│{T_RESET} D {T_YELLOW}│{T_RESET} F {T_YELLOW}│{T_RESET} G {T_YELLOW}│{T_RESET} H {T_YELLOW}│{T_RESET} J {T_YELLOW}│{T_RESET} K {T_YELLOW}│{T_RESET} L {T_YELLOW}│{T_RESET} ; {T_YELLOW}│{T_RESET}")
    print(f"  {T_YELLOW}│{T_RESET} {T_CYAN}ש{T_RESET} {T_YELLOW}│{T_RESET} {T_CYAN}ד{T_RESET} {T_YELLOW}│{T_RESET} {T_CYAN}ג{T_RESET} {T_YELLOW}│{T_RESET} {T_CYAN}כ{T_RESET} {T_YELLOW}│{T_RESET} {T_CYAN}ע{T_RESET} {T_YELLOW}│{T_RESET} {T_CYAN}י{T_RESET} {T_YELLOW}│{T_RESET} {T_CYAN}ח{T_RESET} {T_YELLOW}│{T_RESET} {T_CYAN}ל{T_RESET} {T_YELLOW}│{T_RESET} {T_CYAN}ך{T_RESET} {T_YELLOW}│{T_RESET} {T_CYAN}ף{T_RESET} {T_YELLOW}│{T_RESET}")
    print(f"  {T_YELLOW}├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤{T_RESET}")
    print(f"  {T_YELLOW}│{T_RESET} Z {T_YELLOW}│{T_RESET} X {T_YELLOW}│{T_RESET} C {T_YELLOW}│{T_RESET} V {T_YELLOW}│{T_RESET} B {T_YELLOW}│{T_RESET} N {T_YELLOW}│{T_RESET} M {T_YELLOW}│{T_RESET} , {T_YELLOW}│{T_RESET} . {T_YELLOW}│{T_RESET}")
    print(f"  {T_YELLOW}│{T_RESET} {T_CYAN}ז{T_RESET} {T_YELLOW}│{T_RESET} {T_CYAN}ס{T_RESET} {T_YELLOW}│{T_RESET} {T_CYAN}ב{T_RESET} {T_YELLOW}│{T_RESET} {T_CYAN}ה{T_RESET} {T_YELLOW}│{T_RESET} {T_CYAN}נ{T_RESET} {T_YELLOW}│{T_RESET} {T_CYAN}מ{T_RESET} {T_YELLOW}│{T_RESET} {T_CYAN}צ{T_RESET} {T_YELLOW}│{T_RESET} {T_CYAN}ת{T_RESET} {T_YELLOW}│{T_RESET} {T_CYAN}ץ{T_RESET} {T_YELLOW}│{T_RESET}")
    print(f"  {T_YELLOW}└───┴───┴───┴───┴───┴───┴───┴───┴───┴───┘{T_RESET}")
    print()

    # Windows Standard Hebrew keyboard - sorted by QWERTY key
    mappings = [
        ("A", "ש", "shin (sh)"),
        ("B", "נ", "nun (n)"),
        ("C", "ב", "bet (b/v)"),
        ("D", "ג", "gimel (g)"),
        ("E", "ק", "qof (k)"),
        ("F", "כ", "kaf (k/kh)"),
        ("G", "ע", "ayin (silent)"),
        ("H", "י", "yod (y/i)"),
        ("I", "ן", "nun sofit"),
        ("J", "ח", "chet (ch)"),
        ("K", "ל", "lamed (l)"),
        ("L", "ך", "kaf sofit"),
        ("M", "צ", "tsadi (tz)"),
        ("N", "מ", "mem (m)"),
        ("O", "ם", "mem sofit"),
        ("P", "פ", "pe (p/f)"),
        ("R", "ר", "resh (r)"),
        ("S", "ד", "dalet (d)"),
        ("T", "א", "alef (silent)"),
        ("U", "ו", "vav (v/o/u)"),
        ("V", "ה", "he (h)"),
        ("X", "ס", "samekh (s)"),
        ("Y", "ט", "tet (t)"),
        ("Z", "ז", "zayin (z)"),
        (",", "ת", "tav (t)"),
        (".", "ץ", "tsadi sofit"),
        (";", "ף", "pe sofit"),
    ]

    print(f"  {T_YELLOW}{'Key':<6}{T_RESET} {T_CYAN}{'Hebrew':<6}{T_RESET} {T_WHITE}Name{T_RESET}")
    print(f"  {'-' * 40}")
    for eng, heb, name in mappings:
        print(f"  {T_YELLOW}{eng:<6}{T_RESET} {T_CYAN}{heb:<6}{T_RESET} {T_GRAY}{name}{T_RESET}")

    print()
    print(f"{T_GREEN}Type English words to get Hebrew + keyboard keys{T_RESET}")
    print(f"{T_GRAY}(type 'q' to quit){T_RESET}")
    print()

    while True:
        word = input(f"{T_YELLOW}English word: {T_RESET}").strip()
        if not word or word.lower() == 'q':
            break

        # Translate English to Hebrew
        try:
            if HAS_TRANSLATE:
                from deep_translator import MyMemoryTranslator
                translator = MyMemoryTranslator(source='en-GB', target='he-IL')
                hebrew = translator.translate(word)
            else:
                hebrew = "[install deep-translator]"
        except:
            hebrew = "[translation error]"

        if hebrew and hebrew not in ["[translation error]", "[install deep-translator]"]:
            pronunciation = transliterate_hebrew(hebrew)
            keys = typing_hebrew(hebrew)

            print()
            print(f"  {T_WHITE}English:{T_RESET}       {word}")
            print(f"  {T_CYAN}Hebrew (PS):{T_RESET}   {reverse_for_powershell(hebrew)}")
            print(f"  {T_CYAN}Hebrew (copy):{T_RESET} {hebrew}")
            print(f"  {T_YELLOW}Say:{T_RESET}          {pronunciation}")
            print(f"  {T_MAGENTA}Type:{T_RESET}         {keys}")

            # TTS
            if speak_hebrew(hebrew):
                print(f"  {T_GREEN}[playing audio]{T_RESET}")
            print()
        else:
            print(f"  {T_GRAY}{hebrew}{T_RESET}")
            print()

def hebrew_practice_mode():
    """Offline Hebrew practice - paste Hebrew, get pronunciation + typing keys"""
    print()
    print(f"{T_MAGENTA}{'=' * 60}{T_RESET}")
    print(f"{T_MAGENTA}  Hebrew Practice Mode (OFFLINE){T_RESET}")
    print(f"{T_GRAY}  Paste Hebrew text, get pronunciation + keyboard keys{T_RESET}")
    print(f"{T_MAGENTA}{'=' * 60}{T_RESET}")
    print()
    print(f"{T_GREEN}Type Hebrew words/phrases (or 'q' to quit):{T_RESET}")
    print()

    while True:
        hebrew = input(f"{T_CYAN}Hebrew: {T_RESET}").strip()
        if not hebrew or hebrew.lower() == 'q':
            break

        # Check if actually Hebrew
        if not any('֐' <= c <= '׿' for c in hebrew):
            print(f"  {T_GRAY}(not Hebrew text){T_RESET}")
            print()
            continue

        pronunciation = transliterate_hebrew(hebrew)
        keys = typing_hebrew(hebrew)

        print()
        print(f"  {T_CYAN}Hebrew (PS):{T_RESET}   {reverse_for_powershell(hebrew)}")
        print(f"  {T_CYAN}Hebrew (copy):{T_RESET} {hebrew}")
        print(f"  {T_YELLOW}Say:{T_RESET}          {pronunciation}")
        print(f"  {T_MAGENTA}Type:{T_RESET}         {keys}")

        # TTS
        if speak_hebrew(hebrew):
            print(f"  {T_GREEN}[playing audio]{T_RESET}")
        print()

def show_main_menu():
    print()
    print(f"{T_GREEN}{'=' * 50}{T_RESET}")
    print(f"{T_GREEN}  Hebrew Lyrics Tool{T_RESET}")
    print(f"{T_GRAY}  Learn Hebrew through songs{T_RESET}")
    print(f"{T_GREEN}{'=' * 50}{T_RESET}")
    print()
    print(f"  {T_YELLOW}1{T_RESET}. Paste & process lyrics")
    print(f"  {T_YELLOW}2{T_RESET}. English → Hebrew (online translation)")
    print(f"  {T_YELLOW}3{T_RESET}. Hebrew practice (offline - paste Hebrew)")
    print(f"  {T_GRAY}0{T_RESET}. Exit")
    print("-" * 50)
    return input("Choice: ").strip()

def main():
    while True:
        choice = show_main_menu()

        if choice == "0" or choice == "":
            print(f"{T_GREEN}lehitraot! (להתראות){T_RESET}")
            break

        elif choice == "2":
            show_letter_reference()
            continue

        elif choice == "3":
            hebrew_practice_mode()
            continue

        elif choice == "1":
            process_lyrics_workflow()

        else:
            print(f"{T_GRAY}Invalid choice{T_RESET}")

def process_lyrics_workflow():
    print()
    print(f"{T_CYAN}Paste Hebrew lyrics, then type END on a new line:{T_RESET}")
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
            translit, english, hebrew, typing = item
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

        if choice.lower() == "m":
            print(f"{T_GRAY}Returning to main menu...{T_RESET}")
            return

        if choice == "0" or choice == "":
            print(f"{T_GREEN}lehitraot! (להתראות){T_RESET}")
            import sys
            sys.exit(0)

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
            chunks = format_discord_chunked(lines_data, include_hebrew=False)
            if len(chunks) == 1:
                filename = save_file(chunks[0], "discord", "txt")
                print(f"{T_GREEN}✓ Saved: {filename}{T_RESET}")
            else:
                print(f"{T_GREEN}✓ Split into {len(chunks)} messages:{T_RESET}")
                for i, chunk in enumerate(chunks, 1):
                    filename = save_file(chunk, f"discord_part{i}", "txt")
                    print(f"   {filename} ({len(chunk)} chars)")

        elif choice == "9":
            chunks = format_discord_chunked(lines_data, include_hebrew=True)
            if len(chunks) == 1:
                filename = save_file(chunks[0], "discord_heb", "txt")
                print(f"{T_GREEN}✓ Saved: {filename}{T_RESET}")
            else:
                print(f"{T_GREEN}✓ Split into {len(chunks)} messages (with Hebrew):{T_RESET}")
                for i, chunk in enumerate(chunks, 1):
                    filename = save_file(chunk, f"discord_heb_part{i}", "txt")
                    print(f"   {filename} ({len(chunk)} chars)")

        elif choice == "10":
            f1 = save_file(format_markdown(lines_data, True), "with_hebrew")
            f2 = save_file(format_markdown(lines_data, False), "translit_only")
            f3 = save_file(format_discord(lines_data), "discord", "txt")
            f4 = save_file(format_terminal_plain(lines_data), "plain", "txt")
            print(f"{T_GREEN}✓ Saved: {f1}, {f2}, {f3}, {f4}{T_RESET}")

        elif choice == "11":
            print()
            print(f"{T_MAGENTA}TYPING MODE - exact keyboard keys{T_RESET}")
            print(f"{T_GRAY}(Pronunciation = how to SAY it, Typing = what to TYPE){T_RESET}")
            print()
            for item in lines_data:
                if item is None:
                    print(f"  {T_GRAY}---{T_RESET}")
                else:
                    translit, english, hebrew, typing = item
                    if typing:
                        print(f"  {T_CYAN}{reverse_for_powershell(hebrew)}{T_RESET}")
                        print(f"  {T_YELLOW}Say: {translit}{T_RESET}")
                        print(f"  {T_MAGENTA}Type: {typing}{T_RESET}")
                        print()

        elif choice == "12":
            output = "```ansi\n"
            for item in lines_data:
                if item is None:
                    output += "\n"
                else:
                    translit, english, hebrew, typing = item
                    if typing:
                        output += f"{D_CYAN}{hebrew}{D_RESET}\n"
                        output += f"{D_YELLOW}Say: {translit}{D_RESET}\n"
                        output += f"\x1b[2;35mType: {typing}\x1b[0m\n\n"
            output = output.rstrip('\n') + "\n```"
            pyperclip.copy(output)
            print(f"{T_GREEN}✓ Typing mode copied!{T_RESET}")

        else:
            print(f"{T_GRAY}Invalid choice{T_RESET}")

if __name__ == "__main__":
    main()
