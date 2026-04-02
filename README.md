# EDI Markdown Tools – Sublime Text Plugin

Sublime Text 4 Plugin für das EDI-Team bei Quehenberger Logistics.
Effizientes Erstellen von Markdown-Dokumentationen für Lobster_data Profile,
Macros, Prozessbeschreibungen und Schnittstellendokumentation.

## Quick Start

1. `EDI Markdown Tools.sublime-package` in den `Installed Packages/` Ordner kopieren
2. Sublime Text (neu) starten
3. Eine `.md` Datei öffnen
4. `Ctrl+Shift+P` → "EDI" tippen – alle Commands erscheinen

---

## Features

### Tabellen (Ctrl+Alt+1–8)

8 vordefinierte Tabellen-Templates mit Tab-navigierbaren Platzhaltern:

| Shortcut      | Command Palette                   | Tabelle                  |
|---------------|-----------------------------------|--------------------------|
| `Ctrl+Alt+1`  | EDI: Profil-Übersichtstabelle    | 9-Felder Profil-Tabelle  |
| `Ctrl+Alt+2`  | EDI: Feld-Tabelle                | Feld/Typ/Beschreibung    |
| `Ctrl+Alt+3`  | EDI: Mapping-Tabelle             | Input→Output Mapping     |
| `Ctrl+Alt+4`  | EDI: Variablen-Tabelle           | VAR__/MSG_CALL Variablen |
| `Ctrl+Alt+5`  | EDI: Macro-Tabelle               | Macro/Profil-Aufrufe     |
| `Ctrl+Alt+6`  | EDI: Response Units              | Response Units           |
| `Ctrl+Alt+7`  | EDI: Fehlerbehandlung            | Fehlerbehandlung         |
| `Ctrl+Alt+8`  | EDI: Lbase-Feld-Tabelle          | Feld/Lbase-Ref           |

Nach dem Einfügen: `Tab` drücken um zum nächsten Platzhalter zu springen, Wert eintippen, nächster `Tab`, usw.

### Flowcharts

ASCII-Flowcharts direkt ins Markdown einfügen:

| Command Palette                   | Beschreibung                              |
|-----------------------------------|-------------------------------------------|
| EDI: Flowchart – Einfach          | Linearer Ablauf (3 Schritte)              |
| EDI: Flowchart – Lobster Pipeline | Input → Phase 1 → Phase 2 → Output       |
| EDI: Flowchart – Entscheidung     | If/Else Verzweigung                       |
| EDI: Flowchart – Fehlerbehandlung | Prozess mit Error-Handling Branch          |
| EDI: Flowchart – Wizard...        | Interaktiv: Schritte + Titel → Flowchart  |

**Flowchart-Wizard** (`Ctrl+Alt+G`):
1. Anzahl Schritte eingeben (2–10)
2. Titel eingeben
3. Fertiger ASCII-Flowchart wird generiert

### Dokument-Gerüste (Ctrl+Alt+D)

Vollständige Dokumentations-Vorlagen über Quick Panel auswählen:

| Command Palette                   | Inhalt                                              |
|-----------------------------------|-----------------------------------------------------|
| EDI: Neue Profil-Dokumentation    | Übersicht, Felder, Mapping, Variablen, Fehler       |
| EDI: Neue Bereichsseite          | Team/Abteilung mit Profil-Liste, Ansprechpartner    |
| EDI: Neue Prozess-Beschreibung   | Ablauf mit Flowchart, Schritte, Fehlerszenarien      |
| EDI: Neue Macro-Dokumentation    | Parameter, Variablen, Logik, Aufrufe, Beispiel       |

### Eigene Vorlagen

Eigene Text-Bausteine speichern und wiederverwenden:

| Shortcut      | Command Palette                          | Beschreibung                    |
|---------------|------------------------------------------|---------------------------------|
| `Ctrl+Alt+S`  | EDI: Auswahl als Vorlage speichern...   | Markierten Text als Vorlage speichern |
| `Ctrl+Alt+U`  | EDI: Eigene Vorlage einfügen...         | Gespeicherte Vorlage einfügen   |
| —             | EDI: Eigene Vorlage löschen...           | Vorlage aus der Liste entfernen |

**Workflow:**
1. Text markieren → `Ctrl+Alt+S`
2. Name eingeben (z.B. "Meine Mapping-Tabelle")
3. Kategorie wählen: `tabelle`, `flowchart`, `dokument` oder `sonstig`
4. Später: `Ctrl+Alt+U` → Vorlage aus Quick Panel wählen

Eigene Vorlagen werden in `Packages/User/EDI Markdown Tools/user_templates.json` gespeichert und bleiben bei Plugin-Updates erhalten.

**Tipp:** Platzhalter mit Sublime-Syntax `${1:Standardwert}` in der Vorlage machen sie Tab-navigierbar!

### Autocomplete

Tippe einen Prefix und wähle aus der Autocomplete-Liste:

| Prefix   | Zeigt                                        | Badge |
|----------|----------------------------------------------|-------|
| `tbl.`   | Alle Tabellen-Templates                     | **E** |
| `flow.`  | Alle Flowchart-Templates                    | **E** |
| `doc.`   | Alle Dokument-Gerüste                       | **E** |
| `my.`    | Eigene gespeicherte Vorlagen                | **U** |

Beispiele:
```
tbl.profil    → Profil-Übersichtstabelle
tbl.mapping   → Mapping-Tabelle
flow.lobster  → Lobster Pipeline
doc.prozess   → Prozess-Beschreibung
my.mein_block → Eigene Vorlage "Mein Block"
```

