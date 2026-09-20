# Hebrew Discord Formatter

Learn Hebrew through songs. Paste lyrics, get pronunciation + translation + Discord colors.

## Install

```powershell
pip install -r requirements.txt
```

Requirements: `pyperclip`, `deep-translator`

## Usage

```powershell
python hebrew_to_discord.py
```

1. Paste Hebrew lyrics
2. Type `END` on new line
3. Choose from menu options

## Menu Options

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

## Discord Colors

```
בקרוב תזרח השמש          <- cyan (hebrew)
Bekarov Tizrach Hashemesh  <- yellow (transliteration)
The sun is coming up       <- white (english)
```

## Features

### Transliteration (Offline)
- 40+ common Hebrew words pre-mapped (שלום, ישראל, אהבה, etc.)
- Vowel inference for unknown words
- No internet needed

### Translation (Online)
- Uses MyMemory API
- Requires internet
- Falls back to `[translation error]` if offline

### Auto-Chunking (Non-Nitro)
- Discord limit: 2000 chars without Nitro
- Export options 8/9 auto-split into multiple files
- Each file = one Discord message

### PowerShell RTL Fix
- Hebrew auto-reversed for terminal display
- PowerShell's broken RTL re-reverses it = correct display
- Copy/export stays original (correct)

## Example

Input:
```
בקרוב תזרח השמש
נדע ימים יפים מאלה
END
```

Terminal Output (Option 2):
```
בקרוב תזרח השמש
Bekarov Tizrach Hashemesh
The sun is coming up

נדע ימים יפים מאלה
Neda Yamim Yafim Me'ele
We will know better days than these
```

## Files

| File | Purpose |
|------|---------|
| `hebrew_to_discord.py` | Main script |
| `requirements.txt` | Dependencies |
| `lyrics_with_hebrew_*.md` | Markdown with Hebrew |
| `lyrics_translit_only_*.md` | Markdown without Hebrew |
| `lyrics_discord_*.txt` | Discord ANSI format |
| `lyrics_discord_heb_*.txt` | Discord with Hebrew |
