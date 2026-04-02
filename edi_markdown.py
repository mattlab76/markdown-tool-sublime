import sublime
import sublime_plugin
import json
import os


# Package name used for sublime.load_resource() – works both from
# Packages/ folder and from .sublime-package (ZIP) files.
_PACKAGE_NAME = "EDI Markdown Tools"

# User templates are stored in Packages/User/EDI Markdown Tools/
_USER_TEMPLATES_DIR = os.path.join(
    sublime.packages_path(), "User", _PACKAGE_NAME
) if hasattr(sublime, "packages_path") else ""


def _ensure_user_templates_dir():
    """Create the user templates directory if it doesn't exist."""
    d = os.path.join(sublime.packages_path(), "User", _PACKAGE_NAME)
    if not os.path.isdir(d):
        os.makedirs(d)
    return d


def _user_templates_path():
    """Return path to the user's custom templates JSON file."""
    return os.path.join(_ensure_user_templates_dir(), "user_templates.json")


def _load_user_templates():
    """Load user-defined templates from Packages/User/EDI Markdown Tools/."""
    path = _user_templates_path()
    if os.path.isfile(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def _save_user_templates(data):
    """Save user-defined templates to Packages/User/EDI Markdown Tools/."""
    path = _user_templates_path()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def _load_templates(filename):
    """Load a JSON template file from the templates/ directory."""
    resource = "Packages/{}/templates/{}".format(_PACKAGE_NAME, filename)
    try:
        raw = sublime.load_resource(resource)
        return json.loads(raw)
    except Exception:
        # Fallback: try loading from loose files (dev/symlink installs)
        plugin_dir = os.path.dirname(__file__)
        path = os.path.join(plugin_dir, "templates", filename)
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)


def _get_setting(key, default=None):
    """Read a value from edi_markdown.sublime-settings."""
    settings = sublime.load_settings("edi_markdown.sublime-settings")
    return settings.get(key, default)


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

        snippet = entry["snippet"]

        # Substitute default_author setting into templates
        author = _get_setting("default_author", "Autor")
        snippet = snippet.replace("${2:Matthias Haas}", "${2:" + author + "}")
        snippet = snippet.replace("${4:Matthias Haas}", "${4:" + author + "}")
        snippet = snippet.replace("${9:Autor}", "${9:" + author + "}")

        self.view.run_command("insert_snippet", {"contents": snippet})

        # Auto-format table after insertion if enabled
        if _get_setting("auto_format_tables", False) and file == "tables.json":
            sublime.set_timeout(lambda: self.view.run_command("edi_format_table"), 50)

    def is_enabled(self, file=None, key=None):
        return self.view.match_selector(0, "text.html.markdown")


class EdiInsertSnippetUserCommand(sublime_plugin.TextCommand):
    """Insert a user-defined template by key (used by autocomplete)."""

    def run(self, edit, key):
        templates = _load_user_templates()
        entry = templates.get(key)
        if entry is None:
            sublime.status_message("EDI Markdown: Vorlage '{}' nicht gefunden".format(key))
            return
        self.view.run_command("insert_snippet", {"contents": entry["snippet"]})

    def is_enabled(self, key=None):
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


# ---------------------------------------------------------------------------
# Flowchart commands
# ---------------------------------------------------------------------------

_FLOW_KEYS = [
    ("simple",         "Einfacher Flowchart"),
    ("lobster",        "Lobster Pipeline"),
    ("decision",       "Flowchart mit Entscheidung"),
    ("error_handling", "Flowchart mit Fehlerbehandlung"),
]


def _make_flow_command(key):
    """Factory that creates an EdiInsertFlow<Key>Command class."""

    class Cmd(sublime_plugin.TextCommand):
        def run(self, edit):
            self.view.run_command(
                "edi_insert_snippet", {"file": "flowcharts.json", "key": key}
            )

        def is_enabled(self):
            return self.view.match_selector(0, "text.html.markdown")

    class_name = "EdiInsertFlow{}Command".format(
        key.replace("_", " ").title().replace(" ", "")
    )
    Cmd.__name__ = class_name
    Cmd.__qualname__ = class_name
    return Cmd


for _key, _desc in _FLOW_KEYS:
    globals()[
        "EdiInsertFlow{}Command".format(
            _key.replace("_", " ").title().replace(" ", "")
        )
    ] = _make_flow_command(_key)


# ---------------------------------------------------------------------------
# Document scaffold commands
# ---------------------------------------------------------------------------

_DOC_KEYS = [
    ("profil",  "Profil-Dokumentation"),
    ("bereich", "Bereichsseite"),
    ("prozess", "Prozess-Beschreibung"),
    ("macro",   "Macro-Dokumentation"),
]


