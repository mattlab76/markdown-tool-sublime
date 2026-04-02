# Sublime Text Plugin: EDI Markdown Tools

## Projektübersicht

Ein Sublime Text 4 Plugin für das EDI-Team bei Quehenberger Logistics.  
Ziel: Effizientes Erstellen von Markdown-Dokumentationen für Lobster_data Profile,
Macros, Prozessbeschreibungen und Schnittstellendokumentation.

**Repo:** `mattlab76/sublime-edi-markdown`  
**Sprache:** Python 3 (Sublime Text API)  
**Kompatibilität:** Sublime Text 4, Windows + Linux, Portable-fähig

---

## Projektstruktur

```
sublime-edi-markdown/
├── edi_markdown.py               # Haupt-Plugin (Commands)
├── edi_markdown_completions.py   # Autocomplete Provider
├── edi_markdown_formatter.py     # Tabellen-Formatter
├── edi_markdown_wizard.py        # Flowchart-Wizard Dialog
├── templates/                    # Eingebettete Templates (JSON)
│   ├── tables.json               # Alle Tabellen-Definitionen
│   ├── flowcharts.json           # Alle Flowchart-Templates
│   └── documents.json            # Dokument-Gerüste
├── Default.sublime-commands      # Command Palette Einträge
├── Default.sublime-keymap        # Keyboard Shortcuts
├── Main.sublime-menu             # Menü-Einträge unter Tools
├── edi_markdown.sublime-settings # Default-Einstellungen
└── README.md
```

---

## Phase 1 – Basis (MVP)

### 1.1 Tabellen einfügen

Jede Tabelle als Snippet-String in `templates/tables.json`.  
Ein generischer `EdiInsertSnippetCommand` nimmt den Template-Key entgegen.  
Platzhalter mit Sublime `${}` Syntax für Tab-Navigation.

| Command ID               | Palette-Name                    | Shortcut     | Beschreibung              |
|--------------------------|---------------------------------|--------------|---------------------------|
| `edi_insert_table_profil`  | EDI: Profil-Übersichtstabelle | `Ctrl+Alt+1` | 9-Felder Profil-Tabelle   |
| `edi_insert_table_felder`  | EDI: Feld-Tabelle             | `Ctrl+Alt+2` | Feld/Typ/Beschreibung     |
| `edi_insert_table_mapping` | EDI: Mapping-Tabelle          | `Ctrl+Alt+3` | Input→Output Mapping      |
| `edi_insert_table_var`     | EDI: Variablen-Tabelle        | `Ctrl+Alt+4` | VAR__/MSG_CALL Variablen  |
| `edi_insert_table_macro`   | EDI: Macro-Tabelle            | `Ctrl+Alt+5` | Macro/Profil-Aufrufe      |
| `edi_insert_table_response`| EDI: Response Units           | `Ctrl+Alt+6` | Response Units            |
| `edi_insert_table_fehler`  | EDI: Fehlerbehandlung         | `Ctrl+Alt+7` | Fehlerbehandlung          |
| `edi_insert_table_lbase`   | EDI: Lbase-Feld-Tabelle       | `Ctrl+Alt+8` | Feld/Lbase-Ref/Beschreibung |

### 1.2 Menü-Integration (Main.sublime-menu)

```json
[
  {
    "caption": "Tools",
    "children": [
      {
        "caption": "EDI Markdown",
        "children": [
          {
            "caption": "Tabellen",
            "children": [
              { "caption": "Profil-Übersicht",  "command": "edi_insert_table_profil" },
              { "caption": "Feld-Tabelle",       "command": "edi_insert_table_felder" },
              { "caption": "Mapping-Tabelle",    "command": "edi_insert_table_mapping" },
              { "caption": "Variablen-Tabelle",  "command": "edi_insert_table_var" },
              { "caption": "Macro-Tabelle",      "command": "edi_insert_table_macro" },
              { "caption": "Response Units",     "command": "edi_insert_table_response" },
              { "caption": "Fehlerbehandlung",   "command": "edi_insert_table_fehler" },
              { "caption": "Lbase-Feld-Tabelle", "command": "edi_insert_table_lbase" }
            ]
          },
          {
            "caption": "Flowcharts",
            "children": [
              { "caption": "Einfach",           "command": "edi_insert_flow_simple" },
              { "caption": "Lobster Pipeline",  "command": "edi_insert_flow_lobster" },
              { "caption": "Wizard...",         "command": "edi_insert_flow_wizard" }
            ]
          },
          {
            "caption": "Neue Dokumentation",
            "children": [
              { "caption": "Profil-Dokumentation", "command": "edi_insert_doc_profil" },
              { "caption": "Bereichsseite",         "command": "edi_insert_doc_bereich" },
              { "caption": "Prozess-Beschreibung",  "command": "edi_insert_doc_prozess" },
              { "caption": "Macro-Dokumentation",   "command": "edi_insert_doc_macro" }
            ]
          },
          { "caption": "-" },
          { "caption": "Tabelle formatieren", "command": "edi_format_table" }
        ]
      }
    ]
  }
]
```

