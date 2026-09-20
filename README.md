# Hebrew Discord Formatter

Learn Hebrew through songs. Paste lyrics, get pronunciation + translation + Discord colors. Practice typing with Windows Hebrew keyboard.

![Preview](preview.png)
![Typing Practice](שלום.png)

## Install

```powershell
pip install -r requirements.txt
```

Requirements: `pyperclip`, `deep-translator`

## Usage

```powershell
python hebrew_to_discord.py
```

## Main Menu

| Option | Description |
|--------|-------------|
| 1 | Paste & process lyrics |
| 2 | Typing practice (English → Hebrew + keyboard keys) |

## Option 1: Lyrics Workflow

1. Paste Hebrew lyrics
2. Type `END` on new line
3. Choose from output options

### Display (Terminal)
| Option | Description |
|--------|-------------|
| 1 | Show transliteration + English |
| 2 | Show all 3: Hebrew + transliteration + English |
| 3 | Show plain text (no colors) |

### Copy (Clipboard)
| Option | Description |
|--------|-------------|
| 4 | Copy Discord ANSI (full song - use with Nitro) |
| 5 | Copy plain text |

### Export (Save to File)
| Option | Description |
|--------|-------------|
| 6 | Save Markdown (with Hebrew) |
| 7 | Save Markdown (transliteration only) |
| 8 | Save Discord (translit + english) - auto-chunks for non-Nitro |
| 9 | Save Discord (hebrew + translit + english) - auto-chunks |
| 10 | Save ALL formats |

### Typing Mode
| Option | Description |
|--------|-------------|
| 11 | Show typing (keyboard keys to press) |
| 12 | Copy typing for Discord |
| M | Back to main menu |

## Option 2: Typing Practice

Interactive mode with visual QWERTY → Hebrew keyboard reference:

```
  ┌───┬───┬───┬───┬───┬───┬───┬───┬───┬───┐
  │ Q │ W │ E │ R │ T │ Y │ U │ I │ O │ P │
  │ / │ ' │ ק │ ר │ א │ ט │ ו │ ן │ ם │ פ │
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
  │ A │ S │ D │ F │ G │ H │ J │ K │ L │ ; │
  │ ש │ ד │ ג │ כ │ ע │ י │ ח │ ל │ ך │ ף │
  ├───┼───┼───┼───┼───┼───┼───┼───┼───┼───┤
  │ Z │ X │ C │ V │ B │ N │ M │ , │ . │
  │ ז │ ס │ ב │ ה │ נ │ מ │ צ │ ת │ ץ │
  └───┴───┴───┴───┴───┴───┴───┴───┴───┴───┘
```

Type English words, get:
- **Hebrew:** שלום (actual translation)
- **Say:** Shalom (pronunciation)
- **Type:** AKUO (Windows Hebrew keyboard keys)

### Windows Hebrew Keyboard Setup

1. Windows Settings → Time & Language → Language
2. Add Hebrew
3. Use "Hebrew" layout (not "Standard")
4. Win+Space to switch keyboards

### Example Words

| English | Hebrew | Say | Type |
|---------|--------|-----|------|
| peace/hello | שלום | Shalom | AKUO |
| thanks | תודה | Toda | ,USV |
| yes | כן | Ken | FI |
| no | לא | Lo | KT |
| what | מה | Ma | NV |
| love | אהבה | Ahava | TVCT |

## Discord Colors

```
בקרוב תזרח השמש          <- cyan (hebrew)
Bekarov Tizrach Hashemesh  <- yellow (transliteration)
The sun is coming up       <- white (english)
```

## Features

### Windows Hebrew Keyboard Support
- Visual QWERTY → Hebrew keyboard map
- Shows exact keys to press (AKUO not "shalom")
- Works with Windows Standard Hebrew layout

### Transliteration (Offline)
- 40+ common Hebrew words pre-mapped
- Vowel inference for unknown words
- No internet needed

### Translation (Online)
- Uses MyMemory API
- Requires internet
- Falls back to `[translation error]` if offline

### Auto-Chunking (Non-Nitro)
- Discord limit: 2000 chars without Nitro
- Export options 8/9 auto-split into multiple files

### PowerShell RTL Fix
- Hebrew auto-reversed for terminal display
- PowerShell's broken RTL re-reverses it = correct display