def _make_doc_command(key):
    """Factory that creates an EdiInsertDoc<Key>Command class."""

    class Cmd(sublime_plugin.TextCommand):
        def run(self, edit):
            self.view.run_command(
                "edi_insert_snippet", {"file": "documents.json", "key": key}
            )

        def is_enabled(self):
            return self.view.match_selector(0, "text.html.markdown")

    class_name = "EdiInsertDoc{}Command".format(key.capitalize())
    Cmd.__name__ = class_name
    Cmd.__qualname__ = class_name
    return Cmd


for _key, _desc in _DOC_KEYS:
    globals()["EdiInsertDoc{}Command".format(_key.capitalize())] = _make_doc_command(_key)


# ---------------------------------------------------------------------------
# Quick-panel menu for Ctrl+Alt+D → pick a document type
# ---------------------------------------------------------------------------

class EdiDocMenuCommand(sublime_plugin.TextCommand):
    """Shows a quick panel to choose a document scaffold."""

    def run(self, edit):
        self._items = list(_DOC_KEYS)
        labels = [desc for _key, desc in self._items]
        self.view.window().show_quick_panel(labels, self._on_select)

    def _on_select(self, index):
        if index == -1:
            return
        key = self._items[index][0]
        self.view.run_command(
            "edi_insert_snippet", {"file": "documents.json", "key": key}
        )

    def is_enabled(self):
        return self.view.match_selector(0, "text.html.markdown")


# ---------------------------------------------------------------------------
# User templates – save selection as template / insert user template
# ---------------------------------------------------------------------------

class EdiSaveTemplateCommand(sublime_plugin.TextCommand):
    """Save the current selection as a reusable user template."""

    def run(self, edit):
        sel = self.view.sel()
        if not sel or sel[0].empty():
            sublime.status_message("EDI Markdown: Bitte zuerst Text markieren")
            return

        self._content = self.view.substr(sel[0])
        self.view.window().show_input_panel(
            "Vorlagen-Name:", "", self._on_name, None, None
        )

    def _on_name(self, name):
        name = name.strip()
        if not name:
            return

        self._name = name
        self.view.window().show_input_panel(
            "Kategorie (tabelle/flowchart/dokument/sonstig):",
            "sonstig",
            self._on_category,
            None, None,
        )

    def _on_category(self, category):
        category = category.strip().lower() or "sonstig"
        key = self._name.lower().replace(" ", "_").replace("-", "_")

        templates = _load_user_templates()
        templates[key] = {
            "name": self._name,
            "category": category,
            "description": self._name,
            "snippet": self._content,
        }
        _save_user_templates(templates)
        sublime.status_message(
            "EDI Markdown: Vorlage '{}' gespeichert".format(self._name)
        )

    def is_enabled(self):
        return self.view.match_selector(0, "text.html.markdown")


class EdiInsertUserTemplateCommand(sublime_plugin.TextCommand):
    """Show a quick panel of user-defined templates and insert the chosen one."""

    def run(self, edit):
        templates = _load_user_templates()
        if not templates:
            sublime.status_message("EDI Markdown: Keine eigenen Vorlagen vorhanden")
            return

        self._keys = list(templates.keys())
        self._templates = templates

        labels = []
        for k in self._keys:
            t = templates[k]
            labels.append(
                sublime.QuickPanelItem(
                    trigger=t.get("name", k),
                    annotation=t.get("category", ""),
                    details=t.get("description", ""),
                )
            )

        self.view.window().show_quick_panel(labels, self._on_select)

    def _on_select(self, index):
        if index == -1:
            return
        key = self._keys[index]
        snippet = self._templates[key]["snippet"]
        self.view.run_command("insert_snippet", {"contents": snippet})

    def is_enabled(self):
        return self.view.match_selector(0, "text.html.markdown")


class EdiDeleteUserTemplateCommand(sublime_plugin.TextCommand):
    """Show a quick panel to delete a user-defined template."""

    def run(self, edit):
        templates = _load_user_templates()
        if not templates:
            sublime.status_message("EDI Markdown: Keine eigenen Vorlagen vorhanden")
            return

        self._keys = list(templates.keys())
        self._templates = templates

        labels = [templates[k].get("name", k) for k in self._keys]
        self.view.window().show_quick_panel(labels, self._on_select)

    def _on_select(self, index):
        if index == -1:
            return
        key = self._keys[index]
        name = self._templates[key].get("name", key)
        templates = _load_user_templates()
        del templates[key]
        _save_user_templates(templates)
        sublime.status_message(
            "EDI Markdown: Vorlage '{}' gelöscht".format(name)
        )

    def is_enabled(self):
        return self.view.match_selector(0, "text.html.markdown")