### Tabellen-Formatter (Ctrl+Alt+F)

Cursor in eine Markdown-Tabelle setzen und `Ctrl+Alt+F` drücken –
alle Spalten werden automatisch ausgerichtet.

**Vorher:**
```markdown
| Feld | Typ | Beschreibung |
|---|---|---|
| Partner_ID | String | ID des Partners |
| Nachrichtentyp | String | ORDERS, DESADV, etc. |
```

**Nachher:**
```markdown
| Feld             | Typ    | Beschreibung          |
|------------------|--------|-----------------------|
| Partner_ID       | String | ID des Partners       |
| Nachrichtentyp   | String | ORDERS, DESADV, etc.  |
```

Alignment-Markierungen (`:---`, `:---:`, `---:`) bleiben erhalten.

---

## Alle Shortcuts

| Shortcut        | Aktion                                |
|-----------------|---------------------------------------|
| `Ctrl+Alt+1–8`  | Tabellen 1–8 einfügen                |
| `Ctrl+Alt+F`    | Tabelle unter Cursor formatieren     |
| `Ctrl+Alt+D`    | Dokument-Gerüst Quick Panel          |
| `Ctrl+Alt+G`    | Flowchart-Wizard starten             |
| `Ctrl+Alt+S`    | Auswahl als eigene Vorlage speichern |
| `Ctrl+Alt+U`    | Eigene Vorlage einfügen              |

Alle Shortcuts sind **nur in `.md` Dateien** aktiv.

---

## Menü

**Tools → EDI Markdown** mit folgenden Untermenüs:

```
Tools
└── EDI Markdown
    ├── Tabellen
    │   ├── Profil-Übersicht        (Ctrl+Alt+1)
    │   ├── Feld-Tabelle            (Ctrl+Alt+2)
    │   ├── Mapping-Tabelle         (Ctrl+Alt+3)
    │   ├── Variablen-Tabelle       (Ctrl+Alt+4)
    │   ├── Macro-Tabelle           (Ctrl+Alt+5)
    │   ├── Response Units          (Ctrl+Alt+6)
    │   ├── Fehlerbehandlung        (Ctrl+Alt+7)
    │   └── Lbase-Feld-Tabelle      (Ctrl+Alt+8)
    ├── Flowcharts
    │   ├── Einfach
    │   ├── Lobster Pipeline
    │   ├── Entscheidung
    │   ├── Fehlerbehandlung
    │   └── Wizard...               (Ctrl+Alt+G)
    ├── Neue Dokumentation
    │   ├── Profil-Dokumentation
    │   ├── Bereichsseite
    │   ├── Prozess-Beschreibung
    │   └── Macro-Dokumentation
    ├── Eigene Vorlagen
    │   ├── Vorlage einfügen...     (Ctrl+Alt+U)
    │   ├── Auswahl als Vorlage speichern... (Ctrl+Alt+S)
    │   └── Vorlage löschen...
    └── Tabelle formatieren         (Ctrl+Alt+F)
```

---

## Installation

### Schnell-Installation (empfohlen)

1. Datei `EDI Markdown Tools.sublime-package` herunterladen
2. In den `Installed Packages/` Ordner kopieren:
   - **Windows Portable:** `Data/Installed Packages/`
   - **Windows Standard:** `%APPDATA%\Sublime Text\Installed Packages\`
   - **Linux:** `~/.config/sublime-text/Installed Packages/`
3. Sublime Text (neu) starten – fertig!

### Manuelle Installation (Entwicklung)

1. Dieses Repository klonen oder herunterladen
2. Den Ordner in `Packages/` kopieren oder symlinken:
   - **Windows Portable:** `Data/Packages/EDI Markdown Tools/`
   - **Windows Standard:** `%APPDATA%\Sublime Text\Packages\EDI Markdown Tools\`
   - **Linux:** `~/.config/sublime-text/Packages/EDI Markdown Tools/`
3. Kein Neustart nötig – Plugin wird sofort geladen

### Ordnerstruktur

```
EDI Markdown Tools/
├── edi_markdown.py               # Haupt-Plugin (Commands, User Templates)
├── edi_markdown_completions.py   # Autocomplete Provider (tbl/flow/doc/my)
├── edi_markdown_formatter.py     # Tabellen-Formatter
├── edi_markdown_wizard.py        # Flowchart-Wizard (interaktiv)
├── templates/
│   ├── tables.json               # 8 Tabellen-Templates
│   ├── flowcharts.json           # 4 Flowchart-Templates
│   └── documents.json            # 4 Dokument-Gerüste
├── Default.sublime-commands      # Command Palette Einträge
├── Default.sublime-keymap        # Keyboard Shortcuts
├── Main.sublime-menu             # Tools-Menü
└── edi_markdown.sublime-settings # Default-Einstellungen
```

User-Templates werden separat gespeichert in:
```
Packages/User/EDI Markdown Tools/user_templates.json
```

---

## Einstellungen

Über `edi_markdown.sublime-settings` konfigurierbar:

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
| `default_encoding`   | Standard-Encoding für neue Dokumente            | `UTF-8`          |
| `flowchart_style`    | Flowchart-Stil (`boxed` / `simple`)             | `boxed`          |
| `auto_format_tables` | Tabelle nach Einfügen automatisch formatieren   | `false`          |
| `placeholder_style`  | Platzhalter-Syntax (`sublime` / `backticks`)    | `sublime`        |

---

## Kompatibilität

- Sublime Text 4 (Build 4000+)
- Windows & Linux
- Portable-Installation kompatibel

## Lizenz

MIT