### 1.3 Keyboard Shortcuts (nur aktiv in `.md` Dateien)

| Shortcut       | Aktion                        |
|----------------|-------------------------------|
| `Ctrl+Alt+1–8` | Tabellen 1–8 einfügen         |
| `Ctrl+Alt+F`   | Tabelle unter Cursor formatieren |
| `Ctrl+Alt+D`   | Dokument-Gerüst Menü öffnen   |
| `Ctrl+Alt+G`   | Flowchart-Wizard starten      |

Alle Shortcuts nur aktiv mit `"selector": "text.html.markdown"`.

---

## Phase 2 – Flowcharts & Dokument-Gerüste

- Alle Flowchart-Templates (einfach, Lobster Pipeline, mit Entscheidung, etc.)
- **Flowchart-Wizard:** Input-Dialog – Anzahl Schritte eingeben → ASCII-Flowchart wird generiert
- Vollständige Dokument-Gerüste (Profil, Bereich, Prozess, Macro) als einfügbare Templates
- Platzhalter navigierbar mit Tab

---

## Phase 3 – Autocomplete & Formatter

- **Autocomplete Provider:** Tippt man `tbl`, `flow`, `doc` erscheinen alle Optionen mit Beschreibung
- **Tabellen-Formatter:** Cursor in Tabelle → `Ctrl+Alt+F` richtet alle Spalten automatisch aus
- Optional: Auto-Format direkt nach dem Einfügen

---

## Phase 4 – Polish & Release

- Settings-System (`edi_markdown.sublime-settings`)
- README mit Screenshots
- GitHub Release als `mattlab76/sublime-edi-markdown`
- Optional: Package Control Submission

---

## Plugin-Einstellungen (edi_markdown.sublime-settings)

```json
{
    "default_author": "Matthias Haas",
    "default_encoding": "UTF-8",
    "flowchart_style": "boxed",
    "auto_format_tables": true,
    "placeholder_style": "backticks"
}
```

---

## Installation

### Portable (Windows Arbeit / Linux Home)

1. Ordner `edi-markdown` in `Packages/` kopieren
2. Fertig – kein Neustart nötig

### Package Control (später, Phase 4)

```
Ctrl+Shift+P → Install Package → EDI Markdown Tools
```

---

## Claude Code Workflow

```bash
# Repo erstellen
cd ~/projects
mkdir sublime-edi-markdown && cd sublime-edi-markdown
git init

# PLAN.md reinkopieren, dann Claude Code starten
claude
```

**Empfohlener Startprompt für Claude Code:**

```
Erstelle ein Sublime Text 4 Plugin basierend auf dem Plan in PLAN.md.
Starte mit Phase 1: alle Tabellen-Commands (edi_insert_table_*),
Command Palette, Menü unter Tools → EDI Markdown, und Keyboard Shortcuts.
Templates als JSON in templates/tables.json, Platzhalter mit Sublime ${}-Syntax.
Referenz für Plugin-Struktur: mein EDIFACT-Plugin (gleiche Codebasis).
```

---

## Referenzen

- Sublime Text Plugin API: https://www.sublimetext.com/docs/api_reference.html
- Sublime Text Completions: https://www.sublimetext.com/docs/completions.html
- Dein EDIFACT-Plugin: Referenz für Plugin-Struktur und Input-Handler
- Master-Prompt v6+: Basis für die Dokumentations-Templates (Tabellen-Inhalte)
