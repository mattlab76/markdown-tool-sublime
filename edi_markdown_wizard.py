import sublime
import sublime_plugin


class EdiInsertFlowWizardCommand(sublime_plugin.TextCommand):
    """Interactive wizard: asks for number of steps, then generates an ASCII flowchart."""

    def run(self, edit):
        self.view.window().show_input_panel(
            "Anzahl Schritte (2–10):", "3", self._on_count, None, None
        )

    def _on_count(self, text):
        try:
            count = int(text.strip())
        except ValueError:
            sublime.status_message("EDI Markdown: Bitte eine Zahl eingeben")
            return

        if count < 2 or count > 10:
            sublime.status_message("EDI Markdown: Anzahl muss zwischen 2 und 10 liegen")
            return

        self.view.window().show_input_panel(
            "Titel des Flowcharts:", "Prozess", lambda t: self._on_title(t, count), None, None
        )

    def _on_title(self, title, count):
        snippet = self._build_flowchart(title.strip(), count)
        self.view.run_command("insert_snippet", {"contents": snippet})

    def _build_flowchart(self, title, count):
        lines = []
        lines.append("### {}\n".format(title))
        lines.append("```")

        placeholder_idx = 1
        for i in range(count):
            placeholder = "${{{}:Schritt {}}}".format(placeholder_idx, i + 1)
            placeholder_idx += 1

            lines.append("┌─────────────────────┐")
            lines.append("│  {}      │".format(placeholder))
            lines.append("└──────────┬──────────┘")

            if i < count - 1:
                lines.append("           │")
                lines.append("           ▼")

        lines.append("```")
        lines.append("\n$0")

        return "\n".join(lines)

    def is_enabled(self):
        return self.view.match_selector(0, "text.html.markdown")
