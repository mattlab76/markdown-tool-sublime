import sublime
import sublime_plugin
import os
import json


def _load_templates(filename):
    """Load a JSON template file from the templates/ directory."""
    plugin_dir = os.path.dirname(__file__)
    path = os.path.join(plugin_dir, "templates", filename)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


class EdiInsertSnippetCommand(sublime_plugin.TextCommand):
    """Generic command that inserts a snippet from a template file.

    Usage in .sublime-commands / .sublime-keymap:
        { "command": "edi_insert_snippet", "args": { "file": "tables.json", "key": "profil" } }
    """

    def run(self, edit, file, key):
        templates = _load_templates(file)
        entry = templates.get(key)
        if entry is None:
            sublime.status_message("EDI Markdown: Template '{}' not found".format(key))
            return
        self.view.run_command("insert_snippet", {"contents": entry["snippet"]})

    def is_enabled(self, file=None, key=None):
        return self.view.match_selector(0, "text.html.markdown")


# ---------------------------------------------------------------------------
# Convenience aliases – one class per table so they show up individually
# in the Command Palette and can be bound without args.
# ---------------------------------------------------------------------------

_TABLE_KEYS = [
    ("profil",   "Profil-Übersichtstabelle"),
    ("felder",   "Feld-Tabelle"),
    ("mapping",  "Mapping-Tabelle"),
    ("var",      "Variablen-Tabelle"),
    ("macro",    "Macro-Tabelle"),
    ("response", "Response Units"),
    ("fehler",   "Fehlerbehandlung"),
    ("lbase",    "Lbase-Feld-Tabelle"),
]


def _make_table_command(key):
    """Factory that creates an EdiInsertTable<Key>Command class."""

    class Cmd(sublime_plugin.TextCommand):
        def run(self, edit):
            self.view.run_command(
                "edi_insert_snippet", {"file": "tables.json", "key": key}
            )

        def is_enabled(self):
            return self.view.match_selector(0, "text.html.markdown")

    # Sublime expects the class name in CamelCase → command name in snake_case
    # e.g. EdiInsertTableProfilCommand → edi_insert_table_profil
    class_name = "EdiInsertTable{}Command".format(key.capitalize())
    Cmd.__name__ = class_name
    Cmd.__qualname__ = class_name
    return Cmd


# Register all table commands in module scope so Sublime discovers them
for _key, _desc in _TABLE_KEYS:
    globals()["EdiInsertTable{}Command".format(_key.capitalize())] = _make_table_command(_key)
