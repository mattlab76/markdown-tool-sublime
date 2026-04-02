# EDI Markdown Tools – Sublime Text Plugin

Sublime Text 4 Plugin für das EDI-Team bei Quehenberger Logistics.
Effizientes Erstellen von Markdown-Dokumentationen für Lobster_data Profile,
Macros, Prozessbeschreibungen und Schnittstellendokumentation.

## Features

### Tabellen (Ctrl+Alt+1–8)

8 vordefinierte Tabellen-Templates mit Tab-navigierbaren Platzhaltern:

| Shortcut      | Tabelle                  |
|---------------|--------------------------|
| `Ctrl+Alt+1`  | Profil-Übersichtstabelle |
| `Ctrl+Alt+2`  | Feld-Tabelle             |
| `Ctrl+Alt+3`  | Mapping-Tabelle          |
| `Ctrl+Alt+4`  | Variablen-Tabelle        |
| `Ctrl+Alt+5`  | Macro-Tabelle            |
| `Ctrl+Alt+6`  | Response Units           |
| `Ctrl+Alt+7`  | Fehlerbehandlung         |
| `Ctrl+Alt+8`  | Lbase-Feld-Tabelle       |

### Flowcharts

ASCII-Flowcharts direkt ins Markdown einfügen:

- **Einfacher Flowchart** – Linearer Ablauf (3 Schritte)
- **Lobster Pipeline** – Input → Phasen → Output
- **Entscheidung** – If/Else Verzweigung
- **Fehlerbehandlung** – Prozess mit Error-Handling
- **Wizard** (`Ctrl+Alt+G`) – Anzahl Schritte + Titel eingeben → Flowchart wird generiert

### Dokument-Gerüste (Ctrl+Alt+D)

Vollständige Dokumentations-Vorlagen:

- **Profil-Dokumentation** – Übersicht, Felder, Mapping, Variablen, Fehlerbehandlung
- **Bereichsseite** – Team/Abteilung mit Profil-Liste und Ansprechpartnern
- **Prozess-Beschreibung** – Ablauf mit Flowchart und Fehlerszenarien
- **Macro-Dokumentation** – Parameter, Variablen, Logik, Aufrufe

### Autocomplete

Tippe `tbl.`, `flow.` oder `doc.` um alle verfügbaren Templates zu sehen:

```
tbl.profil    → Profil-Übersichtstabelle
tbl.mapping   → Mapping-Tabelle
flow.lobster  → Lobster Pipeline
doc.prozess   → Prozess-Beschreibung
...
```

### Tabellen-Formatter (Ctrl+Alt+F)

Cursor in eine Markdown-Tabelle setzen und `Ctrl+Alt+F` drücken –
alle Spalten werden automatisch ausgerichtet. Alignment-Markierungen (`:---:`) bleiben erhalten.

## Alle Shortcuts

| Shortcut        | Aktion                           |
|-----------------|----------------------------------|
| `Ctrl+Alt+1–8`  | Tabellen 1–8 einfügen           |
| `Ctrl+Alt+F`    | Tabelle unter Cursor formatieren |
| `Ctrl+Alt+D`    | Dokument-Gerüst Menü            |
| `Ctrl+Alt+G`    | Flowchart-Wizard                |

Alle Shortcuts sind nur in `.md` Dateien aktiv.

## Menü

**Tools → EDI Markdown** mit Untermenüs für Tabellen, Flowcharts und Dokumentation.

## Installation

### Manuell (Portable)

1. Diesen Ordner in das Sublime Text `Packages/` Verzeichnis kopieren oder symlinken:
   - Windows: `%APPDATA%\Sublime Text\Packages\`
   - Linux: `~/.config/sublime-text/Packages/`
   - Portable: `Data/Packages/`
2. Fertig – kein Neustart nötig.

### Ordnerstruktur

```
EDI Markdown Tools/
├── edi_markdown.py               # Haupt-Plugin (Commands)
├── edi_markdown_completions.py   # Autocomplete Provider
├── edi_markdown_formatter.py     # Tabellen-Formatter
├── edi_markdown_wizard.py        # Flowchart-Wizard
├── templates/
│   ├── tables.json               # Tabellen-Templates
│   ├── flowcharts.json           # Flowchart-Templates
│   └── documents.json            # Dokument-Gerüste
├── Default.sublime-commands      # Command Palette
├── Default.sublime-keymap        # Keyboard Shortcuts
├── Main.sublime-menu             # Tools-Menü
└── edi_markdown.sublime-settings # Einstellungen
```

## Einstellungen

`Preferences → Package Settings → EDI Markdown` oder direkt in `edi_markdown.sublime-settings`:

```json
{
    "default_author": "Matthias Haas",
    "default_encoding": "UTF-8",
    "flowchart_style": "boxed",
    "auto_format_tables": false,
    "placeholder_style": "sublime"
}
```

| Setting              | Beschreibung                                    | Default          |
|----------------------|-------------------------------------------------|------------------|
| `default_author`     | Wird als Autor-Platzhalter in Templates gesetzt | `Matthias Haas`  |
| `default_encoding`   | Standard-Encoding                               | `UTF-8`          |
| `flowchart_style`    | Flowchart-Stil (`boxed` / `simple`)             | `boxed`          |
| `auto_format_tables` | Tabelle nach Einfügen automatisch formatieren   | `false`          |
| `placeholder_style`  | Platzhalter-Syntax (`sublime` / `backticks`)    | `sublime`        |

## Kompatibilität

- Sublime Text 4 (Build 4000+)
- Windows & Linux
- Portable-Installation kompatibel

## Lizenz

MIT
