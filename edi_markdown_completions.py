import sublime
import sublime_plugin
import os
import json


class EdiMarkdownCompletionListener(sublime_plugin.EventListener):
    """Autocomplete provider for EDI Markdown snippets.

    Typing 'tbl', 'flow', or 'doc' triggers relevant completions.
    """

    _COMPLETIONS = [
        # Tables
        ("tbl.profil\tProfil-Übersicht",        "edi_insert_table_profil"),
        ("tbl.felder\tFeld-Tabelle",             "edi_insert_table_felder"),
        ("tbl.mapping\tMapping-Tabelle",         "edi_insert_table_mapping"),
        ("tbl.var\tVariablen-Tabelle",           "edi_insert_table_var"),
        ("tbl.macro\tMacro-Tabelle",             "edi_insert_table_macro"),
        ("tbl.response\tResponse Units",         "edi_insert_table_response"),
        ("tbl.fehler\tFehlerbehandlung",         "edi_insert_table_fehler"),
        ("tbl.lbase\tLbase-Feld-Tabelle",        "edi_insert_table_lbase"),
        # Flowcharts
        ("flow.simple\tEinfacher Flowchart",     "edi_insert_flow_simple"),
        ("flow.lobster\tLobster Pipeline",       "edi_insert_flow_lobster"),
        ("flow.decision\tEntscheidung",          "edi_insert_flow_decision"),
        ("flow.error\tFehlerbehandlung",         "edi_insert_flow_error_handling"),
        ("flow.wizard\tFlowchart-Wizard",        "edi_insert_flow_wizard"),
        # Documents
        ("doc.profil\tProfil-Dokumentation",     "edi_insert_doc_profil"),
        ("doc.bereich\tBereichsseite",           "edi_insert_doc_bereich"),
        ("doc.prozess\tProzess-Beschreibung",    "edi_insert_doc_prozess"),
        ("doc.macro\tMacro-Dokumentation",       "edi_insert_doc_macro"),
    ]

    def on_query_completions(self, view, prefix, locations):
        if not view.match_selector(locations[0], "text.html.markdown"):
            return None

        prefix_lower = prefix.lower()
        if not any(prefix_lower.startswith(p) for p in ("tbl", "flow", "doc", "my")):
            return None

        completions = []
        for trigger, command in self._COMPLETIONS:
            completions.append(
                sublime.CompletionItem(
                    trigger=trigger.split("\t")[0],
                    annotation=trigger.split("\t")[1],
                    completion="",
                    completion_format=sublime.COMPLETION_FORMAT_TEXT,
                    kind=(sublime.KIND_ID_SNIPPET, "E", "EDI"),
                    details="EDI Markdown",
                    command=command,
                )
            )

        # Add user-defined templates (trigger: my.*)
        user_path = os.path.join(
            sublime.packages_path(), "User", "EDI Markdown Tools", "user_templates.json"
        )
        if os.path.isfile(user_path):
            try:
                with open(user_path, "r", encoding="utf-8") as f:
                    user_templates = json.load(f)
                for key, entry in user_templates.items():
                    completions.append(
                        sublime.CompletionItem(
                            trigger="my.{}".format(key),
                            annotation=entry.get("name", key),
                            completion="",
                            completion_format=sublime.COMPLETION_FORMAT_TEXT,
                            kind=(sublime.KIND_ID_SNIPPET, "U", "User"),
                            details=entry.get("category", "eigene Vorlage"),
                            command="edi_insert_snippet_user",
                            command_args={"key": key},
                        )
                    )
            except Exception:
                pass

        return sublime.CompletionList(
            completions,
            flags=sublime.INHIBIT_WORD_COMPLETIONS | sublime.INHIBIT_EXPLICIT_COMPLETIONS,
        )
