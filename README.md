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
| 1 | Show transliteration + English (no Hebrew) |
| 2 | Show all 3: Hebrew + transliteration + English |
| 3 | Show plain text (no colors) |

### Copy (Clipboard)
| Option | Description |
|--------|-------------|
| 4 | Copy Discord ANSI format (colored in Discord) |
| 5 | Copy plain text |

### Export (Save to File)
| Option | Description |
|--------|-------------|
| 6 | Save Markdown with Hebrew |
| 7 | Save Markdown without Hebrew |
| 8 | Save Discord format (.txt) |
| 9 | Save ALL formats |

## Features

### Transliteration (Offline)
- 40+ common Hebrew words pre-mapped
- Vowel inference for unknown words
- No internet needed

### Translation (Online)
- Uses MyMemory API
- Requires internet
- Falls back to `[translation error]` if offline

### PowerShell RTL Fix
- Hebrew auto-reversed for terminal display
- PowerShell's broken RTL re-reverses it = correct display
- Copy/export stays original

## Example

Input:
```
בקרוב תזרח השמש
END
```

Output:
```
Bekarov Tizrach Hashemesh
The sun is coming up
```

## Discord Output

Paste in Discord for colored text:
- Yellow: Transliteration (pronunciation)
- White: English translation

## Files

- `hebrew_to_discord.py` - Main script
- `requirements.txt` - Dependencies
- `lyrics_*.md` - Exported markdown files
- `lyrics_*.txt` - Exported plain/Discord files
