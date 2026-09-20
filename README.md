# Hebrew Discord Formatter

Paste Hebrew lyrics, get Discord-ready ANSI colored output.

## Install

```bash
pip install -r requirements.txt
```

## Usage

```bash
python hebrew_to_discord.py
```

1. Paste Hebrew lyrics (one line per verse)
2. Enter empty line when done
3. Auto-translates or manually enter English
4. Output copied to clipboard - paste in Discord

## Output Format

```ansi
Hakol tov, hakol tov       (yellow - transliteration)
Everything's good          (white - english)
```

## Manual Mode

If you already have transliteration + English, edit the script or use:

```python
from hebrew_to_discord import format_for_discord
output = format_for_discord(["שלום"], ["Hello"])
```
